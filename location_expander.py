"""
Location Expander & Automated Training Engine
Provides curated candidate locations and auto-ingestion for StreetCLIP GeoGuessr.
Adds 20 new locations (10 Kerala, 5 India, 5 Global) and trains the model every time.
"""

import os
import copy
import random
import torch
from PIL import Image

# Curated pools of genuine geographic spots across Kerala, India, and the World

KERALA_CANDIDATE_POOL = [
    {
        "name": "Chellanam Coastal Village & Sea Wall, Ernakulam, Kerala, India",
        "lat": 9.8051, "lon": 76.2758, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal road in Chellanam Ernakulam Kerala, heavy tetrapod sea wall, fishing boats on shore, Arabian Sea waves, coconut groves, Malayalam boards"
    },
    {
        "name": "Thripunithura Hill Palace Heritage Grounds, Ernakulam, Kerala, India",
        "lat": 9.9535, "lon": 76.3639, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "traditional royal palace courtyard in Thripunithura Kerala, heritage Kerala architecture, sloping tiled roofs, lush royal gardens, laterite walls"
    },
    {
        "name": "Cheruthuruthy Kerala Kalamandalam, Thrissur, Kerala, India",
        "lat": 10.7483, "lon": 76.2803, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "cultural heritage grounds of Kerala Kalamandalam Cheruthuruthy on Bharathapuzha river bank, Kathakali motifs, wooden pillars, temple architecture"
    },
    {
        "name": "Guruvayur Temple Road & East Nada, Thrissur, Kerala, India",
        "lat": 10.5947, "lon": 76.0407, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a bustling temple approach street in Guruvayur Kerala, devotees in traditional mundu, brass lamps and flower stalls, traditional gopuram silhouette, Malayalam signboards"
    },
    {
        "name": "Chavakkad Beach & Coconut Fringe, Thrissur, Kerala, India",
        "lat": 10.5902, "lon": 76.0123, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a quiet sandy beach in Chavakkad Kerala where river meets Arabian Sea, fishing nets drying, tall coconut palms bending in coastal breeze, fishing skiffs"
    },
    {
        "name": "Thusharagiri Cascading Waterfalls, Kozhikode, Kerala, India",
        "lat": 11.4744, "lon": 76.0506, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a tropical rainforest waterfall in Thusharagiri Kozhikode Kerala, rocky river rapids, dense Western Ghats canopy, rubber and arecanut plantations"
    },
    {
        "name": "Kakkayam Dam Reservoir & Forest Edge, Kozhikode, Kerala, India",
        "lat": 11.5541, "lon": 75.9221, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a reservoir view road at Kakkayam Dam Kozhikode Kerala, steep mist-clad hills, dense evergreen forest, calm blue reservoir water, winding mountain road"
    },
    {
        "name": "Vadakara Sandbanks Beach & Moorad River Mouth, Kozhikode, Kerala, India",
        "lat": 11.5833, "lon": 75.5786, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a sandy peninsula beach where Moorad river meets Arabian Sea in Vadakara Kerala, coastal casuarina trees, local families, fishing boats, gentle surf"
    },
    {
        "name": "Teak Museum & Conolly Plot, Nilambur, Malappuram, Kerala, India",
        "lat": 11.2789, "lon": 76.2269, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the world's oldest teak plantation at Conolly Plot Nilambur Kerala, colossal straight teak tree trunks, Chaliyar river suspension bridge, lush Western Ghats greenery"
    },
    {
        "name": "Chamravattom Regulator Bridge & Bharathapuzha, Malappuram, Kerala, India",
        "lat": 10.8354, "lon": 75.9427, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a long scenic road bridge over Bharathapuzha river at Chamravattom Malappuram Kerala, broad riverbed, coconut palms lining the far bank, tropical sunny sky"
    },
    {
        "name": "Ponnani Historic Port & Biyyam Kayal, Malappuram, Kerala, India",
        "lat": 10.7725, "lon": 75.9255, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an ancient harbor street in Ponnani Malappuram Kerala, heritage wooden dhow docks, traditional mosques with tiered roofs, backwater lagoons and coconut groves"
    },
    {
        "name": "Malampuzha Dam Promenade & Rock Garden, Palakkad, Kerala, India",
        "lat": 10.8306, "lon": 76.6841, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "landscaped reservoir gardens below Malampuzha Dam Palakkad Kerala, ropeway cable cars, Yakshi sculpture, rugged Western Ghats mountain backdrop"
    },
    {
        "name": "Silent Valley Sairandhri Rainforest, Palakkad, Kerala, India",
        "lat": 11.0833, "lon": 76.4500, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "pristine tropical evergreen rainforest in Silent Valley Palakkad Kerala, Kunthi river canyon, dense biodiversity canopy, mountain watchtower, jungle trail"
    },
    {
        "name": "Dhoni Waterfalls & Forest Trek, Palakkad, Kerala, India",
        "lat": 10.8718, "lon": 76.6231, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a hillside forest trek path to Dhoni Waterfalls Palakkad Kerala, lush tropical woods, rocky cascade, mountain stream, Kerala forest department checkpost"
    },
    {
        "name": "Kollengode Village Paddy Plains & Seethargundu, Palakkad, Kerala, India",
        "lat": 10.6192, "lon": 76.6974, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic country road in Kollengode Palakkad Kerala, emerald green paddy fields stretching to towering misty Nelliampathy mountain cliffs, palm trees"
    },
    {
        "name": "Vattavada Organic Terraced Farms, Idukki, Kerala, India",
        "lat": 10.1834, "lon": 77.2625, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "terraced mountain vegetable farming in Vattavada Idukki Kerala, cool climate crops, eucalyptus and pine hills, rustic stone huts, Western Ghats highland road"
    },
    {
        "name": "Marayoor Jaggery Mills & Sandalwood Forest, Idukki, Kerala, India",
        "lat": 10.2811, "lon": 77.1606, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "sugarcane fields and traditional jaggery making sheds in Marayoor Idukki Kerala, natural sandalwood reserve, ancient dolmen stone structures on granite hillocks"
    },
    {
        "name": "Ramakkalmedu Windmill Hills, Idukki, Kerala, India",
        "lat": 9.8055, "lon": 77.2405, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "windy grassy ridge at Ramakkalmedu Idukki Kerala, giant power windmills rotating, panoramic view overlooking Tamil Nadu plains below, Kuravan Kurathi statue"
    },
    {
        "name": "Anchuruli Tunnel & Idukki Reservoir Shore, Idukki, Kerala, India",
        "lat": 9.7712, "lon": 77.0653, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dramatic circular water diversion tunnel opening at Anchuruli Idukki Kerala, vast reservoir waters, semi-submerged dead trees, green Western Ghats slopes"
    },
    {
        "name": "Calvary Mount Viewpoint, Idukki, Kerala, India",
        "lat": 9.8214, "lon": 76.9934, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "high mountain view overlooking Idukki Arch Dam reservoir from Calvary Mount, tea garden slopes, Christian cross pilgrim path, cool mountain breeze"
    },
    {
        "name": "Illikkal Kallu Mountain Peak & Bridge, Kottayam, Kerala, India",
        "lat": 9.7744, "lon": 76.8197, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a towering monolithic rock pinnacle at Illikkal Kallu Kottayam Kerala, narrow ridge path, deep misty valley drop-offs, cool breeze, Western Ghats clouds"
    },
    {
        "name": "Malarikkal Water Lily Fields, Kottayam, Kerala, India",
        "lat": 9.5639, "lon": 76.4912, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "vast flooded paddy fields carpeted in pink water lilies at Malarikkal Kottayam Kerala, early morning sunrise mist, wooden country canoes, coconut trees"
    },
    {
        "name": "Vaikom Mahadeva Temple & Lake Promenade, Kottayam, Kerala, India",
        "lat": 9.7547, "lon": 76.3956, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "heritage street around Vaikom Shiva temple Kerala, classical Kerala temple courtyard, copper-roofed sreekovil, nearby Vembanad lake ferry jetty, tranquil setting"
    },
    {
        "name": "Pathiramanal Island Nature Sanctuary, Alappuzha, Kerala, India",
        "lat": 9.6167, "lon": 76.3833, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an isolated green bird sanctuary island in Vembanad Lake Alappuzha Kerala, dense mangrove paths, migratory water birds, houseboats anchored nearby"
    },
    {
        "name": "Marari Fishermen Beach & Village, Alappuzha, Kerala, India",
        "lat": 9.6006, "lon": 76.2974, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a pristine fishing village beach in Marari Alappuzha Kerala, coconut thatch cottages, traditional wooden catamarans on white sand, gentle surf, quiet rural coast"
    },
    {
        "name": "Gavi Dense Eco-Tourism Rainforest, Pathanamthitta, Kerala, India",
        "lat": 9.4389, "lon": 77.1642, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an untouched cardamom and tropical rainforest road in Gavi Pathanamthitta Kerala, misty valleys, wild elephant corridors, forest department jeeps, green jungle"
    },
    {
        "name": "Konni Elephant Reserve & Teak Woods, Pathanamthitta, Kerala, India",
        "lat": 9.2431, "lon": 76.8486, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "historic wooden elephant kraal at Konni Pathanamthitta Kerala, tall teak forest trees, Achankovil river nearby, rural Kerala township, tranquil forest sanctuary"
    },
    {
        "name": "Jatayu Earth Center & Giant Rock Sculpture, Kollam, Kerala, India",
        "lat": 8.8683, "lon": 76.8672, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a massive bird sculpture atop a rocky hill at Jatayu Earth Center Chadayamangalam Kollam Kerala, cable car gondola ropeway, panoramic views of southern Kerala plains"
    },
    {
        "name": "Thenmala Shendurney Eco-Tourism Dam, Kollam, Kerala, India",
        "lat": 8.9567, "lon": 77.0642, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "India's first planned eco-tourism site at Thenmala Kollam Kerala, Kallada river dam, suspension boardwalk bridge, dense tropical forest hills, winding highway"
    },
    {
        "name": "Ponmudi Golden Valley & 22 Hairpin Bends, Thiruvananthapuram, Kerala, India",
        "lat": 8.7601, "lon": 77.1147, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a twisting mountain hairpin road climbing to Ponmudi hill station Thiruvananthapuram Kerala, thick fog, Golden Valley river rapids, tea estates, Western Ghats"
    },
    {
        "name": "Poovar Golden Sand Estuary & Mangroves, Thiruvananthapuram, Kerala, India",
        "lat": 8.3183, "lon": 77.0683, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a unique coastal sand spit where Neyyar river meets Arabian Sea at Poovar Kerala, floating wooden cottages, mangrove canal boat tour, golden sand beach"
    },
    {
        "name": "Banasura Sagar Earthen Dam, Wayanad, Kerala, India",
        "lat": 11.6692, "lon": 75.9575, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "Asia's largest earthen dam at Banasura Sagar Wayanad Kerala, scenic reservoir islands against rugged Banasura mountain peaks, speedboats, green lawns"
    },
    {
        "name": "Thirunelly Ancient Mountain Temple & Papanasini, Wayanad, Kerala, India",
        "lat": 11.9022, "lon": 75.9986, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "an ancient stone pillar temple nestled in Brahmagiri hills at Thirunelly Wayanad Kerala, holy Papanasini stream flowing over granite boulders, deep jungle surroundings"
    },
    {
        "name": "Edakkal Caves & Prehistoric Petroglyphs, Wayanad, Kerala, India",
        "lat": 11.6289, "lon": 76.2347, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "steep stone stairs climbing Ambukuthi Hills to Edakkal Caves Wayanad Kerala, giant split rock shelter, ancient Neolithic petroglyphs, sweeping valley vistas"
    },
    {
        "name": "Muzhappilangad Longest Drive-in Beach, Kannur, Kerala, India",
        "lat": 11.7925, "lon": 75.4497, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "cars driving along firm golden sand directly at water edge on Muzhappilangad drive-in beach Kannur Kerala, gentle sea waves, black rocks, Malabar coast"
    },
    {
        "name": "Paithalmala Highland Ridge & Observatory, Kannur, Kerala, India",
        "lat": 12.1644, "lon": 75.5683, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a grassy highland ridge trek at Paithalmala Kannur Kerala, cool mountain winds, dense Kodagu border shola forests, observatory tower perched on hilltop"
    },
    {
        "name": "Ranipuram Shola Grasslands & Peak, Kasaragod, Kerala, India",
        "lat": 12.5186, "lon": 75.3528, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "rolling green montane grasslands and shola woods at Ranipuram Kasaragod Kerala, rocky trekking trails, misty peaks, cool highland climate"
    },
    {
        "name": "Ananthapura Lake Temple, Kasaragod, Kerala, India",
        "lat": 12.5856, "lon": 74.9814, "country": "India", "region": "Kerala",
        "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the only lake temple in Kerala situated in the middle of a rectangular pond at Ananthapura Kasaragod, traditional Kerala-Tulunadu architecture, tranquil green surroundings"
    }
]

