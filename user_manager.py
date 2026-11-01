"""
User Management and Persistent Scoring System
Stores all player accounts, profiles, passwords, match history, and active sessions
in a dedicated 'user_data' folder with atomic file syncing.
"""

import os
import json
import hashlib
import tempfile
from datetime import datetime

USER_DATA_DIR = "user_data"
USERS_FILE = os.path.join(USER_DATA_DIR, "users.json")
MATCH_HISTORY_FILE = os.path.join(USER_DATA_DIR, "match_history.json")
SESSION_FILE = os.path.join(USER_DATA_DIR, "active_session.json")
ROOT_USERS_FILE = "users.json"


def hash_pw(pw):
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def init_user_storage():
    """Ensure user_data directory exists and migrate existing users from root if needed."""
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    # Migrate from root users.json if present
    migrated_users = {}
    if os.path.exists(ROOT_USERS_FILE):
        try:
            with open(ROOT_USERS_FILE, "r", encoding="utf-8") as f:
                migrated_users = json.load(f)
        except Exception:
            migrated_users = {}

    current_users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                current_users = json.load(f)
        except Exception:
            current_users = {}

    # Merge: keep existing current_users, add any missing from root
    for k, v in migrated_users.items():
        if k not in current_users:
            current_users[k] = v

    # Always ensure admin user straightfamily exists
    if "straightfamily" not in current_users:
        current_users["straightfamily"] = {
            "password_hash": hash_pw("gayless"),
            "total_score": 0.0,
            "rounds_played": 0,
            "wins": 0,
            "losses": 0,
            "best_round_score": 0.0,
            "best_distance_km": None,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat()
        }

    save_users(current_users)

    # Initialize match history
    if not os.path.exists(MATCH_HISTORY_FILE):
        try:
            with open(MATCH_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        except Exception:
            pass

    # Initialize session
    if not os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump({"last_active_user": None}, f, indent=2)
        except Exception:
            pass


def load_users():
    """Loads all user profiles from user_data/users.json with fallback."""
    if not os.path.exists(USERS_FILE):
        init_user_storage()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Fallback to root users.json if user_data is being accessed
        if os.path.exists(ROOT_USERS_FILE):
            try:
                with open(ROOT_USERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}


def save_users(users):
    """
    Saves user profiles atomically to user_data/users.json
    and synchronizes with root users.json for dual redundancy.
    """
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    try:
        # Write to user_data/users.json
        tmp_fd, tmp_path = tempfile.mkstemp(dir=USER_DATA_DIR, prefix="users_tmp_")
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        # Atomic replace on Windows
        if os.path.exists(USERS_FILE):
            os.replace(tmp_path, USERS_FILE)
        else:
            os.rename(tmp_path, USERS_FILE)
    except Exception as e:
        # Fallback direct write
        try:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=2)
        except Exception:
            pass

    # Dual sync to root users.json
    try:
        with open(ROOT_USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
    except Exception:
        pass


def find_user_key(users, username):
    if not username:
        return None
    u_clean = username.strip()
    if u_clean in users:
        return u_clean
    for k in users:
        if k.lower() == u_clean.lower():
            return k
    return None


def register_user(username, password):
    u = username.strip()
    if not u or len(u) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 3:
        return False, "Password must be at least 3 characters."

    users = load_users()
    matched = find_user_key(users, u)
    if matched:
        return False, f"Username '{matched}' already exists. Click 'Sign In' or choose another name."

    users[u] = {
        "password_hash": hash_pw(password),
        "total_score": 0.0,
        "rounds_played": 0,
        "wins": 0,
        "losses": 0,
        "best_round_score": 0.0,
        "best_distance_km": None,
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat()
    }
    save_users(users)
    set_active_session_user(u)
    return True, f"Player profile '{u}' created successfully!"


def authenticate_user(username, password):
    u = username.strip()
    if not u:
        return False, "Please enter your username.", None
    users = load_users()
    matched = find_user_key(users, u)
    if not matched:
        return False, f"Username '{u}' not found. Click '➕ Register New Account' to create this profile!", None

    if users[matched].get("password_hash") != hash_pw(password):
        return False, "Incorrect password. Please try again.", None

    users[matched]["last_active"] = datetime.now().isoformat()
    save_users(users)
    set_active_session_user(matched)
    return True, users[matched], matched


def get_active_session_user():
    """Reads persistent active session from user_data/active_session.json"""
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            u = data.get("last_active_user")
            if u:
                users = load_users()
                matched = find_user_key(users, u)
                return matched
    except Exception:
        pass
    return None


def set_active_session_user(username):
    """Persists current active session so player is never forgotten on refresh."""
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "last_active_user": username,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
    except Exception:
        pass


def clear_active_session():
    """Clears the active session when a player explicitly logs out."""
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "last_active_user": None,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
    except Exception:
        pass


def record_player_round(username, round_score, won, distance_km, extra_details=None):
    """
    Reliably records player score and match results:
    1. Updates user profile totals in user_data/users.json
    2. Logs the individual round in user_data/match_history.json
    3. Keeps the player session actively remembered
    """
    if not username:
        username = "Guest"

    users = load_users()
    matched = find_user_key(users, username)

    if not matched:
        # Create user profile entry so score is never forgotten
        matched = username.strip()
        users[matched] = {
            "password_hash": "",
            "total_score": 0.0,
            "rounds_played": 0,
            "wins": 0,
            "losses": 0,
            "best_round_score": 0.0,
            "best_distance_km": None,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat()
        }

    user = users[matched]
    user["total_score"] = round(float(user.get("total_score", 0.0)) + float(round_score), 1)
    user["rounds_played"] = int(user.get("rounds_played", 0)) + 1

    if won:
        user["wins"] = int(user.get("wins", 0)) + 1
    else:
        user["losses"] = int(user.get("losses", 0)) + 1

    if float(round_score) > float(user.get("best_round_score", 0.0)):
        user["best_round_score"] = round(float(round_score), 1)

    best_d = user.get("best_distance_km")
    if best_d is None or float(distance_km) < float(best_d):
        user["best_distance_km"] = round(float(distance_km), 1)

    user["last_active"] = datetime.now().isoformat()
    users[matched] = user
    save_users(users)

    # Persist to match history
    try:
        history = []
        if os.path.exists(MATCH_HISTORY_FILE):
            with open(MATCH_HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        round_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": matched,
            "round_score": round(float(round_score), 1),
            "distance_km": round(float(distance_km), 1),
            "won": bool(won)
        }
        if extra_details and isinstance(extra_details, dict):
            round_entry.update(extra_details)
        history.append(round_entry)

        tmp_h_fd, tmp_h_path = tempfile.mkstemp(dir=USER_DATA_DIR, prefix="hist_tmp_")
        with os.fdopen(tmp_h_fd, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        if os.path.exists(MATCH_HISTORY_FILE):
            os.replace(tmp_h_path, MATCH_HISTORY_FILE)
        else:
            os.rename(tmp_h_path, MATCH_HISTORY_FILE)
    except Exception as e:
        print("Warning: could not write match history:", e)

    # Ensure active session is kept
    if matched != "Guest":
        set_active_session_user(matched)


def load_match_history(limit=50):
    """Loads recent match logs."""
    if not os.path.exists(MATCH_HISTORY_FILE):
        return []
    try:
        with open(MATCH_HISTORY_FILE, "r", encoding="utf-8") as f:
            hist = json.load(f)
            return list(reversed(hist))[:limit]
    except Exception:
        return []
