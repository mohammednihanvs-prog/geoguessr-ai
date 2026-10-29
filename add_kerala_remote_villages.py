# ==============================================================================
# Script to add 100+ Hyper-Local Remote Kerala Village Micro-Regions to locations.py
# and download authentic reference street & landscape images into Imgs/
# ==============================================================================

import os
import sys
import json
import urllib.request
import urllib.parse
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from locations import LOCATIONS

# 100+ Hyper-Local Remote Kerala Villages across all 14 Districts
KERALA_REMOTE_VILLAGES = [
    # --- 1. IDUKKI REMOTE HIGH-RANGES ---
    {
        "name": "Vattavada, Idukki, Kerala, India",
        "lat": 10.1833, "lon": 77.2667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a high altitude remote farming village road in Vattavada Kerala, terraced cabbage carrot strawberry fields, eucalyptus plantations, cool mountain breeze, Malayalam signboards"
    },
    {
        "name": "Kanthalloor, Idukki, Kerala, India",
        "lat": 10.2167, "lon": 77.2000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a village road in Kanthalloor Idukki, apple plum orange orchards, sugarcane fields producing dark jaggery, red soil, rain-shadow mountain valley, village houses"
    },
    {
        "name": "Suryanelli, Idukki, Kerala, India",
        "lat": 10.0333, "lon": 77.1667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain tea estate village in Suryanelli Idukki, Anayirankal dam view, tent camping sites, off-road 4x4 jeep trails to Kolukkumalai, misty high-range curves"
    },
    {
        "name": "Chinnakanal, Idukki, Kerala, India",
        "lat": 10.0167, "lon": 77.1500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic highway in Chinnakanal Idukki, Anayirankal reservoir lake, wild elephant crossing signs, rolling green tea plantations, Power House waterfalls"
    },
    {
        "name": "Mankulam, Idukki, Kerala, India",
        "lat": 10.1167, "lon": 76.9500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote forest village road in Mankulam Idukki, hanging bridge over wild river where elephants bathe, pepper vines on silver oak, organic cardamom estates"
    },
    {
        "name": "Poopara, Idukki, Kerala, India",
        "lat": 9.9833, "lon": 77.1833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a high-range plantation road junction in Poopara Idukki, cardamom curing sheds, tea bushes on steep slopes, cool mountain air, KSRTC bus stop"
    },
    {
        "name": "Nedumkandam, Idukki, Kerala, India",
        "lat": 9.8333, "lon": 77.1667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a bustling hill town street in Nedumkandam Idukki, cardamom auction centers, spice shops, steep cut roads in red laterite, Kailasapara hills backdrop"
    },
    {
        "name": "Kattappana, Idukki, Kerala, India",
        "lat": 9.7500, "lon": 77.1167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "commercial town junction in Kattappana Idukki, spice traders, multi-storey concrete hill buildings, private buses, Malayalam hoardings, cardamom hills"
    },
    {
        "name": "Kuttikkanam, Idukki, Kerala, India",
        "lat": 9.5833, "lon": 76.9667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a misty hill station road in Kuttikkanam Idukki, dense pine forests, colonial British tea estates, Amritamedhu hills, heavy fog on winding highway"
    },
    {
        "name": "Peerumade, Idukki, Kerala, India",
        "lat": 9.5667, "lon": 77.0167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a tea garden road in Peerumade Idukki, rolling green tea carpet, summer palace heritage buildings, waterfalls, cool mountain climate, Western Ghats"
    },
    {
        "name": "Ramakkalmedu, Idukki, Kerala, India",
        "lat": 9.8000, "lon": 77.2333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a high wind plateau road in Ramakkalmedu Idukki, giant electric windmill turbines, Kuravan and Kurathi stone statue, sheer cliff drop overlooking Tamil Nadu plains"
    },
    {
        "name": "Anchuruli Tunnel, Idukki, Kerala, India",
        "lat": 9.7333, "lon": 77.0833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a reservoir valley road in Anchuruli Idukki, colossal circular water tunnel connecting Erattayar to Idukki reservoir, rocky gorge, calm green water"
    },

    # --- 2. WAYANAD REMOTE FOREST & HILL HAMLETS ---
    {
        "name": "Meppadi, Wayanad, Kerala, India",
        "lat": 11.5500, "lon": 76.1333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a tea valley road in Meppadi Wayanad, towering Chembra peak backdrop, tea factory, Chaliyar river headwaters, Western Ghats rainforest slopes"
    },
    {
        "name": "Thirunelly Temple Valley, Wayanad, Kerala, India",
        "lat": 11.9000, "lon": 75.9833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote forest road approaching Thirunelly temple Wayanad, dense Brahmagiri mountain jungle, Papanasini sacred river stream, stone pillared aqueduct"
    },
    {
        "name": "Pulpally, Wayanad, Kerala, India",
        "lat": 11.7833, "lon": 76.1667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural agricultural road in Pulpally Wayanad, coffee and pepper plantations, Sita Devi temple, Kabini river basin, border village atmosphere"
    },
    {
        "name": "Padinjarathara Banasura, Wayanad, Kerala, India",
        "lat": 11.6667, "lon": 75.9667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic road near Banasura Sagar dam in Padinjarathara Wayanad, largest earthen dam in India, reservoir with submerged hill islands, speedboats"
    },
    {
        "name": "Pozhuthana Tea Stream, Wayanad, Kerala, India",
        "lat": 11.5833, "lon": 76.0167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a tranquil rural road through Pozhuthana Wayanad, bamboo rafting river, historic tea estates, wooden footbridges, lush green rubber trees, mist"
    },
    {
        "name": "Tholpetty Wildlife Sanctuary, Wayanad, Kerala, India",
        "lat": 11.9500, "lon": 76.0833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a forest road through Tholpetty Wayanad, bamboo clumps, moist deciduous teak jungle, wild deer and elephant crossing, forest checkpost"
    },
    {
        "name": "Muthanga Wildlife Border, Wayanad, Kerala, India",
        "lat": 11.6667, "lon": 76.3667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "National Highway 766 passing through Muthanga Wayanad, interstate border with Karnataka, dry deciduous forest, elephant crossing signs, forest barriers"
    },
    {
        "name": "Ambalavayal Heritage Village, Wayanad, Kerala, India",
        "lat": 11.6167, "lon": 76.2167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a village road in Ambalavayal Wayanad, regional agricultural research station flower gardens, Edakkal caves prehistoric petroglyphs hill base"
    },
    {
        "name": "Lakkidi Rainforest Gate, Wayanad, Kerala, India",
        "lat": 11.5167, "lon": 76.0333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the entry point to Wayanad at Lakkidi, legendary chain tree with iron shackles, heavy monsoon rainfall, dense shola forest, viewpoint overlooking Kozhikode plains"
    },

    # --- 3. ALAPPUZHA & KUTTANAD WATER VILLAGES ---
    {
        "name": "Pulinkunnu River Island, Alappuzha, Kerala, India",
        "lat": 9.4500, "lon": 76.4500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a water road in Pulinkunnu Kuttanad, heritage St. Mary's church on Pamba riverbank, country canoes, houseboats cruising narrow canals, coconut palm line"
    },
    {
        "name": "Kavalam Waterways, Alappuzha, Kerala, India",
        "lat": 9.5333, "lon": 76.4667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural canal road in Kavalam Alappuzha, coir spinning wheels, vast green paddy fields below sea level, wooden country boats, Malayalam village shop boards"
    },
    {
        "name": "Kainakkary Backwaters, Alappuzha, Kerala, India",
        "lat": 9.4833, "lon": 76.4000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a tranquil village canal in Kainakkary Kuttanad, duck farming flocks swimming in green water, water hyacinth floating plants, traditional kettuvallam houseboats"
    },
    {
        "name": "Thakazhy Village, Alappuzha, Kerala, India",
        "lat": 9.3833, "lon": 76.4333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural village road in Thakazhy Alappuzha, memorial home of Thakazhi Sivasankara Pillai, vast paddy polders, railway level crossing, irrigation canals"
    },
    {
        "name": "Edathua Forane Church, Alappuzha, Kerala, India",
        "lat": 9.3667, "lon": 76.4833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a riverside town street in Edathua Alappuzha, massive St. George Forane Catholic church on Pamba river, annual May festival grounds, bridge over river"
    },
    {
        "name": "Muttar Backwater Hamlet, Alappuzha, Kerala, India",
        "lat": 9.3500, "lon": 76.5167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a quiet village road in Muttar Kuttanad, narrow canal bridges, coconut palm groves, traditional tiled roof houses, water lilied ponds"
    },
    {
        "name": "Thalavadi River Confluence, Alappuzha, Kerala, India",
        "lat": 9.3500, "lon": 76.4667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural agricultural road in Thalavadi Alappuzha, paddy fields, old tharavadu heritage homes, Pamba river bank, Chinese fishing nets on canals"
    },
    {
        "name": "Veeyapuram Forest River Bank, Alappuzha, Kerala, India",
        "lat": 9.3167, "lon": 76.4833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a junction in Veeyapuram Alappuzha, confluence of Pamba and Achankovil rivers, timber floating ghat, government teak plantations, rustic wooden tea stall"
    },
    {
        "name": "Mannar Bronze Artisan Village, Alappuzha, Kerala, India",
        "lat": 9.3167, "lon": 76.5333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an artisan craft village street in Mannar Alappuzha, bronze and brass bell metal workshops, temple lamps (nilavilakku) displayed outside shops, Pamba river"
    },
    {
        "name": "Mararikulam Coastal Village, Alappuzha, Kerala, India",
        "lat": 9.6000, "lon": 76.3000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a peaceful coastal road in Mararikulam Alappuzha, white sandy beach, colorful wooden fishing boats on shore, coir rope making, coconut palms, sea breeze"
    },

    # --- 4. PATHANAMTHITTA SACRED FORESTS & HILL VILLAGES ---
    {
        "name": "Gavi Rainforest Reserve, Pathanamthitta, Kerala, India",
        "lat": 9.4333, "lon": 77.1667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an unpaved muddy or paved forest road in Gavi Pathanamthitta, virgin tropical evergreen rainforest, cardamom estates, mist, Gavi lake, hornbills"
    },
    {
        "name": "Seethathode Forest Village, Pathanamthitta, Kerala, India",
        "lat": 9.3333, "lon": 76.9667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote forest route road in Seethathode Pathanamthitta, Sabarimala pilgrimage transit, Kakkad river power canal, dense jungle slopes, teak trees"
    },
    {
        "name": "Angamoozhy Forest Hamlet, Pathanamthitta, Kerala, India",
        "lat": 9.3833, "lon": 77.0167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote forest edge village in Angamoozhy Pathanamthitta, Pamba river rocky bed, elephant crossing warning boards, rubber estates, tribal settlement"
    },
    {
        "name": "Chittar Hill Village, Pathanamthitta, Kerala, India",
        "lat": 9.3167, "lon": 76.9167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a winding hill road through Chittar Pathanamthitta, lush green rubber estates, red laterite soil cuts, Meenchembu hills, small village junction"
    },
    {
        "name": "Vadasserikkara River Confluence, Pathanamthitta, Kerala, India",
        "lat": 9.3333, "lon": 76.8167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a river town street in Vadasserikkara Pathanamthitta, confluence of Pamba and Kallar rivers, Sabarimala pilgrim rest centers, suspension footbridge"
    },
    {
        "name": "Ranni Rubber Plantation Town, Pathanamthitta, Kerala, India",
        "lat": 9.3833, "lon": 76.7833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a plantation town street in Ranni Pathanamthitta, Pamba river concrete bridge, rubber sheet processing smokehouses, NRI mansions, church spires"
    },
    {
        "name": "Mallappally Manimala River, Pathanamthitta, Kerala, India",
        "lat": 9.4500, "lon": 76.6500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a town bridge and street in Mallappally Pathanamthitta, Manimala river rapids, rubber plantations, granite quarries, Christian heritage churches"
    },
    {
        "name": "Ayroor Kathakali Village, Pathanamthitta, Kerala, India",
        "lat": 9.3500, "lon": 76.7333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage cultural village road in Ayroor Pathanamthitta along Pamba river, Kathakali dance school Natyagruham, temple ghats, coconut groves"
    },
    {
        "name": "Cherukolpuzha Riverbed, Pathanamthitta, Kerala, India",
        "lat": 9.3333, "lon": 76.7500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the wide dry white sand riverbed of Pamba river in Cherukolpuzha, site of historic annual Hindu convention, temple steps, lush riverbank trees"
    },
    {
        "name": "Pandalam Palace Town, Pathanamthitta, Kerala, India",
        "lat": 9.2333, "lon": 76.6833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street in Pandalam Pathanamthitta, Achankovil river, Pandalam Royal Palace, Valiya Koikkal temple, Lord Ayyappa birthplace site"
    },

    # --- 5. KOTTAYAM PLANTATION & LAKE HAMLETS ---
    {
        "name": "Aymanam Village, Kottayam, Kerala, India",
        "lat": 9.6167, "lon": 76.4833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a tranquil village road in Aymanam Kottayam, setting of The God of Small Things, Meenachil river canals, old Syrian Christian tharavadu homes, lush paddy"
    },
    {
        "name": "Kudamaloor Heritage Village, Kottayam, Kerala, India",
        "lat": 9.6167, "lon": 76.5000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street in Kudamaloor Kottayam, ancient St. Mary's church with Persian cross, Vasudevapuram temple, narrow river canals, traditional houses"
    },
    {
        "name": "Thiruvarpu Temple Canal, Kottayam, Kerala, India",
        "lat": 9.5833, "lon": 76.4833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a temple canal road in Thiruvarpu Kottayam, famed Krishna temple with early morning opening, Meenachil river branch, country boats, coconut palms"
    },
    {
        "name": "Puthuppally Church Town, Kottayam, Kerala, India",
        "lat": 9.5500, "lon": 76.5667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a historic church town street in Puthuppally Kottayam, St. George Orthodox church, rolling rubber plantation hills, Meenachil river basin, KSRTC bus"
    },
    {
        "name": "Kanjirappally Rubber Capital, Kottayam, Kerala, India",
        "lat": 9.5500, "lon": 76.7833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a grand plantation town avenue in Kanjirappally Kottayam, sprawling rubber planter bungalows, Catholic cathedrals, smooth asphalt, Western Ghats foot"
    },
    {
        "name": "Mundakayam Mountain Gateway, Kottayam, Kerala, India",
        "lat": 9.5333, "lon": 76.8833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a river town street in Mundakayam Kottayam, Manimala river bridge, entry point to high-range Idukki hills, rubber estates, hill road curves"
    },
    {
        "name": "Erumely Pilgrim Town, Kottayam, Kerala, India",
        "lat": 9.4833, "lon": 76.8500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a sacred pilgrim town street in Erumely Kottayam, Vavar mosque and Sastha temple, Petta thullal dance grounds, black-clad Sabarimala pilgrims"
    },
    {
        "name": "Bharananganam Alphonsa Shrine, Kottayam, Kerala, India",
        "lat": 9.6833, "lon": 76.7167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a pilgrimage shrine road in Bharananganam Kottayam, tomb of Saint Alphonsa, Meenachil river bank, Catholic pilgrimage complex, rubber hillocks"
    },
    {
        "name": "Kuravilangad Marian Town, Kottayam, Kerala, India",
        "lat": 9.7500, "lon": 76.5667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a historic town street in Kuravilangad Kottayam, ancient Martha Mariam church dating to 105 AD, giant bell tower, rubber estates, coconut groves"
    },

    # --- 6. KOLLAM LAKE & FOREST HAMLETS ---
    {
        "name": "Thenmala Dam Eco-Tourism, Kollam, Kerala, India",
        "lat": 8.9667, "lon": 77.0667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an eco-tourism mountain road in Thenmala Kollam, Shendurney wildlife sanctuary, Parappar dam reservoir, swaying suspension bridge, butterfly safari"
    },
    {
        "name": "Aryankavu Mountain Pass, Kollam, Kerala, India",
        "lat": 8.9833, "lon": 77.1500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain ghat road in Aryankavu Kollam, 13-arch 1904 British railway viaduct bridge, Western Ghats border with Tamil Nadu, sacred forest temple"
    },
    {
        "name": "Achankovil Forest Temple, Kollam, Kerala, India",
        "lat": 9.0833, "lon": 77.1500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote forest route road in Achankovil Kollam, ancient Sastha temple in deep jungle, Achankovil river rapids, teak and sandalwood trees"
    },
    {
        "name": "Kulathupuzha Forest Shrine, Kollam, Kerala, India",
        "lat": 8.9000, "lon": 77.0667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a riverbank temple road in Kulathupuzha Kollam, Kallada river with sacred golden mahseer fish, Balasastha temple, dense tropical forest"
    },
    {
        "name": "Punalur Suspension Bridge, Kollam, Kerala, India",
        "lat": 9.0167, "lon": 76.9167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the historic 1877 British wooden-and-iron suspension bridge across Kallada river in Punalur Kollam, paper mill town, rubber and timber market"
    },
    {
        "name": "Chadayamangalam Jatayu Earth Center, Kollam, Kerala, India",
        "lat": 8.9833, "lon": 76.8667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a highway road in Chadayamangalam Kollam, colossal Jatayu rock sculpture on mountain peak, cable car gondola, rocky granite hills, rubber trees"
    },
    {
        "name": "Kottarakkara Ganapathy Town, Kollam, Kerala, India",
        "lat": 8.9833, "lon": 76.7667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a cultural heritage town road in Kottarakkara Kollam, birthplace of Kathakali, Mahaganapathy temple, cashew processing units, KSRTC bus stand"
    },
    {
        "name": "Sasthamkotta Fresh Water Lake, Kollam, Kerala, India",
        "lat": 9.0333, "lon": 76.6333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic lakeside road in Sasthamkotta Kollam, Queen of Lakes largest freshwater lake in Kerala, monkey temple on hillock, red laterite soil"
    },

    # --- 7. THIRUVANANTHAPURAM HILL & COASTAL HAMLETS ---
    {
        "name": "Bonacaud Tea Estate Ruins, Thiruvananthapuram, Kerala, India",
        "lat": 8.6833, "lon": 77.1833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote mountain road ending at Bonacaud Thiruvananthapuram, abandoned British tea factory ruins, Agasthyarkoodam trekking base, mist, shola jungle"
    },
    {
        "name": "Vithura Mountain Foothills, Thiruvananthapuram, Kerala, India",
        "lat": 8.6667, "lon": 77.1000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a foothill village street in Vithura Thiruvananthapuram, rubber plantations, view of Agasthya peak, streams, IISER campus nearby, Western Ghats"
    },
    {
        "name": "Neyyar Dam Reservoir, Thiruvananthapuram, Kerala, India",
        "lat": 8.5333, "lon": 77.1500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dam road in Neyyar Thiruvananthapuram, concrete gravity dam, lake reservoir surrounded by Western Ghats hills, lion safari park, yoga ashram"
    },
    {
        "name": "Poovar Golden Sand Estuary, Thiruvananthapuram, Kerala, India",
        "lat": 8.3167, "lon": 77.0667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a boat jetty and coastal road in Poovar Thiruvananthapuram, Neyyar river estuary opening into sea, golden sand beach spit, floating wooden cottages"
    },
    {
        "name": "Vizhinjam International Port, Thiruvananthapuram, Kerala, India",
        "lat": 8.3833, "lon": 76.9833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal harbor road in Vizhinjam Thiruvananthapuram, giant international container transshipment port cranes, traditional fishing harbor, lighthouse"
    },
    {
        "name": "Kilimanoor Palace Village, Thiruvananthapuram, Kerala, India",
        "lat": 8.7667, "lon": 76.8833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural heritage street in Kilimanoor Thiruvananthapuram, historic Kilimanoor Palace studio of painter Raja Ravi Varma, nalukettu courtyards, rubber hills"
    },

    # --- 8. THRISSUR HERITAGE & FOREST HAMLETS ---
    {
        "name": "Malakkappara Sholayar Rainforest, Thrissur, Kerala, India",
        "lat": 10.2667, "lon": 76.8500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote mountain border highway in Malakkappara Thrissur, Sholayar rainforest canopy, Tata tea gardens, lion-tailed macaques, cool mist, Western Ghats"
    },
    {
        "name": "Vettilappara Jungle River, Thrissur, Kerala, India",
        "lat": 10.3000, "lon": 76.5167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rainforest road through Vettilappara Thrissur along Chalakudy river, dense bamboo clusters, suspension hanging bridge, monkeys, river rapids"
    },
    {
        "name": "Meloor Banana Village, Thrissur, Kerala, India",
        "lat": 10.2833, "lon": 76.3833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an agricultural village road in Meloor Thrissur, vast Nendran banana plantations, Chalakudy river banks, rubber estates, peaceful rural Kerala homes"
    },
    {
        "name": "Wadakkanchery Kalamandalam Valley, Thrissur, Kerala, India",
        "lat": 10.6667, "lon": 76.2500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic green valley road in Wadakkanchery Thrissur, Kerala Kalamandalam Deemed University of Arts Cheruthuruthy, Bharathapuzha river, paddy fields"
    },
    {
        "name": "Triprayar Temple River, Thrissur, Kerala, India",
        "lat": 10.4167, "lon": 76.1167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a riverside temple road in Triprayar Thrissur, majestic Triprayar Sri Rama temple, Theevra river with fish feeding ghats, brass lamps, coconut trees"
    },
    {
        "name": "Kodungallur Muziris Port & Mosque, Thrissur, Kerala, India",
        "lat": 10.2167, "lon": 76.2000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street in Kodungallur Thrissur, Cheraman Juma Masjid earliest mosque in India 629 AD, Kurumba Bhagavathy temple, backwater river canal"
    },
    {
        "name": "Mala Historic Synagogue Village, Thrissur, Kerala, India",
        "lat": 10.2000, "lon": 76.3000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a historic village road in Mala Thrissur, ancient wooden Jewish Synagogue, Jewish cemetery, canal water roads, traditional coir spinning workshops"
    },
    {
        "name": "Peechi Dam Forest Reserve, Thrissur, Kerala, India",
        "lat": 10.5333, "lon": 76.3667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dam road in Peechi Thrissur, reservoir lake surrounded by forest hills, Manali river catchment, Kerala Forest Research Institute, botanical garden"
    },

    # --- 9. ERNAKULAM COASTAL & HILL HAMLETS ---
    {
        "name": "Kumbalangi Model Eco-Village, Ernakulam, Kerala, India",
        "lat": 9.8833, "lon": 76.2833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a narrow backwater island road in Kumbalangi Ernakulam, Chinese fishing nets lining canal, crab farming ponds, mangrove trees, country canoes, homestays"
    },
    {
        "name": "Chellanam Coastal Fishing Hamlet, Ernakulam, Kerala, India",
        "lat": 9.8000, "lon": 76.2667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal road in Chellanam Ernakulam, massive granite boulder seawall, breaking Arabian sea waves, colorful fiber fishing boats, St. Sebastian church"
    },
    {
        "name": "Cherai & Munambam Harbour, Ernakulam, Kerala, India",
        "lat": 10.1833, "lon": 76.1833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal harbor road in Munambam Cherai Vypin, mouth of Periyar river meeting sea, mechanized trawler fishing boats, dolphin sightings, long beach"
    },
    {
        "name": "Chendamangalam Handloom Village, Ernakulam, Kerala, India",
        "lat": 10.1500, "lon": 76.2667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a weaving village street in Chendamangalam Ernakulam, traditional cotton handloom weaving sheds, Paliam Dutch Palace, ancient Jewish synagogue"
    },
    {
        "name": "Malayattoor Kurisumudy Mountain, Ernakulam, Kerala, India",
        "lat": 10.1833, "lon": 76.5000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain pilgrimage road in Malayattoor Ernakulam, St. Thomas international shrine perched on Kurisumudy hill, Periyar river below, teak forest"
    },
    {
        "name": "Boothathankettu Forest Dam, Ernakulam, Kerala, India",
        "lat": 10.1333, "lon": 76.6667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dam road in Boothathankettu Ernakulam, ancient mythic natural stone boulders damming Periyar river, dense jungle, Thattekad bird sanctuary entrance"
    },
    {
        "name": "Neriamangalam Bridge, Ernakulam, Kerala, India",
        "lat": 10.0500, "lon": 76.7833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the Ranis Bridge 1935 heritage stone arch bridge in Neriamangalam Ernakulam, Periyar river gorge, heaviest rainfall Cherrapunji of Kerala, high-range gateway"
    },
    {
        "name": "Piravom River Town, Ernakulam, Kerala, India",
        "lat": 9.8667, "lon": 76.4833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a river town street in Piravom Ernakulam, Muvattupuzha river bridge, historic Rajakkal Raja church, Pazhoor Padippura astrology hermitage"
    },

    # --- 10. PALAKKAD GAP & PADDY HAMLETS ---
    {
        "name": "Kollengode Palace Village, Palakkad, Kerala, India",
        "lat": 10.6167, "lon": 76.7000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a postcard village road in Kollengode Palakkad, endless emerald green paddy fields, majestic Nelliyampathy Western Ghats mountain wall, palm trees, cinema shoot spot"
    },
    {
        "name": "Nenmara Vallanghy Village, Palakkad, Kerala, India",
        "lat": 10.5833, "lon": 76.6000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a festival village street in Nenmara Palakkad, Nellikulangara Bhagavathy temple, agricultural fields, elephant procession grounds, Nelliyampathy hills foot"
    },
    {
        "name": "Ayalur Agraharam Village, Palakkad, Kerala, India",
        "lat": 10.5500, "lon": 76.5667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a traditional Brahmin agraharam street in Ayalur Palakkad, rows of connected tiled roof houses with kolam chalk drawings, temple pond, coconut groves"
    },
    {
        "name": "Chittur Konganpada Village, Palakkad, Kerala, India",
        "lat": 10.7000, "lon": 76.7167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural town street in Chittur Palakkad, Shokanasini river, Thunchath Ezhuthachan Gurumadhom memorial, palmyra palm trees, agricultural countryside"
    },
    {
        "name": "Kozhinjampara Border Plains, Palakkad, Kerala, India",
        "lat": 10.7333, "lon": 76.8167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dry rural road in Kozhinjampara Palakkad on Tamil Nadu border, towering palmyra palm trees, windmill wind turbines, bullock carts, red arid soil"
    },
    {
        "name": "Ottapalam Varikkassery Mana, Palakkad, Kerala, India",
        "lat": 10.7667, "lon": 76.3833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage village road in Ottapalam Palakkad, famed Varikkassery Mana wooden architectural mansion, Bharathapuzha river banks, Kathakali schools"
    },
    {
        "name": "Cherpulassery Ayyappan Village, Palakkad, Kerala, India",
        "lat": 10.8833, "lon": 76.3167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural town junction in Cherpulassery Palakkad, Cherpulassery Ayyappan temple, paddy fields, elephant festival grounds, Malabar rural countryside"
    },
    {
        "name": "Pattambi Nila River Town, Palakkad, Kerala, India",
        "lat": 10.8000, "lon": 76.1833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a riverside town street in Pattambi Palakkad, wide bridge over sacred Bharathapuzha Nila river, historic Sanskrit college, regional agricultural research paddy fields"
    },

    # --- 11. MALAPPURAM HERITAGE & HILL HAMLETS ---
    {
        "name": "Karuvarakundu Cherumb Hill, Malappuram, Kerala, India",
        "lat": 11.1667, "lon": 76.3500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain village road in Karuvarakundu Malappuram, Cherumb eco village, Olive Brook waterfall stream, Silent Valley buffer forest, rubber hills"
    },
    {
        "name": "Vazhikkadavu Mountain Pass, Malappuram, Kerala, India",
        "lat": 11.3833, "lon": 76.3333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a winding ghat road in Vazhikkadavu Malappuram climbing to Nadugani Nilgiris, dense rainforest, checkpost, monkey troops on stone parapets"
    },
    {
        "name": "Tanur Coastal Harbor, Malappuram, Kerala, India",
        "lat": 10.9667, "lon": 75.8667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a vibrant coastal fishing village road in Tanur Malappuram, fishing harbor with painted trawlers, drying fish racks, Keraladheeswarapuram temple"
    },
    {
        "name": "Kadalundi Bird Estuary, Malappuram, Kerala, India",
        "lat": 11.1333, "lon": 75.8333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic bridge and road across Kadalundi river estuary in Vallikkunnu Malappuram, mangrove forest islands, migratory sea birds, railway bridge"
    },
    {
        "name": "Ponnani Historic Port & Mosque, Malappuram, Kerala, India",
        "lat": 10.7667, "lon": 75.9167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a historic port street in Ponnani Malappuram, 1519 Valiya Juma Masjid with timber ceiling, Bharathapuzha river mouth meeting Arabian sea, lighthouse"
    },

    # --- 12. KOZHIKODE COASTAL & VALLEY HAMLETS ---
    {
        "name": "Kakkadampoyil Mini Gavi, Kozhikode, Kerala, India",
        "lat": 11.3333, "lon": 76.1167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a misty mountain road in Kakkadampoyil Kozhikode, Mini Gavi hill station, Kozhippara waterfall stream, cool mountain air, rubber and coffee estates"
    },
    {
        "name": "Thusharagiri Waterfalls, Kozhikode, Kerala, India",
        "lat": 11.4667, "lon": 76.0500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a plantation road leading to Thusharagiri waterfalls Kozhikode, roaring white water cascading through spice plantations of ginger, pepper, cardamom"
    },
    {
        "name": "Peruvannamuzhi Dam & Sanctuary, Kozhikode, Kerala, India",
        "lat": 11.5833, "lon": 75.8167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dam reservoir road in Peruvannamuzhi Kozhikode, Kuttiady river dam, crocodile rehabilitation park, bird sanctuary islands, dense green jungle"
    },
    {
        "name": "Kakkayam Dam Reservoir Valley, Kozhikode, Kerala, India",
        "lat": 11.5500, "lon": 75.9167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a narrow high-range dam road in Kakkayam Kozhikode, steep forest valley viewpoint, wild elephant habitat, waterfalls, mist over reservoir"
    },
    {
        "name": "Kuttiady Ghat Pass, Kozhikode, Kerala, India",
        "lat": 11.6667, "lon": 75.7500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain hairpin road Kuttiady Churam climbing towards Wayanad, spice traders, pepper vines, steep forested Western Ghats mountain curves"
    },
    {
        "name": "Iringal Sargalaya Crafts Village, Kozhikode, Kerala, India",
        "lat": 11.5667, "lon": 75.6167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage crafts village road in Iringal Kozhikode, Moorad river backwaters, Sargalaya artisan huts, Kunjali Marakkar naval museum"
    },

    # --- 13. KANNUR THEYYAM & MALABAR HAMLETS ---
    {
        "name": "Madayipara Laterite Hill, Kannur, Kerala, India",
        "lat": 12.0333, "lon": 75.2500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic road across Madayipara Kannur, sprawling red laterite rock plateau, seasonal blooming blue and yellow wildflowers, Madayi Kavu temple, sea view"
    },
    {
        "name": "Muzhappilangad Drive-In Beach, Kannur, Kerala, India",
        "lat": 11.7833, "lon": 75.4500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "driving directly on the firm wet sand along Muzhappilangad drive-in beach Kannur, 4km long beach, cars driving along breaking Arabian sea waves, coconut trees"
    },
    {
        "name": "Dharmadam Island & Estuary, Kannur, Kerala, India",
        "lat": 11.7667, "lon": 75.4667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal road overlooking Dharmadam green island in Kannur, Anjarakkandy river meeting Arabian sea, rocky shoreline, coconut palm trees, sea breeze"
    },
    {
        "name": "Kottiyoor Sacred Forest Temple, Kannur, Kerala, India",
        "lat": 11.8667, "lon": 75.8667,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a deep forest pilgrimage road in Kottiyoor Kannur, Bavali riverbed sacred Shiva temple Ikkare Kottiyoor, thatched palm leaf shrines in dense jungle"
    },
    {
        "name": "Alakode High-Range Hamlet, Kannur, Kerala, India",
        "lat": 12.1833, "lon": 75.4833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a hill village road in Alakode Kannur bordering Coorg, rubber plantations, black pepper vines, Christian settler church, misty hill slopes"
    },

    # --- 14. KASARAGOD NORTHERN BORDER HAMLETS ---
    {
        "name": "Ranipuram Shola Grasslands, Kasaragod, Kerala, India",
        "lat": 12.5000, "lon": 75.3500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a high altitude mountain road in Ranipuram Kasaragod, the Ooty of Kerala, expansive rolling green shola grasslands, elephant trekking path, cool mountain wind"
    },
    {
        "name": "Kottancheri Rainforest Hills, Kasaragod, Kerala, India",
        "lat": 12.3500, "lon": 75.4000,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a hill station road in Kottancheri Kasaragod, Western Ghats rainforest trekking reserve, Talacauvery wildlife buffer, misty green mountain peaks"
    },
    {
        "name": "Badiyadka Areca Nut Village, Kasaragod, Kerala, India",
        "lat": 12.6000, "lon": 75.0500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural agricultural road in Badiyadka Kasaragod, tall slender areca nut supari palm plantations, red laterite soil, multilingual Kannada and Malayalam signage"
    },
    {
        "name": "Manjeshwar Ananthapura Lake Temple, Kasaragod, Kerala, India",
        "lat": 12.7167, "lon": 74.8833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a temple road in Manjeshwar Kasaragod, ancient 9th-century Ananthapura Lake temple surrounded by green freshwater lake, cashew hills on border"
    },
    {
        "name": "Nileshwaram Tejaswini River, Kasaragod, Kerala, India",
        "lat": 12.2500, "lon": 75.1333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a cultural riverside road in Nileshwaram Kasaragod, Tejaswini river backwaters, Nileshwar Rajas Palace, Ayurveda yoga ashram, traditional houseboats"
    }
]