INDIA_CANDIDATE_POOL = [
    {
        "name": "Hampi UNESCO Stone Chariot & Ruins, Vijayanagara, Karnataka, India",
        "lat": 15.3350, "lon": 76.4600, "country": "India", "region": "Karnataka",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "the iconic stone chariot in Vijaya Vittala temple complex Hampi Karnataka, boulder-strewn arid landscape, carved granite pillars, Tungabhadra river valley"
    },
    {
        "name": "Coorg Abbey Falls & Coffee Plantations, Kodagu, Karnataka, India",
        "lat": 12.4542, "lon": 75.7197, "country": "India", "region": "Karnataka",
        "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a gushing white waterfall surrounded by lush coffee estates and pepper vines in Abbey Falls Coorg Karnataka, hanging suspension bridge, humid Western Ghats"
    },
    {
        "name": "Gokarna Om Beach & Rocky Coast, Karnataka, India",
        "lat": 14.5167, "lon": 74.3167, "country": "India", "region": "Karnataka",
        "category": "India - Coastal", "driving_side": "Left",
        "prompt": "an Om-shaped sandy coastal bay framed by rugged black laterite rocks in Gokarna Karnataka, Arabian Sea waves, beach shacks, coconut palms"
    },
    {
        "name": "Mysore Amba Vilas Palace & Heritage Gates, Karnataka, India",
        "lat": 12.3051, "lon": 76.6551, "country": "India", "region": "Karnataka",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "grand Indo-Saracenic royal palace of Mysore Karnataka, ornate domes and arches, manicured palace lawns, heritage stone gateway, heritage horse tongas"
    },
    {
        "name": "Mahabalipuram Shore Temple & Pancha Rathas, Tamil Nadu, India",
        "lat": 12.6167, "lon": 80.1925, "country": "India", "region": "Tamil Nadu",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "ancient 8th-century monolithic rock-cut shore temple on Bay of Bengal at Mahabalipuram Tamil Nadu, granite carvings weathered by sea spray, casuarina trees"
    },
    {
        "name": "Dhanushkodi Ghost Town & Ram Setu Beach, Tamil Nadu, India",
        "lat": 9.1764, "lon": 79.4144, "country": "India", "region": "Tamil Nadu",
        "category": "India - Coastal", "driving_side": "Left",
        "prompt": "abandoned church ruins on white sand spit at Dhanushkodi Tamil Nadu, turquoise ocean meeting shallow gulf, lone asphalt road to land's end"
    },
    {
        "name": "Meenakshi Amman Temple Gopuram Towers, Madurai, Tamil Nadu, India",
        "lat": 9.9195, "lon": 78.1193, "country": "India", "region": "Tamil Nadu",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "towering multi-colored sculpted gopuram towers of Meenakshi temple in Madurai Tamil Nadu, bustling market street with flower sellers, auto rickshaws, Tamil boards"
    },
    {
        "name": "Charminar & Laad Bazaar, Hyderabad, Telangana, India",
        "lat": 17.3616, "lon": 78.4747, "country": "India", "region": "Telangana",
        "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "the four-minaret monument Charminar in old Hyderabad Telangana, bustling Laad Bazaar with lacquer bangle shops, street vendors, historic stucco architecture"
    },
    {
        "name": "Marine Drive Queen's Necklace Promenade, Mumbai, Maharashtra, India",
        "lat": 18.9438, "lon": 72.8232, "country": "India", "region": "Maharashtra",
        "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "curving seaside boulevard along Back Bay in Mumbai Maharashtra, Art Deco apartment facades, concrete tetrapods along sea wall, yellow-black Premier Padmini cabs"
    },
    {
        "name": "Ajanta Caves UNESCO Buddhist Rock Frescoes, Maharashtra, India",
        "lat": 20.5519, "lon": 75.7033, "country": "India", "region": "Maharashtra",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "horseshoe-shaped cliff gorge of Waghora river with ancient rock-cut Buddhist monastery caves at Ajanta Maharashtra, stone colonnades, arid Deccan plateau scenery"
    },
    {
        "name": "Dudhsagar Four-Tier Waterfalls & Railway Bridge, Goa, India",
        "lat": 15.3144, "lon": 74.3144, "country": "India", "region": "Goa",
        "category": "India - Nature", "driving_side": "Left",
        "prompt": "a massive white tiered waterfall with an arched railway viaduct bridge crossing right in front in Dudhsagar Goa, lush green Western Ghats jungle canopy"
    },
    {
        "name": "Great Rann of Kutch White Salt Desert, Gujarat, India",
        "lat": 23.8333, "lon": 69.8333, "country": "India", "region": "Gujarat",
        "category": "India - Nature", "driving_side": "Left",
        "prompt": "an endless expanse of blinding white crystallized salt desert under open blue sky in Rann of Kutch Gujarat, Kutchi bhunga mud huts, decorated camels, desert horizon"
    },
    {
        "name": "Hawa Mahal Palace of Winds, Jaipur, Rajasthan, India",
        "lat": 26.9239, "lon": 75.8267, "country": "India", "region": "Rajasthan",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "iconic pink and red honeycomb sandstone facade of Hawa Mahal in Jaipur Rajasthan, 953 ornate jharokha windows, bustling old city market street, auto rickshaws"
    },
    {
        "name": "Udaipur Lake Pichola & City Palace Waterfront, Rajasthan, India",
        "lat": 24.5764, "lon": 73.6835, "country": "India", "region": "Rajasthan",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "magnificent granite and marble City Palace rising above the waters of Lake Pichola Udaipur Rajasthan, traditional heritage boats, white ghats, Aravalli hills"
    },
    {
        "name": "Jodhpur Mehrangarh Fort Blue City Panorama, Rajasthan, India",
        "lat": 26.2978, "lon": 73.0185, "country": "India", "region": "Rajasthan",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "a view of the sea of blue-painted houses in Jodhpur Rajasthan spreading below the colossal red sandstone ramparts of Mehrangarh Fort, Thar desert sun"
    },
    {
        "name": "Varanasi Dashashwamedh Ghat & River Ganga, Uttar Pradesh, India",
        "lat": 25.3076, "lon": 83.0107, "country": "India", "region": "Uttar Pradesh",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "stone steps leading down to the sacred river Ganga at Dashashwamedh Ghat Varanasi Uttar Pradesh, wooden row boats, brass arti lamps, sadhus, ancient temples"
    },
    {
        "name": "Golden Temple Harmandir Sahib & Pool of Nectar, Amritsar, Punjab, India",
        "lat": 31.6200, "lon": 74.8765, "country": "India", "region": "Punjab",
        "category": "India - Heritage", "driving_side": "Left",
        "prompt": "the shimmering gold-plated sanctum of Harmandir Sahib reflected in the holy Amrit Sarovar water pool Amritsar Punjab, white marble parikrama walkway, Sikh pilgrims"
    },
    {
        "name": "Spiti Valley Key Gompa Monastery & Kaza, Himachal Pradesh, India",
        "lat": 32.2989, "lon": 78.0125, "country": "India", "region": "Himachal Pradesh",
        "category": "India - Mountain", "driving_side": "Left",
        "prompt": "a thousand-year-old Tibetan Buddhist monastery perched atop a conical barren hill in Spiti Valley Himachal Pradesh, snow-capped Trans-Himalayan peaks, mud brick cells"
    },
    {
        "name": "Pangong Tso High Altitude Blue Lake, Ladakh, India",
        "lat": 33.7595, "lon": 78.6586, "country": "India", "region": "Ladakh",
        "category": "India - Mountain", "driving_side": "Left",
        "prompt": "deep turquoise and azure waters of Pangong Tso lake at 4,250m altitude in Ladakh, barren arid Himalayan mountain ranges, stony shoreline, prayer flags"
    },
    {
        "name": "Living Root Bridges & Rain Canopy, Cherrapunji, Meghalaya, India",
        "lat": 25.2783, "lon": 91.7325, "country": "India", "region": "Meghalaya",
        "category": "India - Nature", "driving_side": "Left",
        "prompt": "a bio-engineered double-decker living root bridge woven across a pristine crystal stream in Nongriat Meghalaya, lush monsoon jungle, giant boulders, Khasi hills"
    }
]

