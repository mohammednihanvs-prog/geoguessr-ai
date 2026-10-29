import os
import sys
import time
import json
import urllib.request
import urllib.parse
from PIL import Image
from io import BytesIO

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEST_DIR = "Imgs"
os.makedirs(DEST_DIR, exist_ok=True)

# Curated dataset of target training images with specific Wikimedia search queries
IMAGE_TARGETS = [
    # --- Local Kerala Villages & Towns ---
    {
        "filename": "Munnar_Idukki_Kerala_India.jpg",
        "query": "Munnar tea plantation road landscape Kerala"
    },
    {
        "filename": "Fort_Kochi_Ernakulam_Kerala_India.jpg",
        "query": "Chinese fishing nets Fort Kochi Kerala street"
    },
    {
        "filename": "Kuttanad_Alappuzha_Kerala_India.jpg",
        "query": "Kuttanad backwaters canal Kerala"
    },
    {
        "filename": "Alappuzha_Town_Beach_Kerala_India.jpg",
        "query": "Alappuzha beach pier Kerala landscape"
    },
    {
        "filename": "Aranmula_Pathanamthitta_Kerala_India.jpg",
        "query": "Aranmula Parthasarathy temple Kerala"
    },
    {
        "filename": "Kovalam_Beach_Thiruvananthapuram_Kerala_India.jpg",
        "query": "Kovalam lighthouse beach Kerala sea"
    },
    {
        "filename": "Varkala_Cliff_Thiruvananthapuram_Kerala_India.jpg",
        "query": "Varkala beach cliff Kerala"
    },
    {
        "filename": "Athirappilly_Thrissur_Kerala_India.jpg",
        "query": "Athirappilly waterfall Kerala river"
    },
    {
        "filename": "Bekal_Fort_Kasaragod_Kerala_India.jpg",
        "query": "Bekal Fort Kasaragod Kerala"
    },
    {
        "filename": "Sulthan_Bathery_Wayanad_Kerala_India.jpg",
        "query": "Wayanad landscape road Kerala"
    },
    {
        "filename": "Vagamon_Idukki_Kerala_India.jpg",
        "query": "Vagamon pine forest hills Kerala"
    },
    {
        "filename": "Kumarakom_Kottayam_Kerala_India.jpg",
        "query": "Kumarakom Vembanad lake Kerala backwater"
    },
    {
        "filename": "Palakkad_Fort_Kerala_India.jpg",
        "query": "Palakkad Fort Kerala Tipu"
    },
    {
        "filename": "Calicut_Beach_Kozhikode_Kerala_India.jpg",
        "query": "Kozhikode beach pier Calicut Kerala"
    },
    {
        "filename": "Thrissur_Swaraj_Round_Kerala_India.jpg",
        "query": "Vadakkunnathan temple Thrissur Kerala"
    },
    {
        "filename": "Ponmudi_Hill_Thiruvananthapuram_Kerala_India.jpg",
        "query": "Ponmudi hill station Kerala road"
    },
    {
        "filename": "Munroe_Island_Kollam_Kerala_India.jpg",
        "query": "Munroe Island Kollam Kerala canal"
    },

    # --- Pan-India Landmarks & Cultural Centers ---
    {
        "filename": "Varanasi_Ghats_Uttar_Pradesh_India.jpg",
        "query": "Varanasi Ghats river Ganges boat ancient temples"
    },
    {
        "filename": "Old_Delhi_Chandni_Chowk_Delhi_India.jpg",
        "query": "Chandni Chowk Old Delhi street"
    },
    {
        "filename": "Hampi_Bellary_Karnataka_India.jpg",
        "query": "Hampi ruins Virupaksha temple Karnataka"
    },
    {
        "filename": "Jaipur_Pink_City_Rajasthan_India.jpg",
        "query": "Hawa Mahal Jaipur Rajasthan street view"
    },
    {
        "filename": "Mumbai_Marine_Drive_Maharashtra_India.jpg",
        "query": "Marine Drive Mumbai promenade"
    },
    {
        "filename": "Kolkata_Howrah_Bridge_West_Bengal_India.jpg",
        "query": "Howrah bridge Kolkata yellow taxi street"
    },
    {
        "filename": "Amritsar_Golden_Temple_Punjab_India.jpg",
        "query": "Harmandir Sahib Golden Temple Amritsar Punjab"
    },
    {
        "filename": "Shimla_Mall_Road_Himachal_Pradesh_India.jpg",
        "query": "The Ridge Shimla Christ Church Himachal"
    },
    {
        "filename": "Ladakh_Pangong_Tso_India.jpg",
        "query": "Pangong Tso lake Ladakh mountains cold desert"
    },
    {
        "filename": "Goa_Panaji_Latin_Quarter_India.jpg",
        "query": "Fontainhas Panaji Goa Latin Quarter colonial houses"
    },
    {
        "filename": "Meghalaya_Living_Root_Bridge_India.jpg",
        "query": "Living root bridge Meghalaya"
    },
    {
        "filename": "Bengaluru_Vidhana_Soudha_Karnataka_India.jpg",
        "query": "Vidhana Soudha Bangalore Karnataka"
    },

    # --- Global Iconic Locations ---
    {
        "filename": "Tokyo_Shinjuku_Japan.jpg",
        "query": "Tokyo street view daytime buildings"
    },
    {
        "filename": "Kyoto_Gion_Japan.jpg",
        "query": "Kyoto street traditional machiya"
    },
    {
        "filename": "Paris_Haussmann_Boulevard_France.jpg",
        "query": "Paris street view Haussmann architecture"
    },
    {
        "filename": "London_Westminster_United_Kingdom.jpg",
        "query": "London street Westminster double decker"
    },
    {
        "filename": "New_York_City_Manhattan_United_States.jpg",
        "query": "Manhattan street view yellow cab"
    },
    {
        "filename": "Amsterdam_Canal_Netherlands.jpg",
        "query": "Amsterdam canal houses bridge bicycle"
    },
    {
        "filename": "Rome_Street_Colosseum_Italy.jpg",
        "query": "Colosseum Rome Italy street view"
    },
    {
        "filename": "Swiss_Alps_Lauterbrunnen_Switzerland.jpg",
        "query": "Lauterbrunnen valley Swiss Alps waterfall"
    },
    {
        "filename": "Sydney_Harbour_Australia.jpg",
        "query": "Sydney Opera House Harbour Bridge"
    },
    {
        "filename": "Rio_de_Janeiro_Copacabana_Brazil.jpg",
        "query": "Copacabana Rio de Janeiro beach promenade"
    },
    {
        "filename": "Reykjavik_Iceland.jpg",
        "query": "Iceland landscape highway volcanic"
    },
    {
        "filename": "Dubai_Sheikh_Zayed_Road_UAE.jpg",
        "query": "Dubai skyline Burj Khalifa highway"
    },

    # --- Expanded High-Diversity Batch ---
    {
        "filename": "Thalassery_Kannur_Kerala_India.jpg",
        "query": "Thalassery fort sea pier Kerala"
    },
    {
        "filename": "Muzhappilangad_Drive_in_Beach_Kerala_India.jpg",
        "query": "Muzhappilangad drive in beach Kerala coast"
    },
    {
        "filename": "Kovalam_Beach_Thiruvananthapuram_Kerala_India.jpg",
        "query": "Kovalam lighthouse beach Kerala"
    },
    {
        "filename": "Madurai_Meenakshi_Tamil_Nadu_India.jpg",
        "query": "Madurai Meenakshi temple gopuram Tamil Nadu"
    },
    {
        "filename": "Mysore_Palace_Karnataka_India.jpg",
        "query": "Mysore Palace facade Karnataka illuminated"
    },
    {
        "filename": "Agra_Taj_Mahal_Uttar_Pradesh_India.jpg",
        "query": "Taj Mahal Agra Uttar Pradesh marble reflection"
    },
    {
        "filename": "Udaipur_City_Palace_Rajasthan_India.jpg",
        "query": "Udaipur City Palace Lake Pichola Rajasthan"
    },
    {
        "filename": "Darjeeling_Tea_Garden_West_Bengal_India.jpg",
        "query": "Darjeeling tea garden toy train Himalayas"
    },
    {
        "filename": "Kashmir_Dal_Lake_Srinagar_India.jpg",
        "query": "Dal Lake Srinagar Shikara houseboat snow Kashmir"
    },
    {
        "filename": "Rishikesh_Ganga_Uttarakhand_India.jpg",
        "query": "Rishikesh Laxman Jhula bridge Ganga river ashram"
    },
    {
        "filename": "Hyderabad_Charminar_Telangana_India.jpg",
        "query": "Charminar Hyderabad street view"
    },
    {
        "filename": "Cairo_Giza_Pyramids_Egypt.jpg",
        "query": "Giza Pyramids Cairo Egypt desert"
    },
    {
        "filename": "Cape_Town_Table_Mountain_South_Africa.jpg",
        "query": "Table Mountain Cape Town South Africa coast"
    },
    {
        "filename": "Santorini_Oia_Greece.jpg",
        "query": "Santorini Oia white houses blue dome church Greece"
    },
    {
        "filename": "Bavaria_Neuschwanstein_Germany.jpg",
        "query": "Neuschwanstein Castle Bavaria Germany mountain"
    },
    {
        "filename": "Seoul_Gangnam_South_Korea.jpg",
        "query": "Seoul street view daytime buildings Korea"
    },
    {
        "filename": "San_Francisco_Golden_Gate_United_States.jpg",
        "query": "Golden Gate Bridge San Francisco street view California"
    },
    {
        "filename": "Tuscany_Val_d_Orcia_Italy.jpg",
        "query": "Tuscany cypress trees road hills Italy"
    },
    {
        "filename": "Scottish_Highlands_Scotland_UK.jpg",
        "query": "Scottish Highlands road loch Scotland UK"
    },
    {
        "filename": "Singapore_Marina_Bay_Singapore.jpg",
        "query": "Marina Bay Sands Singapore skyline street"
    },
    {
        "filename": "Toronto_CN_Tower_Canada.jpg",
        "query": "Toronto skyline CN Tower street view Canada"
    }
]

