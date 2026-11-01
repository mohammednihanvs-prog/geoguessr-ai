"""
Precision GeoGuessr Scoring & Distance-Error Training Engine
Provides:
1. Improved tiered point scheme based on physical distance and error (0.0 to 5.0 pts).
2. Vectorized distance error computation for model training and evaluation.
3. Distance-aware loss computation for training Residual Vision Adapter.
"""

import math
import torch


def compute_geoguessr_score(dist_km):
    """
    Tiered precision 5.0-point scoring system based on distance error:
    - Under 5 km: 5.0 / 5.0 pts (Bullseye!)
    - 5 - 25 km: 4.50 - 4.99 pts (Pinpoint local town/city)
    - 25 - 100 km: 3.50 - 4.49 pts (Regional vicinity / adjacent district)
    - 100 - 500 km: 2.00 - 3.49 pts (State / Sub-national zone)
    - 500 - 2500 km: 0.50 - 1.99 pts (Continental boundary)
    - > 2500 km: 0.00 - 0.49 pts (Global miss)
    """
    d = float(dist_km)
    if d <= 5.0:
        return 5.0
    elif d <= 25.0:
        score = 5.0 - 0.5 * ((d - 5.0) / 20.0)
        return round(score, 2)
    elif d <= 100.0:
        score = 4.5 - 1.0 * ((d - 25.0) / 75.0)
        return round(score, 2)
    elif d <= 500.0:
        score = 3.5 - 1.5 * ((d - 100.0) / 400.0)
        return round(score, 2)
    elif d <= 2500.0:
        score = 2.0 - 1.5 * ((d - 500.0) / 2000.0)
        return round(score, 2)
    else:
        score = 0.5 * math.exp(-(d - 2500.0) / 3000.0)
        return round(max(0.0, min(0.5, score)), 2)


def compute_geoguessr_score_details(dist_km):
    """
    Returns (score, rating_badge, hex_color, accuracy_pct).
    """
    d = float(dist_km)
    score = compute_geoguessr_score(d)
    if d <= 5.0:
        return score, "🎯 Bullseye (<5 km)", "#00FFA3", 100.0
    elif d <= 25.0:
        return score, "📍 Pinpoint (<25 km)", "#38ef7d", round(score / 5.0 * 100, 1)
    elif d <= 100.0:
        return score, "🗺️ Regional (<100 km)", "#00d2ff", round(score / 5.0 * 100, 1)
    elif d <= 500.0:
        return score, "🧭 Sub-National (<500 km)", "#f39c12", round(score / 5.0 * 100, 1)
    elif d <= 2500.0:
        return score, "🌍 Continental (<2500 km)", "#e67e22", round(score / 5.0 * 100, 1)
    else:
        return score, "🌐 Global Miss (>2500 km)", "#e74c3c", round(score / 5.0 * 100, 1)


class TrainingMetrics(dict):
    """
    Container for detailed training metrics.
    Supports backward-compatible unpacking:
        acc_init, acc_final, elapsed = metrics
    while also providing key-value access to distance error telemetry.
    """
    def __iter__(self):
        yield self.get("acc_init", 0.0)
        yield self.get("acc_final", 0.0)
        yield self.get("elapsed", 0.0)


def compute_batch_distance_errors(preds, targets, loc_lats, loc_lons):
    """
    Vectorized Haversine distance computation in km between predictions and targets.
    Returns (dists_tensor, mean_err, median_err, bullseye_pct, pinpoint_pct).
    """
    lat_p, lon_p = loc_lats[preds], loc_lons[preds]
    lat_t, lon_t = loc_lats[targets], loc_lons[targets]
    dlat = torch.deg2rad(lat_p - lat_t)
    dlon = torch.deg2rad(lon_p - lon_t)
    a = torch.sin(dlat / 2.0)**2 + torch.cos(torch.deg2rad(lat_t)) * torch.cos(torch.deg2rad(lat_p)) * torch.sin(dlon / 2.0)**2
    c = 2.0 * torch.atan2(torch.sqrt(a), torch.sqrt((1.0 - a).clamp(min=1e-7)))
    dists = 6371.0 * c
    mean_err = dists.mean().item()
    median_err = dists.median().item()
    bullseye = (dists <= 5.0).float().mean().item() * 100.0
    pinpoint = (dists <= 25.0).float().mean().item() * 100.0
    return dists, mean_err, median_err, bullseye, pinpoint


def compute_distance_penalty_matrix(targets, loc_lats, loc_lons, max_penalty_km=2500.0):
    """
    Computes a pairwise distance penalty matrix of shape (batch_size, num_locations)
    for use in distance-aware training loss.
    """
    y_lats = loc_lats[targets].unsqueeze(1)
    y_lons = loc_lons[targets].unsqueeze(1)
    all_lats = loc_lats.unsqueeze(0)
    all_lons = loc_lons.unsqueeze(0)
    dlat = torch.deg2rad(all_lats - y_lats)
    dlon = torch.deg2rad(all_lons - y_lons)
    a = torch.sin(dlat / 2.0)**2 + torch.cos(torch.deg2rad(y_lats)) * torch.cos(torch.deg2rad(all_lats)) * torch.sin(dlon / 2.0)**2
    c = 2.0 * torch.atan2(torch.sqrt(a), torch.sqrt((1.0 - a).clamp(min=1e-7)))
    dist_matrix_km = 6371.0 * c
    return (dist_matrix_km / max_penalty_km).clamp(max=1.0)