GLOBAL_CANDIDATE_POOL = [
    {
        "name": "Shibuya Scramble Crossing & Neon Towers, Tokyo, Japan",
        "lat": 35.6595, "lon": 139.7004, "country": "Japan", "region": "Kanto",
        "category": "Global", "driving_side": "Left",
        "prompt": "massive pedestrian scramble crossing outside Shibuya Station Tokyo Japan, towering giant LED video screens, neon Japanese signs, bustling metropolis crosswalk"
    },
    {
        "name": "Fushimi Inari Taisha Thousand Torii Gates, Kyoto, Japan",
        "lat": 34.9671, "lon": 135.7727, "country": "Japan", "region": "Kansai",
        "category": "Global", "driving_side": "Left",
        "prompt": "winding uphill path under thousands of bright vermillion red wooden torii gates at Fushimi Inari shrine Kyoto Japan, lush green cedar forest, stone fox statues"
    },
    {
        "name": "Lake Kawaguchiko Mount Fuji Reflection, Yamanashi, Japan",
        "lat": 35.5171, "lon": 138.7518, "country": "Japan", "region": "Chubu",
        "category": "Global", "driving_side": "Left",
        "prompt": "snow-capped symmetrical volcanic peak of Mount Fuji rising majestically over calm blue waters of Lake Kawaguchiko Japan, cherry blossoms or autumn maples"
    },
    {
        "name": "Marina Bay Sands & Gardens by the Bay, Singapore",
        "lat": 1.2838, "lon": 103.8591, "country": "Singapore", "region": "Central",
        "category": "Global", "driving_side": "Left",
        "prompt": "iconic three-tower Marina Bay Sands hotel with surfboard SkyPark roof, futuristic Supertree grove, pristine clean tropical waterfront promenade Singapore"
    },
    {
        "name": "Petronas Twin Towers & Suria KLCC, Kuala Lumpur, Malaysia",
        "lat": 3.1578, "lon": 101.7119, "country": "Malaysia", "region": "Federal Territory",
        "category": "Global", "driving_side": "Left",
        "prompt": "soaring stainless steel and glass Islamic geometric architecture of Petronas Twin Towers Kuala Lumpur Malaysia, two-tier skybridge, KLCC park fountains"
    },
    {
        "name": "Angkor Wat Ancient Khmer Temple Complex, Siem Reap, Cambodia",
        "lat": 13.4125, "lon": 103.8670, "country": "Cambodia", "region": "Siem Reap",
        "category": "Global", "driving_side": "Right",
        "prompt": "monumental sandstone lotus-bud towers of Angkor Wat Cambodia reflected in water lily moat, ancient stone galleries with bas-relief carvings, tropical palms"
    },
    {
        "name": "Ha Long Bay Limestone Karsts & Emerald Waters, Vietnam",
        "lat": 20.9101, "lon": 107.1839, "country": "Vietnam", "region": "Quang Ninh",
        "category": "Global", "driving_side": "Right",
        "prompt": "thousands of towering limestone pillars and karst islets rising from tranquil emerald green waters of Ha Long Bay Vietnam, traditional wooden junk boats"
    },
    {
        "name": "Burj Khalifa & Downtown Boardwalk, Dubai, United Arab Emirates",
        "lat": 25.1972, "lon": 55.2744, "country": "United Arab Emirates", "region": "Dubai",
        "category": "Global", "driving_side": "Right",
        "prompt": "world's tallest skyscraper Burj Khalifa piercing desert blue sky in Dubai UAE, turquoise artificial lake, Dubai Fountain boardwalk, modern desert architecture"
    },
    {
        "name": "Petra Treasury Al-Khazneh Sandstone Canyon, Ma'an, Jordan",
        "lat": 30.3285, "lon": 35.4444, "country": "Jordan", "region": "Ma'an",
        "category": "Global", "driving_side": "Right",
        "prompt": "spectacular classical Hellenistic facade carved directly into rose-red sandstone cliff face framed by the narrow Siq canyon gorge at Petra Jordan, bedouin camels"
    },
    {
        "name": "Table Mountain & Camps Bay Coastline, Cape Town, South Africa",
        "lat": -33.9573, "lon": 18.3776, "country": "South Africa", "region": "Western Cape",
        "category": "Global", "driving_side": "Left",
        "prompt": "flat-topped Table Mountain covered in white cloud tablecloth rising dramatically behind turquoise waters and palm-lined white sand beach of Camps Bay Cape Town"
    },
    {
        "name": "Colosseum & Roman Forum Historic Ruins, Rome, Italy",
        "lat": 41.8902, "lon": 12.4922, "country": "Italy", "region": "Lazio",
        "category": "Global", "driving_side": "Right",
        "prompt": "ancient travertine stone arches and tiers of the Flavian Amphitheatre Colosseum in Rome Italy, stone pine umbrella trees, cobblestone streets, sunny Italian sky"
    },
    {
        "name": "Venice Grand Canal & Rialto Bridge, Veneto, Italy",
        "lat": 45.4380, "lon": 12.3359, "country": "Italy", "region": "Veneto",
        "category": "Global", "driving_side": "Right",
        "prompt": "wide curving Grand Canal in Venice Italy lined with ornate Renaissance and Venetian Gothic palazzos, black wooden gondolas, white stone arched Rialto Bridge"
    },
    {
        "name": "Sagrada Familia Basilica & Eixample Avenues, Barcelona, Spain",
        "lat": 41.4036, "lon": 2.1744, "country": "Spain", "region": "Catalonia",
        "category": "Global", "driving_side": "Right",
        "prompt": "soaring organic Art Nouveau towers of Antoni Gaudi's Sagrada Familia basilica in Barcelona Spain, detailed Nativity facade, sunny Catalan city avenue"
    },
    {
        "name": "Santorini Oia Whitewashed Caldera Village, Cyclades, Greece",
        "lat": 36.4618, "lon": 25.3753, "country": "Greece", "region": "South Aegean",
        "category": "Global", "driving_side": "Right",
        "prompt": "dazzling whitewashed cliffside cave houses and vibrant cobalt blue church domes overlooking Aegean Sea caldera in Oia Santorini Greece, pink bougainvillea"
    },
    {
        "name": "Neuschwanstein Fairy Tale Castle & Bavarian Alps, Germany",
        "lat": 47.5576, "lon": 10.7498, "country": "Germany", "region": "Bavaria",
        "category": "Global", "driving_side": "Right",
        "prompt": "romantic 19th-century white limestone castle with pointed spires perched on a steep rugged forested crag in the Bavarian Alps Hohenschwangau Germany"
    },
    {
        "name": "Amsterdam Keizersgracht Canal & Bicycle Bridges, Netherlands",
        "lat": 52.3667, "lon": 4.8833, "country": "Netherlands", "region": "North Holland",
        "category": "Global", "driving_side": "Right",
        "prompt": "serene tree-lined canal street along Keizersgracht in Amsterdam Netherlands, narrow brick gabled canal houses, arched stone bridge with parked Dutch bicycles"
    },
    {
        "name": "Tower Bridge & River Thames Promenade, London, United Kingdom",
        "lat": 51.5055, "lon": -0.0754, "country": "United Kingdom", "region": "England",
        "category": "Global", "driving_side": "Left",
        "prompt": "iconic Victorian Gothic twin stone suspension towers of Tower Bridge over the River Thames London England, red double-decker bus crossing, grey British sky"
    },
    {
        "name": "Edinburgh Castle & Royal Mile Cobblestones, Scotland, United Kingdom",
        "lat": 55.9486, "lon": -3.1999, "country": "United Kingdom", "region": "Scotland",
        "category": "Global", "driving_side": "Left",
        "prompt": "historic stone fortress of Edinburgh Castle perched high upon the volcanic Castle Rock overlooking the cobblestone Royal Mile Scotland, stone tenements"
    },
    {
        "name": "Times Square Broadway Neon Billboards, New York City, United States",
        "lat": 40.7580, "lon": -73.9855, "country": "United States", "region": "New York",
        "category": "Global", "driving_side": "Right",
        "prompt": "vibrant street canyon in Times Square Manhattan New York City, towering high-rise digital LED billboards, yellow taxicabs, Broadway theatre district crowds"
    },
    {
        "name": "Sydney Opera House & Harbour Waterfront, New South Wales, Australia",
        "lat": -33.8568, "lon": 151.2153, "country": "Australia", "region": "New South Wales",
        "category": "Global", "driving_side": "Left",
        "prompt": "distinctive white interlocking sail roof shells of Sydney Opera House at Bennelong Point Sydney Australia, blue harbour waters, Sydney Harbour Bridge nearby"
    }
]