def search_wikimedia_image(query):
    encoded_query = urllib.parse.quote(query)
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrnamespace=6&gsrsearch={encoded_query}&gsrlimit=3&prop=imageinfo"
        f"&iiprop=url|mime&iiurlwidth=1000&format=json"
    )
    headers = {"User-Agent": "GeoGuessrEducationDataset/2.0 (contact: user@school.edu)"}

    for attempt in range(3):
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as response:
                data = json.loads(response.read())
                pages = data.get("query", {}).get("pages", {})
                for page_id, page_data in pages.items():
                    image_info = page_data.get("imageinfo", [{}])[0]
                    thumb_url = image_info.get("thumburl")
                    if thumb_url:
                        return thumb_url
                    raw_url = image_info.get("url")
                    if raw_url and (raw_url.lower().endswith(".jpg") or raw_url.lower().endswith(".jpeg") or raw_url.lower().endswith(".png")):
                        return raw_url
            break
        except urllib.error.HTTPError as he:
            if he.code == 429:
                print(f"    (Rate limited, waiting 6 seconds on attempt {attempt+1})...", flush=True)
                time.sleep(6)
            else:
                print(f"    (HTTP {he.code} on '{query}')", flush=True)
                break
        except Exception as e:
            print(f"    (API error: {e})", flush=True)
            time.sleep(2)
    return None

