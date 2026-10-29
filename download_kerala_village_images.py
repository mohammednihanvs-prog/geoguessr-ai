import os
import sys
import json
import time
import urllib.request
import urllib.parse
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Target curated remote Kerala village shots and random rural shots
VILLAGE_TARGETS = [
    # (Target Filename, Wikimedia Search Query)
    ("Vattavada_Farming_Village_Idukki_Kerala_India.jpg", "Vattavada Kerala"),
    ("Kanthalloor_Village_Road_Idukki_Kerala_India.jpg", "Kanthalloor"),
    ("Suryanelli_Tea_Hills_Idukki_Kerala_India.jpg", "Suryanelli Kerala"),
    ("Chinnakanal_Mountain_Road_Idukki_Kerala_India.jpg", "Chinnakanal"),
    ("Mankulam_River_Road_Idukki_Kerala_India.jpg", "Mankulam Kerala"),
    ("Marayoor_Sandalwood_Road_Idukki_Kerala_India.jpg", "Marayoor Kerala"),
    ("Kollengode_Palakkad_Kerala_India.jpg", "Kollengode Palakkad"),
    ("Nelliyampathy_Hills_Palakkad_Kerala_India.jpg", "Nelliyampathy"),
    ("Silent_Valley_Buffer_Palakkad_Kerala_India.jpg", "Silent Valley Kerala"),
    ("Attappadi_Tribal_Valley_Palakkad_Kerala_India.jpg", "Attappadi"),
    ("Meppadi_Tea_Road_Wayanad_Kerala_India.jpg", "Meppadi Wayanad"),
    ("Thirunelly_Temple_Road_Wayanad_Kerala_India.jpg", "Thirunelli"),
    ("Pulpally_Village_Wayanad_Kerala_India.jpg", "Pulpally"),
    ("Banasura_Sagar_Dam_Wayanad_Kerala_India.jpg", "Banasura Sagar Dam"),
    ("Kuruva_Dweep_River_Wayanad_Kerala_India.jpg", "Kuruvadweep"),
    ("Pulinkunnu_Backwater_Canal_Alappuzha_Kerala_India.jpg", "Pulinkunnoo"),
    ("Champakulam_Church_Road_Alappuzha_Kerala_India.jpg", "Champakulam Church"),
    ("Kavalam_Paddy_Canal_Alappuzha_Kerala_India.jpg", "Kavalam Alappuzha"),
    ("Thakazhy_Village_Road_Alappuzha_Kerala_India.jpg", "Thakazhy"),
    ("Edathua_River_Paddy_Alappuzha_Kerala_India.jpg", "Edathua Church"),
    ("Gavi_Forest_Road_Pathanamthitta_Kerala_India.jpg", "Gavi Kerala"),
    ("Konni_Elephant_Reserve_Pathanamthitta_Kerala_India.jpg", "Konni Kerala"),
    ("Perunthenaruvi_Falls_Pathanamthitta_Kerala_India.jpg", "Perunthenaruvi Waterfalls"),
    ("Aymanam_Village_Canal_Kottayam_Kerala_India.jpg", "Aymanam"),
    ("Ilaveezhapoonchira_Hills_Kottayam_Kerala_India.jpg", "Ilaveezhapoonchira"),
    ("Marmala_Waterfalls_Kottayam_Kerala_India.jpg", "Marmala waterfalls"),
    ("Vaikom_Backwaters_Kottayam_Kerala_India.jpg", "Vaikom Kerala"),
    ("Thenmala_Eco_Dam_Kollam_Kerala_India.jpg", "Thenmala"),
    ("Sasthamkotta_Freshwater_Lake_Kollam_Kerala_India.jpg", "Sasthamkotta Lake"),
    ("Arippa_Forest_Road_Kollam_Kerala_India.jpg", "Arippa Kerala"),
    ("Bonacaud_Tea_Bungalow_Thiruvananthapuram_Kerala_India.jpg", "Bonacaud"),
    ("Neyyar_Dam_Road_Thiruvananthapuram_Kerala_India.jpg", "Neyyar Dam"),
    ("Poovar_Estuary_Beach_Thiruvananthapuram_Kerala_India.jpg", "Poovar"),
    ("Malakkappara_Tea_Highway_Thrissur_Kerala_India.jpg", "Malakkappara"),
    ("Vazhachal_Forest_Falls_Thrissur_Kerala_India.jpg", "Vazhachal Falls"),
    ("Peechi_Dam_Canal_Thrissur_Kerala_India.jpg", "Peechi Dam"),
    ("Kumbalangi_Integrated_Village_Ernakulam_Kerala_India.jpg", "Kumbalangi"),
    ("Bhoothathankettu_Barrage_Ernakulam_Kerala_India.jpg", "Bhoothathankettu"),
    ("Karuvarakundu_Waterfall_Road_Malappuram_Kerala_India.jpg", "Karuvarakundu"),
    ("Kakkadampoyil_Hill_Road_Malappuram_Kerala_India.jpg", "Kakkadampoyil"),
    ("Nilambur_Teak_Plantation_Malappuram_Kerala_India.jpg", "Nilambur Teak"),
    ("Kakkayam_Dam_Valley_Kozhikode_Kerala_India.jpg", "Kakkayam Dam"),
    ("Thusharagiri_Village_Falls_Kozhikode_Kerala_India.jpg", "Thusharagiri Falls"),
    ("Madayipara_Laterite_Plateau_Kannur_Kerala_India.jpg", "Madayipara"),
    ("Paithalmala_Fog_Ridge_Kannur_Kerala_India.jpg", "Paithalmala"),
    ("Dharmadam_Island_Beach_Kannur_Kerala_India.jpg", "Dharmadam Island"),
    ("Ranipuram_Hill_Village_Kasaragod_Kerala_India.jpg", "Ranipuram"),
    ("Kottancheri_Rainforest_Kasaragod_Kerala_India.jpg", "Kottancheri Hills"),
    ("Ananthapura_Lake_Temple_Kasaragod_Kerala_India.jpg", "Ananthapura Lake Temple"),
    ("Nileshwaram_River_Kasaragod_Kerala_India.jpg", "Nileshwaram"),
    # Random Shots & Micro-Cues across Kerala Interior
    ("Kerala_Rural_Village_Paddy_Road.jpg", "Kerala paddy field road"),
    ("Kerala_Country_Tea_Shop_Chayakada.jpg", "tea shop Kerala"),
    ("Kerala_Laterite_Red_Soil_Path.jpg", "red soil road Kerala"),
    ("Kerala_Backwater_Canal_Country_Boat.jpg", "country boat canal Kerala"),
    ("Kerala_Western_Ghats_Misty_Curve.jpg", "Western Ghats hairpin curve")
]