def pick_next_20_locations(existing_locations):
    """
    Selects exactly 20 new locations:
    - 10 Kerala locations
    - 5 India locations
    - 5 Global locations
    ensuring none are already present in existing_locations.
    """
    existing_names = set(l["name"].strip().lower() for l in existing_locations)

    # 1. Filter Kerala candidates
    kerala_avail = [l for l in KERALA_CANDIDATE_POOL if l["name"].strip().lower() not in existing_names]
    # 2. Filter India candidates
    india_avail = [l for l in INDIA_CANDIDATE_POOL if l["name"].strip().lower() not in existing_names]
    # 3. Filter Global candidates
    global_avail = [l for l in GLOBAL_CANDIDATE_POOL if l["name"].strip().lower() not in existing_names]

    # Dynamic fallback generator if candidate pools are ever depleted
    epoch_seed = len(existing_locations) + random.randint(100, 999)

    selected_kerala = []
    for cand in kerala_avail[:10]:
        selected_kerala.append(cand)
    while len(selected_kerala) < 10:
        idx = len(selected_kerala) + 1
        name = f"Kerala Scenic Route Micro-Sector #{idx} (Sector-{epoch_seed}), Kerala, India"
        lat = round(9.0 + (random.random() * 3.2), 4)
        lon = round(75.5 + (random.random() * 1.5), 4)
        selected_kerala.append({
            "name": name,
            "lat": lat, "lon": lon,
            "country": "India", "region": "Kerala",
            "category": "Kerala - Micro-Region", "driving_side": "Left",
            "prompt": f"a tropical street in Kerala India, roadside coconut trees, red laterite soil, Malayalam signage, KSRTC bus, tropical monsoonal vegetation"
        })

    selected_india = []
    for cand in india_avail[:5]:
        selected_india.append(cand)
    while len(selected_india) < 5:
        idx = len(selected_india) + 1
        name = f"Indian Cultural Hub & Transit Zone #{idx} (Hub-{epoch_seed}), India"
        lat = round(12.0 + (random.random() * 18.0), 4)
        lon = round(72.0 + (random.random() * 16.0), 4)
        selected_india.append({
            "name": name,
            "lat": lat, "lon": lon,
            "country": "India", "region": "Central",
            "category": "India - City/Hub", "driving_side": "Left",
            "prompt": f"a street in India, heritage architectural facades, roadside marketplace, auto rickshaws, vibrant signs in Devanagari or regional script"
        })

    selected_global = []
    for cand in global_avail[:5]:
        selected_global.append(cand)
    while len(selected_global) < 5:
        idx = len(selected_global) + 1
        name = f"Global World Landmark Sector #{idx} (Landmark-{epoch_seed})"
        lat = round(-40.0 + (random.random() * 95.0), 4)
        lon = round(-120.0 + (random.random() * 240.0), 4)
        selected_global.append({
            "name": name,
            "lat": lat, "lon": lon,
            "country": "Global", "region": "International",
            "category": "Global", "driving_side": "Right",
            "prompt": f"an iconic international streetscape, distinctive urban architecture, street vehicles, asphalt roadway, global travel destination"
        })

    return selected_kerala + selected_india + selected_global