def download_and_save(img_url, out_path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(img_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read()
        pil_img = Image.open(BytesIO(content)).convert("RGB")
        if max(pil_img.size) > 1200:
            pil_img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        pil_img.save(out_path, "JPEG", quality=90)
        return pil_img.size

print(f"=== Downloading {len(IMAGE_TARGETS)} Training & Test Images to '{DEST_DIR}/' ===", flush=True)
downloaded_count = 0

for idx, item in enumerate(IMAGE_TARGETS, start=1):
    dest_path = os.path.join(DEST_DIR, item["filename"])
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        print(f"[{idx}/{len(IMAGE_TARGETS)}] Already cached: {item['filename']}", flush=True)
        downloaded_count += 1
        continue

    print(f"[{idx}/{len(IMAGE_TARGETS)}] Fetching: {item['filename']}...", flush=True)
    img_url = search_wikimedia_image(item["query"])
    if img_url:
        try:
            size = download_and_save(img_url, dest_path)
            print(f"  -> Saved {item['filename']} ({size[0]}x{size[1]})", flush=True)
            downloaded_count += 1
        except Exception as err:
            print(f"  -> Download error: {err}", flush=True)
    else:
        print(f"  -> No image found for '{item['query']}'", flush=True)

    # Respect rate limits
    time.sleep(2.0)

print(f"\nDone! Gathered {downloaded_count}/{len(IMAGE_TARGETS)} images in '{DEST_DIR}/'.", flush=True)