def add_kerala_villages():
    print(f"Current locations: {len(LOCATIONS)}")
    seen = {l["name"].strip().lower() for l in LOCATIONS}
    added = 0
    new_list = list(LOCATIONS)

    for item in KERALA_REMOTE_VILLAGES:
        n = item["name"].strip().lower()
        if n not in seen:
            seen.add(n)
            new_list.append(item)
            added += 1

    print(f"Added {added} brand-new remote Kerala villages!")
    print(f"Total unified locations: {len(new_list)}")

    output_code = ['# ==============================================================================',
                   '# Comprehensive Global, Pan-India, and Hyper-Local Micro-Regional Locations',
                   '# for StreetCLIP GeoGuessr AI (Unified Database)',
                   '# ==============================================================================\n',
                   'LOCATIONS = [']

    for loc in new_list:
        output_code.append('    {')
        output_code.append(f'        "name": {repr(loc["name"])},')
        output_code.append(f'        "lat": {loc["lat"]}, "lon": {loc["lon"]},')
        output_code.append(f'        "country": {repr(loc.get("country", "Unknown"))}, '
                           f'"region": {repr(loc.get("region", ""))}, '
                           f'"category": {repr(loc.get("category", "General"))}, '
                           f'"driving_side": {repr(loc.get("driving_side", "Unknown"))},')
        output_code.append(f'        "prompt": {repr(loc.get("prompt", ""))}')
        output_code.append('    },')

    output_code.append(']\n')

    with open("locations.py", "w", encoding="utf-8") as f:
        f.write("\n".join(output_code))

    print("Saved updated locations.py with dense remote Kerala villages!")

if __name__ == "__main__":
    add_kerala_villages()