def expand_database_and_train_20(processor, model, cache_file, adapter_file, epochs=30):
    """
    1. Loads existing cache.
    2. Selects 20 new locations (10 Kerala, 5 India, 5 Global).
    3. Computes StreetCLIP text embeddings.
    4. Saves to cache_file and appends to locations.py.
    5. Runs automated training on the Residual Adapter.
    Returns: (new_20_locations, acc_init, acc_final, elapsed_sec)
    """
    import time
    t0 = time.time()

    cache_data = torch.load(cache_file, weights_only=False)
    existing_embs = cache_data["embeddings"]
    existing_locs = cache_data["locations"]

    new_20 = pick_next_20_locations(existing_locs)

    # Compute embeddings for all 20 locations using the ensemble approach
    new_vectors = []
    for loc in new_20:
        p_vis = loc["prompt"]
        p_can = f"a street view photo in {loc['name']}"
        p_geo = f"a photo taken in {loc['name']}, {loc.get('country', '')}"

        with torch.no_grad():
            t_in = processor(
                text=[p_vis, p_can, p_geo],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=77
            )
            t_out = model.get_text_features(input_ids=t_in["input_ids"])
            t_raw = t_out.pooler_output if hasattr(t_out, "pooler_output") else t_out
            t_norm = t_raw / t_raw.norm(dim=-1, keepdim=True)
            comb = 0.50 * t_norm[0:1] + 0.30 * t_norm[1:2] + 0.20 * t_norm[2:3]
            comb_norm = (comb / comb.norm(dim=-1, keepdim=True)).cpu()
            new_vectors.append(comb_norm)

    new_embs = torch.cat(new_vectors, dim=0)

    # Append to existing
    updated_embs = torch.cat([existing_embs, new_embs], dim=0)
    updated_locs = existing_locs + new_20

    # Save to embeddings_cache.pt
    torch.save({"embeddings": updated_embs, "locations": updated_locs}, cache_file)

    # Also append to locations.py so python source stays updated
    try:
        if os.path.exists("locations.py"):
            with open("locations.py", "r", encoding="utf-8") as f:
                loc_content = f.read()
            # find last ']'
            last_bracket = loc_content.rfind("]")
            if last_bracket != -1:
                import pprint
                lines_to_add = "\n"
                for item in new_20:
                    lines_to_add += "    " + pprint.pformat(item) + ",\n"
                new_loc_content = loc_content[:last_bracket] + lines_to_add + loc_content[last_bracket:]
                with open("locations.py", "w", encoding="utf-8") as f:
                    f.write(new_loc_content)
    except Exception as e:
        print(f"Warning: could not update locations.py directly: {e}")

    # Now train Residual Adapter
    import glob
    from torch import nn
    from ResidualAdapter import ResidualAdapter

    extensions = ("*.jpg", "*.jpeg", "*.png")
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join("Imgs", ext)))
    image_paths = [p for p in image_paths if not os.path.basename(p).startswith("test")]

    feats_list = []
    targets_list = []

    for path in image_paths:
        fname = os.path.basename(path)
        base = os.path.splitext(fname)[0]
        toks = [t.lower() for t in base.replace("-", "_").split("_") if t]
        best_idx, best_score = 0, 0
        for idx, loc in enumerate(updated_locs):
            score = sum(1 for tok in toks if tok in loc["name"].lower())
            if score > best_score:
                best_score = score
                best_idx = idx

        try:
            im = Image.open(path).convert("RGB")
            inp = processor(images=im, return_tensors="pt")
            with torch.no_grad():
                out = model.get_image_features(pixel_values=inp["pixel_values"])
                raw = out.pooler_output if hasattr(out, "pooler_output") else out
                norm = raw / raw.norm(dim=-1, keepdim=True)
                feats_list.append(norm.squeeze(0))
                targets_list.append(best_idx)
        except Exception:
            continue

    if feats_list:
        X = torch.stack(feats_list)
        Y = torch.tensor(targets_list, dtype=torch.long)

        new_adapter = ResidualAdapter(dim=X.shape[1], bottleneck=256, alpha=0.85)
        optimizer = torch.optim.AdamW(new_adapter.parameters(), lr=2e-3, weight_decay=1e-4)
        loss_fn = nn.CrossEntropyLoss()

        new_adapter.eval()
        with torch.no_grad():
            out_init = new_adapter(X)
            acc_init = (torch.argmax((out_init @ updated_embs.T) * 35.0, dim=-1) == Y).float().mean().item() * 100.0

        new_adapter.train()
        for _ in range(epochs):
            optimizer.zero_grad()
            out_feats = new_adapter(X)
            loss = loss_fn((out_feats @ updated_embs.T) * 35.0, Y)
            loss.backward()
            optimizer.step()

        new_adapter.eval()
        with torch.no_grad():
            out_final = new_adapter(X)
            acc_final = (torch.argmax((out_final @ updated_embs.T) * 35.0, dim=-1) == Y).float().mean().item() * 100.0

        torch.save(new_adapter.state_dict(), adapter_file)
    else:
        acc_init, acc_final = 0.0, 0.0

    elapsed = time.time() - t0
    return new_20, acc_init, acc_final, elapsed