USER_AGENT = "GeoGuessrKeralaLocalDataset/2.5 (contact: nihangeo@local.edu; educational machine-learning research)"

def search_wikimedia_thumbnail(query):
    encoded_q = urllib.parse.quote(query)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={encoded_q}&gsrnamespace=6&gsrlimit=3&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for p in pages.values():
                    info_list = p.get("imageinfo", [])
                    if not info_list:
                        continue
                    thumb_url = info_list[0].get("thumburl")
                    if thumb_url and ("jpg" in thumb_url.lower() or "jpeg" in thumb_url.lower() or "png" in thumb_url.lower()):
                        return thumb_url
                return None
        except urllib.error.HTTPError as he:
            if he.code == 429:
                wait_sec = 4 * (attempt + 1)
                print(f"    [Rate limited, waiting {wait_sec}s]...")
                time.sleep(wait_sec)
            else:
                print(f"    [HTTP Error {he.code}]: {he.reason}")
                break
        except Exception as e:
            print(f"    [Search Error]: {e}")
            break
    return None

def download_and_optimize(url, target_path):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    temp_path = target_path + ".download"

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                with open(temp_path, "wb") as f:
                    f.write(resp.read())

            with Image.open(temp_path) as img:
                img_rgb = img.convert("RGB")
                img_rgb.save(target_path, "JPEG", quality=88, optimize=True)

            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            return True
        except urllib.error.HTTPError as he:
            if he.code == 429:
                wait_sec = 4 * (attempt + 1)
                print(f"    [Download 429, waiting {wait_sec}s]...")
                time.sleep(wait_sec)
            else:
                break
        except Exception as e:
            print(f"    [Download failed]: {e}")
            break

    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except Exception:
            pass
    return False

def main():
    os.makedirs("Imgs", exist_ok=True)
    downloaded = 0
    skipped = 0

    print(f"Checking {len(VILLAGE_TARGETS)} Kerala village micro-regions and rural random shots...")
    for idx, (filename, query) in enumerate(VILLAGE_TARGETS):
        target_path = os.path.join("Imgs", filename)
        if os.path.exists(target_path) and os.path.getsize(target_path) > 15000:
            print(f"[{idx+1}/{len(VILLAGE_TARGETS)}] Already cached: {filename}")
            skipped += 1
            continue

        print(f"[{idx+1}/{len(VILLAGE_TARGETS)}] Searching '{query}' for {filename}...")
        thumb_url = search_wikimedia_thumbnail(query)
        time.sleep(1.8) # Respectful delay between queries

        if thumb_url:
            ok = download_and_optimize(thumb_url, target_path)
            if ok:
                size_kb = os.path.getsize(target_path) // 1024
                print(f"  ✓ Downloaded ({size_kb} KB): {filename}")
                downloaded += 1
            else:
                print(f"  ✗ Failed to save image for {filename}")
        else:
            print(f"  ✗ No thumbnail found for query '{query}'")

        time.sleep(1.2) # Delay between image downloads

    print(f"\nFinished! Added {downloaded} new images, {skipped} existing.")
    total_imgs = len([f for f in os.listdir("Imgs") if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    print(f"Total reference images in Imgs/: {total_imgs}")

if __name__ == "__main__":
    main()
