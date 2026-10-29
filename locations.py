# ==============================================================================
# Comprehensive Global, Pan-India, and Hyper-Local Micro-Regional Locations
# for StreetCLIP GeoGuessr AI
#
# Each location contains:
# - name: Canonical human-readable place name
# - lat, lon: Accurate GPS coordinates
# - country: Country name
# - region: State / Province / Territory
# - category: "Global", "India - State/UT", "India - City/Hub", or "Kerala - Micro-Region"
# - driving_side: "Left" or "Right"
# - prompt: Dense GeoGuessr visual features (bollards, road lines, soil, vegetation,
#           architecture, scripts, vehicles, topography)
# ==============================================================================

LOCATIONS = [
    # ==========================================================================
    # 1. KERALA MICRO-REGIONS & VILLAGES (ALL 14 DISTRICTS)
    # ==========================================================================
    # --- Alappuzha & Central Travancore ---
    {
        "name": "Chengannur, Alappuzha, Kerala, India",
        "lat": 9.3175, "lon": 76.6114,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a street photo in Chengannur Kerala, red soil, laterite stone walls, railway town, KSRTC red bus, Malayalam shop signboards, tropical coconut trees"
    },
    {
        "name": "Aranmula, Pathanamthitta, Kerala, India",
        "lat": 9.3333, "lon": 76.6833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a village road in Aranmula Kerala, Pamba river bank, heritage wooden tharavadu houses, temple architecture, lush green paddy fields, Malayalam boards"
    },
    {
        "name": "Kuttanad, Alappuzha, Kerala, India",
        "lat": 9.4214, "lon": 76.4357,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural landscape in Kuttanad Kerala, narrow canal water roads, traditional houseboats, vast submerged green paddy fields below sea level, coconut palm groves"
    },
    {
        "name": "Alappuzha Town & Beach, Kerala, India",
        "lat": 9.4981, "lon": 76.3388,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal street in Alleppey Alappuzha Kerala, old sea bridge pier, canals crisscrossing town, fish stalls, palm trees, humid coastal atmosphere"
    },
    {
        "name": "Tiruvalla, Pathanamthitta, Kerala, India",
        "lat": 9.3835, "lon": 76.5741,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a commercial street in Tiruvalla Kerala, multi-storey concrete commercial buildings, busy town junction, NRI bungalows, Malayalam signboards"
    },
    {
        "name": "Mavelikkara, Alappuzha, Kerala, India",
        "lat": 9.2435, "lon": 76.5497,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a traditional town junction in Mavelikkara Kerala, heritage palace grounds, laterite compounds, Chettikulangara temple roads, paved state highway"
    },
    {
        "name": "Champakulam, Alappuzha, Kerala, India",
        "lat": 9.4000, "lon": 76.4167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a riverbank village in Champakulam Kerala, ancient church on the water, snake boat racing sheds, quiet canal walkways, lush water hyacinth"
    },
    {
        "name": "Haripad, Alappuzha, Kerala, India",
        "lat": 9.2882, "lon": 76.4622,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a town road in Haripad Kerala, Subrahmanya Swamy temple surroundings, coastal plain highway, auto rickshaws, coconut groves"
    },

    # --- Pathanamthitta & Kollam ---
    {
        "name": "Kozhencherry, Pathanamthitta, Kerala, India",
        "lat": 9.3414, "lon": 76.7126,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a town bridge road over Pamba river in Kozhencherry Kerala, Maramon convention sandbanks, hilly riverbanks, rubber plantations"
    },
    {
        "name": "Konni, Pathanamthitta, Kerala, India",
        "lat": 9.2432, "lon": 76.8504,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a forest fringe road in Konni Kerala, elephant training kraal, dense teak and rubber plantations, Achankovil river forest road"
    },
    {
        "name": "Ranni, Pathanamthitta, Kerala, India",
        "lat": 9.3811, "lon": 76.7869,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a hilly village road in Ranni Kerala, undulating rubber tree hills, winding tarmac roads, private estate gates, Christian churches"
    },
    {
        "name": "Munroe Island, Kollam, Kerala, India",
        "lat": 8.9889, "lon": 76.6111,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a narrow village waterway in Munroe Island Kollam Kerala, coir retting pools, mangrove canals, small concrete footbridges, country boats"
    },
    {
        "name": "Kollam Port & Beach, Kerala, India",
        "lat": 8.8932, "lon": 76.6141,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal street in Kollam Kerala, Tangasseri lighthouse, fishing harbor, cashew processing town, Arabian sea coastal road"
    },
    {
        "name": "Punalur, Kollam, Kerala, India",
        "lat": 9.0192, "lon": 76.9248,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a valley road in Punalur Kerala, British heritage suspension bridge across Kallada river, paper mill town, Western Ghat foothills"
    },

    # --- Thiruvananthapuram ---
    {
        "name": "East Fort, Thiruvananthapuram, Kerala, India",
        "lat": 8.4833, "lon": 76.9458,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street in East Fort Thiruvananthapuram, Padmanabhaswamy temple gateway, heritage stone fort arches, white and blue city buses"
    },
    {
        "name": "Kovalam Beach, Thiruvananthapuram, Kerala, India",
        "lat": 8.4004, "lon": 76.9787,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal road in Kovalam Kerala, red-and-white striped lighthouse, crescent rocky beach, beachside cafes, coconut palms"
    },
    {
        "name": "Varkala Cliff, Thiruvananthapuram, Kerala, India",
        "lat": 8.7379, "lon": 76.7163,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a cliffside path in Varkala Kerala, dramatic red laterite cliffs over the Arabian Sea, bohemian cafes, coconut palms, paved walkway"
    },
    {
        "name": "Ponmudi, Thiruvananthapuram, Kerala, India",
        "lat": 8.7600, "lon": 77.1167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a winding hairpin hill road in Ponmudi Kerala, misty Western Ghat peaks, tea plantations, golden grass meadows, cooler mountain air"
    },

    # --- Kottayam & Idukki ---
    {
        "name": "Kumarakom, Kottayam, Kerala, India",
        "lat": 9.6175, "lon": 76.4300,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a lakeside resort road in Kumarakom Kerala, Vembanad lake shore, bird sanctuary canals, luxury houseboats, mangrove trees"
    },
    {
        "name": "Pala, Kottayam, Kerala, India",
        "lat": 9.7107, "lon": 76.6848,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a street in Pala town Kottayam, undulating rubber estates, Syrian Catholic churches, steep roads, Malayalam street signs"
    },
    {
        "name": "Erattupetta, Kottayam, Kerala, India",
        "lat": 9.6942, "lon": 76.7836,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a foothill town in Erattupetta Kerala, Meenachil river, timber merchants, rubber tree plantations, high range misty hilly terrain"
    },
    {
        "name": "Ilaveezhapoonchira, Kottayam, Kerala, India",
        "lat": 9.7892, "lon": 76.7997,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rocky mountain ridge road in Ilaveezhapoonchira Kerala, treeless green rolling hill peaks, windy foggy viewpoint, dirt offroad track"
    },
    {
        "name": "Munnar, Idukki, Kerala, India",
        "lat": 10.0889, "lon": 77.0595,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain road in Munnar Kerala, undulating manicured green tea gardens, heavy mist, winding hairpin road, silver oak trees, cool climate"
    },
    {
        "name": "Thekkady, Idukki, Kerala, India",
        "lat": 9.6031, "lon": 77.1615,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a spice plantation road in Thekkady Periyar Kerala, cardamom and pepper vines, teak forest reserve, safari jeeps, cool highland air"
    },
    {
        "name": "Vagamon, Idukki, Kerala, India",
        "lat": 9.6917, "lon": 76.9067,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic hill road in Vagamon Kerala, pine tree forests, undulating grassy meadows, Kurisumala misty hills, tea gardens"
    },
    {
        "name": "Marayoor, Idukki, Kerala, India",
        "lat": 10.2800, "lon": 77.1500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dry valley road in Marayoor Kerala, natural sandalwood forest, sugarcane jaggery boiling sheds, ancient prehistoric dolmens, rain-shadow hills"
    },
    {
        "name": "Ramakkalmedu, Idukki, Kerala, India",
        "lat": 9.8000, "lon": 77.2500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a high wind cliff in Ramakkalmedu Kerala, giant electricity-generating windmills, panoramic view of Tamil Nadu plains below, Kuravan statue"
    },

    # --- Ernakulam & Thrissur ---
    {
        "name": "Fort Kochi, Ernakulam, Kerala, India",
        "lat": 9.9658, "lon": 76.2421,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a street in Fort Kochi, Dutch and Portuguese colonial architecture, massive rain trees, giant cantilever Chinese fishing nets, cobblestone promenade"
    },
    {
        "name": "Mattancherry Jew Town, Ernakulam, Kerala, India",
        "lat": 9.9575, "lon": 76.2594,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street in Jew Town Mattancherry Kochi, spice warehouses, antique craft shops, Paradesi Synagogue street, Dutch Palace walls"
    },
    {
        "name": "Marine Drive, Kochi, Kerala, India",
        "lat": 9.9790, "lon": 76.2760,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a waterfront boulevard in Marine Drive Kochi, rainbow bridge, luxury high-rise apartments, backwater ferries, urban promenade"
    },
    {
        "name": "Aluva, Ernakulam, Kerala, India",
        "lat": 10.1076, "lon": 76.3516,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a riverside town road in Aluva Kerala, Periyar river banks, Aluva Manappuram temple sandbed, Kochi Metro viaduct pillar"
    },
    {
        "name": "Swaraj Round, Thrissur, Kerala, India",
        "lat": 10.5276, "lon": 76.2144,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a circular city street around Swaraj Round Thrissur, Vadakkunnathan temple hillock in center, Pooram festival ground, bustling town traffic"
    },
    {
        "name": "Guruvayur, Thrissur, Kerala, India",
        "lat": 10.5947, "lon": 76.0394,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a temple street in Guruvayur Kerala, Krishna temple gopuram, pilgrims in traditional mundu attire, elephant sanctuary camp, brass lamps"
    },
    {
        "name": "Athirappilly, Thrissur, Kerala, India",
        "lat": 10.2851, "lon": 76.5698,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a forest road near Athirappilly Falls Kerala, majestic wide waterfall crashing over rocks, dense tropical rainforest, Western Ghats jungle road"
    },

    # --- Palakkad & Malappuram ---
    {
        "name": "Palakkad Fort, Palakkad, Kerala, India",
        "lat": 10.7633, "lon": 76.6547,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street near Palakkad Tipu Sultan Fort, granite fort ramparts with water moat, palmyra palm trees, flat dry gap plains"
    },
    {
        "name": "Chittur, Palakkad, Kerala, India",
        "lat": 10.7042, "lon": 76.7578,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rural village road in Chittur Palakkad, palmyra toddy palms against blue sky, emerald green irrigated paddy fields, bullock cart road"
    },
    {
        "name": "Nelliyampathy, Palakkad, Kerala, India",
        "lat": 10.5344, "lon": 76.6936,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a mountain ghat road in Nelliyampathy Kerala, orange and tea plantations, Pothundi dam view, cloud-covered hills, hairpin bends"
    },
    {
        "name": "Nilambur, Malappuram, Kerala, India",
        "lat": 11.2778, "lon": 76.2250,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a lush tree-lined road in Nilambur Kerala, world oldest teak plantation Conolly Plot, Chaliyar river banks, towering tropical hardwood trees"
    },
    {
        "name": "Kottakkal, Malappuram, Kerala, India",
        "lat": 10.9989, "lon": 75.9989,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a town street in Kottakkal Malappuram Kerala, Arya Vaidya Sala ayurvedic hospitals, medicinal herb gardens, tiled Kerala roof clinics"
    },
    {
        "name": "Ponnani, Malappuram, Kerala, India",
        "lat": 10.7667, "lon": 75.9333,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal harbor road in Ponnani Malappuram, ancient Juma Masjid wooden architecture, colorful wooden fishing boats, estuary where river meets sea"
    },

    # --- Kozhikode & Wayanad ---
    {
        "name": "Calicut Beach, Kozhikode, Kerala, India",
        "lat": 11.2588, "lon": 75.7686,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a seaside road at Calicut Beach Kozhikode, historic iron pier ruins in the waves, sunset promenade, pickled fruit stalls, Arabian sea"
    },
    {
        "name": "SM Street (Mittai Theruvu), Kozhikode, Kerala, India",
        "lat": 11.2504, "lon": 75.7804,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a bustling pedestrian heritage market in Sweet Meat Street Kozhikode, traditional Kozhikode halwa shops, tiled roof shop fronts, banana chips"
    },
    {
        "name": "Thamarassery Churam, Kozhikode, Kerala, India",
        "lat": 11.4983, "lon": 76.0125,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a dramatic mountain pass road at Thamarassery Churam Kerala, 9 steep hairpin curves, trucks climbing Ghat road, breathtaking valley view below"
    },
    {
        "name": "Sulthan Bathery, Wayanad, Kerala, India",
        "lat": 11.6667, "lon": 76.2500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a highland road in Sulthan Bathery Wayanad Kerala, ancient Jain temple, forest check post, coffee and pepper plantations, eucalyptus trees"
    },
    {
        "name": "Kalpetta, Wayanad, Kerala, India",
        "lat": 11.6083, "lon": 76.0833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a hilly town road in Kalpetta Wayanad, rolling coffee estates, spice markets, cool mountain climate, Chembra peak backdrop"
    },
    {
        "name": "Banasura Sagar Dam, Wayanad, Kerala, India",
        "lat": 11.6708, "lon": 75.9575,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic reservoir road at Banasura Sagar Dam Wayanad, largest earthen dam in India, reservoir with submerged hill islands, rugged hills"
    },

    # --- Kannur & Kasaragod ---
    {
        "name": "Thalassery, Kannur, Kerala, India",
        "lat": 11.7480, "lon": 75.4894,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal street in Thalassery Kannur, colonial English fort over rocky sea, historic bakery culture, cricket maidans, Malayalam signage"
    },
    {
        "name": "Muzhappilangad Drive-in Beach, Kannur, Kerala, India",
        "lat": 11.7925, "lon": 75.4522,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "cars driving directly along the wet hard sand of Muzhappilangad Drive-in Beach Kannur, sea waves splashing tires, coconut palm coastline"
    },
    {
        "name": "Payyambalam Beach, Kannur, Kerala, India",
        "lat": 11.8722, "lon": 75.3522,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal road in Payyambalam Kannur, St Angelo Fort laterite walls nearby, Arabian sea cliffs, political martyr monuments, palm trees"
    },
    {
        "name": "Bekal Fort, Kasaragod, Kerala, India",
        "lat": 12.3925, "lon": 75.0319,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal heritage view at Bekal Fort Kasaragod, massive dark laterite observation tower projecting into the sea, manicured green lawns, waves"
    },
    {
        "name": "Ranipuram, Kasaragod, Kerala, India",
        "lat": 12.4333, "lon": 75.3500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a high altitude shola grassland track in Ranipuram Kasaragod, Ooty of Kerala, undulating green hills, shola forest patches, misty hiking trail"
    },

    # ==========================================================================
    # 2. ALL 28 INDIAN STATES & 8 UNION TERRITORIES
    # ==========================================================================
    {
        "name": "Andhra Pradesh, India",
        "lat": 16.5062, "lon": 80.6480,
        "country": "India", "region": "Andhra Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in Andhra Pradesh, Krishna river delta, Telugu script on shop signs, agricultural chilli and paddy fields, rural RTC bus"
    },
    {
        "name": "Arunachal Pradesh, India",
        "lat": 27.5861, "lon": 91.8678,
        "country": "India", "region": "Arunachal Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain road in Arunachal Pradesh, Tawang Tibetan Buddhist monastery, snow-covered Eastern Himalayas, prayer flags, bamboo bridges"
    },
    {
        "name": "Assam, India",
        "lat": 26.1445, "lon": 91.7362,
        "country": "India", "region": "Assam", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a rural road in Assam, vast green tea garden plantations, Brahmaputra river plains, bamboo stilt huts, Assamese script road signs"
    },
    {
        "name": "Bihar, India",
        "lat": 25.5941, "lon": 85.1376,
        "country": "India", "region": "Bihar", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Bihar, fertile Gangetic floodplains, brick chimneys and kilns, thatched village mud houses, tractors, Hindi script"
    },
    {
        "name": "Chhattisgarh, India",
        "lat": 21.2514, "lon": 81.6296,
        "country": "India", "region": "Chhattisgarh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a highway in Chhattisgarh, dense Sal and teak forest, red mineral soil, tribal village haat market, broad newly paved state road"
    },
    {
        "name": "Goa, India",
        "lat": 15.2993, "lon": 74.1240,
        "country": "India", "region": "Goa", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in Goa, Portuguese colonial villas painted in yellow and blue, white baroque Catholic churches, scooter rentals, coconut palms"
    },
    {
        "name": "Gujarat, India",
        "lat": 23.0225, "lon": 72.5714,
        "country": "India", "region": "Gujarat", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in Gujarat, wide clean highways, Gujarati signboards, textile and diamond workshops, dry thorny vegetation, modern overpasses"
    },
    {
        "name": "Haryana, India",
        "lat": 29.0588, "lon": 76.0856,
        "country": "India", "region": "Haryana", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a rural road in Haryana, vast green wheat and yellow mustard fields, irrigation canal tubewells, heavy agricultural tractors, wide tollways"
    },
    {
        "name": "Himachal Pradesh, India",
        "lat": 31.1048, "lon": 77.1734,
        "country": "India", "region": "Himachal Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain road in Himachal Pradesh, towering Himalayan deodar pine trees, apple orchards, steep mountain cliffs, slate roof houses"
    },
    {
        "name": "Jharkhand, India",
        "lat": 23.3441, "lon": 85.3096,
        "country": "India", "region": "Jharkhand", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Jharkhand, Chota Nagpur plateau, red gravel hills, coal and iron transport trucks, Sal tree forests, tribal hamlets"
    },
    {
        "name": "Karnataka, India",
        "lat": 12.9716, "lon": 77.5946,
        "country": "India", "region": "Karnataka", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Karnataka, red soil, Deccan granite boulders, Kannada script signboards, KSRTC red bus, coconut and areca nut palms"
    },
    {
        "name": "Kerala, India",
        "lat": 10.8505, "lon": 76.2711,
        "country": "India", "region": "Kerala", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Kerala, lush green coconut trees, red laterite compound walls, Malayalam language boards, rubber trees, humid tropical landscape"
    },
    {
        "name": "Madhya Pradesh, India",
        "lat": 23.2599, "lon": 77.4126,
        "country": "India", "region": "Madhya Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a highway in Madhya Pradesh, rolling central Indian plateau, ancient sandstone temples and forts, wheat fields, dry deciduous forest"
    },
    {
        "name": "Maharashtra, India",
        "lat": 19.0760, "lon": 72.8777,
        "country": "India", "region": "Maharashtra", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Maharashtra, Sahyadri Western Ghat mountains, black basalt rock cut roads, Marathi signboards, sugarcane fields, MSRTC bus"
    },
    {
        "name": "Manipur, India",
        "lat": 24.8170, "lon": 93.9368,
        "country": "India", "region": "Manipur", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Manipur, Imphal valley surrounded by green hills, Loktak lake phumdis floating islands, Meitei script boards, bamboo fencing"
    },
    {
        "name": "Meghalaya, India",
        "lat": 25.5788, "lon": 91.8933,
        "country": "India", "region": "Meghalaya", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a scenic road in Meghalaya, heavy rain and rolling mountain mist, living root bridges, pine hills, dramatic limestone waterfalls, Khasi villages"
    },
    {
        "name": "Mizoram, India",
        "lat": 23.7271, "lon": 92.7176,
        "country": "India", "region": "Mizoram", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a steep ridge road in Mizoram, colorful houses perched precariously on sheer hill slopes, bamboo thickets, blue mountain horizon"
    },
    {
        "name": "Nagaland, India",
        "lat": 25.6751, "lon": 94.1086,
        "country": "India", "region": "Nagaland", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain ridge road in Nagaland, traditional Naga wooden carved village gates, terraced rice hills, church spires, misty highlands"
    },
    {
        "name": "Odisha, India",
        "lat": 20.2961, "lon": 85.8245,
        "country": "India", "region": "Odisha", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Odisha, ancient Kalinga temple spires, red laterite soil, Odia script curved signboards, coastal paddy fields, banyan trees"
    },
    {
        "name": "Punjab, India",
        "lat": 31.6340, "lon": 74.8723,
        "country": "India", "region": "Punjab", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a highway in Punjab, fertile wheat and mustard fields, Gurmukhi Punjabi signboards, large Sikh gurdwaras with golden domes, tractors"
    },
    {
        "name": "Rajasthan, India",
        "lat": 26.9124, "lon": 75.7873,
        "country": "India", "region": "Rajasthan", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a desert road in Rajasthan, golden sand dunes, thorny acacia trees, yellow sandstone forts and havelis, camels, vibrant turbans"
    },
    {
        "name": "Sikkim, India",
        "lat": 27.3389, "lon": 88.6065,
        "country": "India", "region": "Sikkim", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain road in Sikkim, view of snow-capped Kanchenjunga peak, colorful Buddhist prayer flags, cardamom terrace farms, clean roads"
    },
    {
        "name": "Tamil Nadu, India",
        "lat": 13.0827, "lon": 80.2707,
        "country": "India", "region": "Tamil Nadu", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in Tamil Nadu, towering colorful temple gopuram entrance, Tamil script boards, banana trees, autorickshaws, hot tropical sun"
    },
    {
        "name": "Telangana, India",
        "lat": 17.3850, "lon": 78.4867,
        "country": "India", "region": "Telangana", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Telangana, ancient Deccan granite boulder rock formations, Telugu and Urdu signboards, red soil, neem trees, modern highway"
    },
    {
        "name": "Tripura, India",
        "lat": 23.8315, "lon": 91.2868,
        "country": "India", "region": "Tripura", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Tripura, Ujjayanta white palace, lush rubber plantations, bamboo groves, small brick bridges, Bengali and Kokborok boards"
    },
    {
        "name": "Uttar Pradesh, India",
        "lat": 26.8467, "lon": 80.9462,
        "country": "India", "region": "Uttar Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a busy road in Uttar Pradesh, Gangetic plains, Mughal domes and minarets, Hindi shop boards, cycle rickshaws, sugarcane carts"
    },
    {
        "name": "Uttarakhand, India",
        "lat": 30.0668, "lon": 79.0193,
        "country": "India", "region": "Uttarakhand", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain highway in Uttarakhand, holy Ganga river gorge, Himalayan suspension footbridges, pine covered steep ridges, ashrams"
    },
    {
        "name": "West Bengal, India",
        "lat": 22.5726, "lon": 88.3639,
        "country": "India", "region": "West Bengal", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in West Bengal, yellow Ambassador taxis, British colonial stone facades, Bengali script signboards, sweet shops, ponds"
    },

    # --- Union Territories ---
    {
        "name": "Delhi NCR, India",
        "lat": 28.6139, "lon": 77.2090,
        "country": "India", "region": "Delhi", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in Delhi, wide tree-lined boulevards of Lutyens Delhi, red sandstone heritage monuments, green and yellow autorickshaws, elevated Metro viaduct"
    },
    {
        "name": "Chandigarh, India",
        "lat": 30.7333, "lon": 76.7794,
        "country": "India", "region": "Chandigarh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a boulevard in Chandigarh, Le Corbusier modernist exposed concrete architecture, wide green roundabouts, manicured sector roads, flowering trees"
    },
    {
        "name": "Ladakh, India",
        "lat": 34.1526, "lon": 77.5771,
        "country": "India", "region": "Ladakh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Ladakh, high altitude cold desert, dramatic barren brown mountains, Tibetan Buddhist white stupas, crystal clear turquoise Indus river"
    },
    {
        "name": "Jammu and Kashmir, India",
        "lat": 34.0837, "lon": 74.7973,
        "country": "India", "region": "Jammu and Kashmir", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a road in Kashmir, Dal lake wooden houseboats, giant chinar trees with golden leaves, snow-covered Pir Panjal mountain range, wooden Kashmiri houses"
    },
    {
        "name": "Puducherry, India",
        "lat": 11.9416, "lon": 79.8083,
        "country": "India", "region": "Puducherry", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a street in Puducherry French Quarter, pastel yellow colonial villas with French shutters, bougainvillea gates, rocky beach promenade, clean grid streets"
    },
    {
        "name": "Andaman and Nicobar Islands, India",
        "lat": 11.6234, "lon": 92.7265,
        "country": "India", "region": "Andaman and Nicobar", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a coastal road in Andaman Islands, Cellular Jail brick walls, tropical turquoise ocean, white coral beaches, dense rain forest canopy"
    },
    {
        "name": "Lakshadweep, India",
        "lat": 10.5667, "lon": 72.6417,
        "country": "India", "region": "Lakshadweep", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "an island pathway in Lakshadweep, turquoise coral reef lagoon, white coral sand, dense canopy of coconut palms, quiet tropical atoll"
    },

    # ==========================================================================
    # 3. MAJOR INDIAN METROS, CULTURAL & HISTORIC HUBS
    # ==========================================================================
    {
        "name": "Old Delhi (Chandni Chowk), Delhi, India",
        "lat": 28.6506, "lon": 77.2303,
        "country": "India", "region": "Delhi", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "dense narrow street in Chandni Chowk Old Delhi, overhead tangle of electrical wires, Mughal brickwork, Hindi Urdu signs, cycle rickshaws"
    },
    {
        "name": "Varanasi Ghats, Uttar Pradesh, India",
        "lat": 25.3036, "lon": 83.0033,
        "country": "India", "region": "Uttar Pradesh", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "stone steps on river Ganges ghats in Varanasi, ancient Hindu temples, wooden boats, ochre painted walls, narrow ancient alleyways"
    },
    {
        "name": "Hampi, Bellary, Karnataka, India",
        "lat": 15.3350, "lon": 76.4600,
        "country": "India", "region": "Karnataka", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "granite boulder hills in Hampi Karnataka, ancient Vijayanagara ruins, arid red terrain, banana plantations, stone monuments"
    },
    {
        "name": "Mumbai (Marine Drive & South Bombay), Maharashtra, India",
        "lat": 18.9432, "lon": 72.8236,
        "country": "India", "region": "Maharashtra", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a boulevard on Marine Drive Mumbai, Art Deco heritage apartments, Arabian Sea seawall tetrapods, yellow and black Premier Padmini taxis"
    },
    {
        "name": "Bengaluru (Tech Corridors & Cubbon Park), Karnataka, India",
        "lat": 12.9716, "lon": 77.5946,
        "country": "India", "region": "Karnataka", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a boulevard in Bengaluru, canopy of blooming rain trees and jacarandas, glass IT tech parks, BMTC green buses, Namma Metro viaduct"
    },
    {
        "name": "Kolkata (Howrah Bridge & Victoria Memorial), West Bengal, India",
        "lat": 22.5850, "lon": 88.3468,
        "country": "India", "region": "West Bengal", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a street in Kolkata, giant steel cantilever Howrah Bridge over Hooghly river, yellow Ambassador taxis, vintage British colonial buildings, tram tracks"
    },
    {
        "name": "Chennai (Marina Beach & Mylapore), Tamil Nadu, India",
        "lat": 13.0475, "lon": 80.2824,
        "country": "India", "region": "Tamil Nadu", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a street in Mylapore Chennai, Kapaleeshwarar temple towering colorful gopuram, silk saree shops, Marina beach promenade, Tamil boards"
    },
    {
        "name": "Hyderabad (Charminar & HITEC City), Telangana, India",
        "lat": 17.3616, "lon": 78.4747,
        "country": "India", "region": "Telangana", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a historic street around Charminar Hyderabad, four towering minarets, pearl and bangle markets, Irani chai cafes, Deccan architecture"
    },
    {
        "name": "Jaipur (Pink City), Rajasthan, India",
        "lat": 26.9239, "lon": 75.8267,
        "country": "India", "region": "Rajasthan", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a street in the Pink City Jaipur, terracotta pink sandstone buildings, Hawa Mahal lattice windows, camels, brass handicraft shops"
    },
    {
        "name": "Agra (Taj Mahal surroundings), Uttar Pradesh, India",
        "lat": 27.1751, "lon": 78.0421,
        "country": "India", "region": "Uttar Pradesh", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a street near Taj Mahal Agra, white marble Mughal domes, red sandstone gates of Agra Fort, Yamuna river bank, battery electric rickshaws"
    },
    {
        "name": "Amritsar (Golden Temple), Punjab, India",
        "lat": 31.6200, "lon": 74.8765,
        "country": "India", "region": "Punjab", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a pedestrian street leading to the Golden Temple Amritsar, clean heritage marble walkway, Sikh turbans, Punjabi food stalls, red brick facades"
    },
    {
        "name": "Shimla (The Ridge & Mall Road), Himachal Pradesh, India",
        "lat": 31.1048, "lon": 77.1734,
        "country": "India", "region": "Himachal Pradesh", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a pedestrian walkway on The Ridge Shimla, British neo-Gothic Christ Church, panoramic Himalayan mountain view, deodar pine forested slopes"
    },
    {
        "name": "Manali (Old Manali & Solang Valley), Himachal Pradesh, India",
        "lat": 32.2396, "lon": 77.1887,
        "country": "India", "region": "Himachal Pradesh", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a rustic mountain road in Old Manali, traditional timber and stone houses, apple orchards, rushing Beas river torrent, snow peaks"
    },
    {
        "name": "Rishikesh (Lakshman Jhula & Ganga), Uttarakhand, India",
        "lat": 30.1333, "lon": 78.3333,
        "country": "India", "region": "Uttarakhand", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a river road in Rishikesh, suspension bridge over the emerald green Ganga river, yoga ashrams, Himalayan foothills, sadhus"
    },
    {
        "name": "Darjeeling, West Bengal, India",
        "lat": 27.0410, "lon": 88.2663,
        "country": "India", "region": "West Bengal", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a hillside street in Darjeeling, narrow-gauge Toy Train railway tracks running along the road, steep tea garden terraces, colonial cottages"
    },
    {
        "name": "Mysore (Mysore Palace), Karnataka, India",
        "lat": 12.3051, "lon": 76.6551,
        "country": "India", "region": "Karnataka", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a royal boulevard in Mysore, Indo-Saracenic Mysore Palace illuminated gates, clean wide avenues, tonga horse carriages, Chamundi hill"
    },
    {
        "name": "Madurai (Meenakshi Temple), Tamil Nadu, India",
        "lat": 9.9195, "lon": 78.1193,
        "country": "India", "region": "Tamil Nadu", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a concentric street in Madurai around Meenakshi Amman Temple, monumental sculpted gopurams reaching the sky, jasmine flower markets, Tamil signs"
    },
    {
        "name": "Pune, Maharashtra, India",
        "lat": 18.5204, "lon": 73.8567,
        "country": "India", "region": "Maharashtra", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a leafy avenue in Pune, traditional wada wooden houses, student university cafes, tree canopy, two-wheelers everywhere, Marathi signage"
    },
    {
        "name": "Ahmedabad, Gujarat, India",
        "lat": 23.0225, "lon": 72.5714,
        "country": "India", "region": "Gujarat", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a street in old Ahmedabad, carved wooden pol houses, Sabarmati riverfront modern promenade, BRTS dedicated bus lanes, Gujarati script"
    },

    # ==========================================================================
    # 4. GLOBAL COUNTRIES & WORLDWIDE REGIONS (STREET VIEW COVERAGE)
    # ==========================================================================
    # --- East & Southeast Asia ---
    {
        "name": "Tokyo, Japan",
        "lat": 35.6762, "lon": 139.6503,
        "country": "Japan", "region": "Kanto", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Tokyo Japan, narrow spotless asphalt road, low utility poles with intricate transformers, Japanese kanji signage, kei cars, driving on left"
    },
    {
        "name": "Kyoto, Japan",
        "lat": 35.0116, "lon": 135.7681,
        "country": "Japan", "region": "Kansai", "category": "Global", "driving_side": "Left",
        "prompt": "a historic street in Kyoto Japan, traditional dark wood machiya townhouses, stone-paved alleyway, bamboo fences, small Shinto shrines, left driving"
    },
    {
        "name": "Hokkaido, Japan",
        "lat": 43.0642, "lon": 141.3469,
        "country": "Japan", "region": "Hokkaido", "category": "Global", "driving_side": "Left",
        "prompt": "a rural road in Hokkaido Japan, downward-pointing red-and-white arrow snow markers on poles, wide flat farm fields, birch trees, snowy mountains"
    },
    {
        "name": "Seoul, South Korea",
        "lat": 37.5665, "lon": 126.9780,
        "country": "South Korea", "region": "Seoul", "category": "Global", "driving_side": "Right",
        "prompt": "a modern street in Seoul South Korea, Hangul script signs, numbered high-rise apartment towers, blue street signs, mountainous hill horizon"
    },
    {
        "name": "Taipei, Taiwan",
        "lat": 25.0330, "lon": 121.5654,
        "country": "Taiwan", "region": "Taipei", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Taipei Taiwan, sea of motor scooters, yellow and black striped utility poles, traditional Chinese characters, lush green mountains"
    },
    {
        "name": "Hong Kong",
        "lat": 22.3193, "lon": 114.1694,
        "country": "Hong Kong", "region": "Hong Kong", "category": "Global", "driving_side": "Left",
        "prompt": "a dense street in Hong Kong, towering high-rises, double-decker buses, bilingual English and Chinese neon signs, steep lush green hills, driving left"
    },
    {
        "name": "Singapore",
        "lat": 1.3521, "lon": 103.8198,
        "country": "Singapore", "region": "Singapore", "category": "Global", "driving_side": "Left",
        "prompt": "a pristine boulevard in Singapore, massive flowering rain trees with fern-covered trunks, manicured green dividers, ERP electronic toll gantries, driving left"
    },
    {
        "name": "Bangkok, Thailand",
        "lat": 13.7563, "lon": 100.5018,
        "country": "Thailand", "region": "Bangkok", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Bangkok Thailand, overhead jumble of power lines, Thai script signs, colorful tuk-tuks and Toyota Hilux pickups, driving on left"
    },
    {
        "name": "Chiang Mai, Thailand",
        "lat": 18.7883, "lon": 98.9853,
        "country": "Thailand", "region": "Northern Thailand", "category": "Global", "driving_side": "Left",
        "prompt": "a road in Chiang Mai Thailand, teak wood Lanna houses, golden Buddhist temple chedis, lush tropical foothills, driving on left"
    },
    {
        "name": "Kuala Lumpur, Malaysia",
        "lat": 3.1390, "lon": 101.6869,
        "country": "Malaysia", "region": "Federal Territory", "category": "Global", "driving_side": "Left",
        "prompt": "a highway in Kuala Lumpur Malaysia, elevated monorail, tropical palm trees, Malay and Jawi script road signs, black license plates, driving on left"
    },
    {
        "name": "Jakarta, Indonesia",
        "lat": -6.2088, "lon": 106.8456,
        "country": "Indonesia", "region": "Java", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Jakarta Indonesia, dense swarm of motorbikes, black license plates with white lettering, tropical humidity, Bahasa Indonesia signs, driving left"
    },
    {
        "name": "Bali, Indonesia",
        "lat": -8.4095, "lon": 115.1889,
        "country": "Indonesia", "region": "Bali", "category": "Global", "driving_side": "Left",
        "prompt": "a village road in Bali Indonesia, carved volcanic stone candi bentar split gates, green terraced rice fields, banyan trees, offerings on sidewalks"
    },
    {
        "name": "Manila, Philippines",
        "lat": 14.5995, "lon": 120.9842,
        "country": "Philippines", "region": "Metro Manila", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Manila Philippines, colorful painted Jeepneys, concrete utility poles, Spanish colonial churches, English road signs, tropical palms"
    },
    {
        "name": "Hanoi, Vietnam",
        "lat": 21.0285, "lon": 105.8542,
        "country": "Vietnam", "region": "Red River Delta", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Hanoi Vietnam, sea of Honda motorbikes, narrow multi-story tube houses with French balconies, Vietnamese script with tone diacritics"
    },
    {
        "name": "Phnom Penh, Cambodia",
        "lat": 11.5564, "lon": 104.9282,
        "country": "Cambodia", "region": "Phnom Penh", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Cambodia, red dirt shoulders, Khmer script signboards, wooden houses on stilts, Buddhist pagodas with golden spires"
    },

    # --- Europe ---
    {
        "name": "London, United Kingdom",
        "lat": 51.5074, "lon": -0.1278,
        "country": "United Kingdom", "region": "England", "category": "Global", "driving_side": "Left",
        "prompt": "a street in London UK, red double-decker buses, Victorian red brick terraced houses, yellow rear vehicle license plates, white front plates, driving on left"
    },
    {
        "name": "Scottish Highlands, United Kingdom",
        "lat": 57.3229, "lon": -4.4244,
        "country": "United Kingdom", "region": "Scotland", "category": "Global", "driving_side": "Left",
        "prompt": "a single-track road in Scottish Highlands UK, passing places, rolling heather moorland, stone cottages, misty lochs, sheep, driving on left"
    },
    {
        "name": "Dublin, Ireland",
        "lat": 53.3498, "lon": -6.2603,
        "country": "Ireland", "region": "Leinster", "category": "Global", "driving_side": "Left",
        "prompt": "a road in Ireland, stone walls along lush green fields, yellow dashed road edge lines, bilingual English and Irish Gaelic road signs, driving on left"
    },
    {
        "name": "Paris, France",
        "lat": 48.8566, "lon": 2.3522,
        "country": "France", "region": "Île-de-France", "category": "Global", "driving_side": "Right",
        "prompt": "a boulevard in Paris France, Haussmannian cream limestone apartment facades with wrought iron balconies, blue enamel street plaques, cafe sidewalk tables"
    },
    {
        "name": "Provence, France",
        "lat": 43.8374, "lon": 5.4474,
        "country": "France", "region": "Provence-Alpes-Côte d'Azur", "category": "Global", "driving_side": "Right",
        "prompt": "a rural road in Provence France, rows of purple lavender fields, stone farmhouses with terracotta tile roofs, cypress trees, white bollards with red reflectors"
    },
    {
        "name": "Berlin, Germany",
        "lat": 52.5200, "lon": 13.4050,
        "country": "Germany", "region": "Berlin", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Berlin Germany, broad asphalt avenue with bicycle lanes, red-and-white pedestrian crossings, German DIN typography on street signs"
    },
    {
        "name": "Bavaria, Germany",
        "lat": 47.7516, "lon": 11.5583,
        "country": "Germany", "region": "Bavaria", "category": "Global", "driving_side": "Right",
        "prompt": "a village road in Bavaria Germany, Alpine chalets with wooden balconies and blooming geraniums, lush green pastures, church onion domes"
    },
    {
        "name": "Rome, Italy",
        "lat": 41.9028, "lon": 12.4964,
        "country": "Italy", "region": "Lazio", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Rome Italy, cobblestone sampietrini paving, ochre and terracotta plaster buildings, Vespa scooters, stone pine trees, small square front license plates"
    },
    {
        "name": "Tuscany, Italy",
        "lat": 43.7711, "lon": 11.2486,
        "country": "Italy", "region": "Tuscany", "category": "Global", "driving_side": "Right",
        "prompt": "a winding country road in Tuscany Italy, rolling golden hills, lines of tall slender cypress trees, stone farmhouse villas, olive groves"
    },
    {
        "name": "Madrid, Spain",
        "lat": 40.4168, "lon": -3.7038,
        "country": "Spain", "region": "Community of Madrid", "category": "Global", "driving_side": "Right",
        "prompt": "a wide street in Madrid Spain, grand classical architecture, stone sidewalk paving, blue sky, modern city buses, European Union blue band on license plates"
    },
    {
        "name": "Andalusia, Spain",
        "lat": 37.3891, "lon": -5.9845,
        "country": "Spain", "region": "Andalusia", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Andalusia Spain, vast olive tree groves stretching across arid hills, whitewashed pueblos blancos hill villages, intense southern sun"
    },
    {
        "name": "Lisbon, Portugal",
        "lat": 38.7223, "lon": -9.1393,
        "country": "Portugal", "region": "Lisbon", "category": "Global", "driving_side": "Right",
        "prompt": "a steep street in Lisbon Portugal, black and white calcada portuguesa cobblestone pavements, glazed azulejo ceramic tile facades, yellow vintage tram tracks"
    },
    {
        "name": "Amsterdam, Netherlands",
        "lat": 52.3676, "lon": 4.9041,
        "country": "Netherlands", "region": "North Holland", "category": "Global", "driving_side": "Right",
        "prompt": "a canal street in Amsterdam Netherlands, narrow brick canal houses with decorative gables, red asphalt bicycle tracks, houseboats, arched brick bridges"
    },
    {
        "name": "Brussels, Belgium",
        "lat": 50.8503, "lon": 4.3517,
        "country": "Belgium", "region": "Brussels", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Brussels Belgium, red and dark brick townhouses with stepped gables, red font license plates with European flag, bilingual French and Dutch signs"
    },
    {
        "name": "Swiss Alps, Switzerland",
        "lat": 46.5663, "lon": 8.0163,
        "country": "Switzerland", "region": "Bern", "category": "Global", "driving_side": "Right",
        "prompt": "an alpine pass road in Switzerland, pristine mountain meadows, wooden Swiss chalets with overhanging roofs, jagged snowcapped Alps, yellow walking trail signs"
    },
    {
        "name": "Tyrol, Austria",
        "lat": 47.2692, "lon": 11.4041,
        "country": "Austria", "region": "Tyrol", "category": "Global", "driving_side": "Right",
        "prompt": "a valley road in Austrian Tyrol, dramatic steep alpine mountains, white plaster churches with pointed spires, flower-adorned timber farmsteads"
    },
    {
        "name": "Stockholm, Sweden",
        "lat": 59.3293, "lon": 18.0686,
        "country": "Sweden", "region": "Stockholm", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Stockholm Sweden, clean Scandinavian architecture, red Falu timber houses in countryside, white dashed road edge lines, birch and spruce trees"
    },
    {
        "name": "Fjords, Norway",
        "lat": 61.2223, "lon": 6.8488,
        "country": "Norway", "region": "Vestland", "category": "Global", "driving_side": "Right",
        "prompt": "a scenic road along a Norwegian fjord, sheer granite cliffs dropping into deep blue water, waterfalls, grass roof wooden huts, yellow painted centerline"
    },
    {
        "name": "Copenhagen, Denmark",
        "lat": 55.6761, "lon": 12.5683,
        "country": "Denmark", "region": "Capital Region", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Copenhagen Denmark, dedicated raised bike tracks filled with cyclists, red brick apartment blocks, flat landscape, yellow rear commercial plates"
    },
    {
        "name": "Helsinki, Finland",
        "lat": 60.1699, "lon": 24.9384,
        "country": "Finland", "region": "Uusimaa", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Finland, endless pine and birch forests, clear granite rock cuts along highway, blue and white road signs, numerous calm lakes"
    },
    {
        "name": "Reykjavik, Iceland",
        "lat": 64.1466, "lon": -21.9426,
        "country": "Iceland", "region": "Capital Region", "category": "Global", "driving_side": "Right",
        "prompt": "a highway in Iceland, barren moss-covered black volcanic lava fields, treeless landscape, yellow roadside marker posts, corrugated metal houses"
    },
    {
        "name": "Warsaw, Poland",
        "lat": 52.2297, "lon": 21.0122,
        "country": "Poland", "region": "Masovia", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Poland, ladder-style concrete utility poles with holes, red-and-white roadside bollards, flat agricultural fields, Polish language signs"
    },
    {
        "name": "Prague, Czech Republic",
        "lat": 50.0755, "lon": 14.4378,
        "country": "Czech Republic", "region": "Prague", "category": "Global", "driving_side": "Right",
        "prompt": "a cobblestone street in Prague Czech Republic, red terracotta roof tiles, historical baroque and gothic facades, blue street signs, red and white trams"
    },
    {
        "name": "Budapest, Hungary",
        "lat": 47.4979, "lon": 19.0402,
        "country": "Hungary", "region": "Central Hungary", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Hungary, concrete utility poles with circular holes, flat Puszta agricultural plain, grand Austro-Hungarian architecture, Hungarian signs"
    },
    {
        "name": "Transylvania, Romania",
        "lat": 46.7712, "lon": 23.6236,
        "country": "Romania", "region": "Transylvania", "category": "Global", "driving_side": "Right",
        "prompt": "a village road in Romania, concrete utility poles painted white at the base with holes, horse-drawn carts, traditional timber gates, Carpathian mountains"
    },
    {
        "name": "Athens, Greece",
        "lat": 37.9838, "lon": 23.7275,
        "country": "Greece", "region": "Attica", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Athens Greece, white concrete residential blocks with fabric awnings on balconies, olive trees, Greek alphabet signs, arid rocky hills"
    },
    {
        "name": "Santorini, Greece",
        "lat": 36.3932, "lon": 25.4615,
        "country": "Greece", "region": "South Aegean", "category": "Global", "driving_side": "Right",
        "prompt": "a cliff path in Santorini Greece, whitewashed cubic houses with bright blue painted domes, volcanic caldera sea view, bougainvillea, stone paths"
    },
    {
        "name": "Dubrovnik, Croatia",
        "lat": 42.6507, "lon": 18.0944,
        "country": "Croatia", "region": "Dalmatia", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road along the Adriatic coast in Croatia, turquoise sea water, limestone karst cliffs, orange terracotta roofed villages, olive groves"
    },
    {
        "name": "Kyiv, Ukraine",
        "lat": 50.4501, "lon": 30.5234,
        "country": "Ukraine", "region": "Kyiv", "category": "Global", "driving_side": "Right",
        "prompt": "a broad avenue in Kyiv Ukraine, golden church cupolas, Cyrillic script signs, vast sunflower fields in countryside, blue and yellow painted fences"
    },
    {
        "name": "Moscow, Russia",
        "lat": 55.7558, "lon": 37.6173,
        "country": "Russia", "region": "Central Federal District", "category": "Global", "driving_side": "Right",
        "prompt": "a wide multi-lane avenue in Moscow Russia, monumental Stalinist architecture, blue street name signs with Cyrillic script, trolleybus overhead wires"
    },
    {
        "name": "Siberia, Russia",
        "lat": 56.0153, "lon": 92.8932,
        "country": "Russia", "region": "Siberian Federal District", "category": "Global", "driving_side": "Right",
        "prompt": "a rural highway in Siberia Russia, vast birch tree and pine taiga forest, wooden izba houses with carved blue window frames, unpaved gravel road"
    },
    {
        "name": "Istanbul, Turkey",
        "lat": 41.0082, "lon": 28.9784,
        "country": "Turkey", "region": "Marmara", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Istanbul Turkey, Bosphorus strait view, Ottoman era wooden mansions, minarets and stone domes, Turkish flags, red terracotta roofline"
    },

    # --- Americas ---
    {
        "name": "New York City, New York, United States",
        "lat": 40.7128, "lon": -74.0060,
        "country": "United States", "region": "New York", "category": "Global", "driving_side": "Right",
        "prompt": "a street in New York City, yellow cabs, iconic Manhattan skyscrapers, brownstone rowhouses with iron fire escapes, green street name signs"
    },
    {
        "name": "Los Angeles, California, United States",
        "lat": 34.0522, "lon": -118.2437,
        "country": "United States", "region": "California", "category": "Global", "driving_side": "Right",
        "prompt": "a wide street in Los Angeles California, towering slender Mexican fan palm trees, low stucco commercial plazas, bright sunshine, wide asphalt lanes"
    },
    {
        "name": "San Francisco, California, United States",
        "lat": 37.7749, "lon": -122.4194,
        "country": "United States", "region": "California", "category": "Global", "driving_side": "Right",
        "prompt": "a steep hilly street in San Francisco California, Victorian Painted Lady row houses, cable car tracks in road, bay view in distance, cool ocean fog"
    },
    {
        "name": "Pacific Coast Highway, California, United States",
        "lat": 36.3615, "lon": -121.8563,
        "country": "United States", "region": "California", "category": "Global", "driving_side": "Right",
        "prompt": "a scenic highway on Big Sur California, rugged cliffs crashing into the Pacific ocean, concrete arch Bixby bridge, yellow center double lines"
    },
    {
        "name": "Pacific Northwest, Washington, United States",
        "lat": 47.6062, "lon": -122.3321,
        "country": "United States", "region": "Washington", "category": "Global", "driving_side": "Right",
        "prompt": "a highway in Washington Pacific Northwest, dense Douglas fir and cedar forests, moss-draped trees, misty overcast grey skies, snow-peaked Mount Rainier"
    },
    {
        "name": "Southwest Desert, Arizona, United States",
        "lat": 34.0489, "lon": -111.0937,
        "country": "United States", "region": "Arizona", "category": "Global", "driving_side": "Right",
        "prompt": "a highway in Arizona, towering giant Saguaro cactus, dry red sandy desert earth, distant flat-topped red rock mesas, brilliant clear blue sky"
    },
    {
        "name": "Midwest Farmland, Iowa, United States",
        "lat": 41.8780, "lon": -93.0977,
        "country": "United States", "region": "Iowa", "category": "Global", "driving_side": "Right",
        "prompt": "a rural county road in US Midwest, endless fields of green corn and golden soybeans, straight grid road, silver grain silos, white wooden barns"
    },
    {
        "name": "Texas Plains, Texas, United States",
        "lat": 31.9686, "lon": -99.9018,
        "country": "United States", "region": "Texas", "category": "Global", "driving_side": "Right",
        "prompt": "a wide flat highway in Texas, large pickup trucks, ranch entrance gates with steer horns, mesquite scrub bushes, massive highway overpasses"
    },
    {
        "name": "Miami, Florida, United States",
        "lat": 25.7617, "lon": -80.1918,
        "country": "United States", "region": "Florida", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal street in Miami Florida, pastel Art Deco buildings, royal palm trees, flat humid coastal sky, white sandy beaches, convertible cars"
    },
    {
        "name": "Anchorage, Alaska, United States",
        "lat": 61.2181, "lon": -149.9003,
        "country": "United States", "region": "Alaska", "category": "Global", "driving_side": "Right",
        "prompt": "a highway in Alaska, snowcapped rugged peaks, spruce forests, wide gravel shoulders, wooden log cabins, tundra vegetation"
    },
    {
        "name": "Honolulu, Hawaii, United States",
        "lat": 21.3069, "lon": -157.8583,
        "country": "United States", "region": "Hawaii", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Hawaii, Diamond Head volcanic crater backdrop, lush tropical banyan and plumeria trees, rainbow state license plates, turquoise Pacific surf"
    },
    {
        "name": "Toronto, Ontario, Canada",
        "lat": 43.6532, "lon": -79.3832,
        "country": "Canada", "region": "Ontario", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Toronto Canada, CN Tower skyline, red TTC streetcars, green highway signs with crown symbol, maple trees, red brick houses"
    },
    {
        "name": "Montreal, Quebec, Canada",
        "lat": 45.5017, "lon": -73.5673,
        "country": "Canada", "region": "Quebec", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Montreal Quebec, red stop signs reading ARRET, exterior spiral iron staircases on triplex townhouses, French language signboards"
    },
    {
        "name": "Canadian Rockies, Alberta, Canada",
        "lat": 51.1784, "lon": -115.5708,
        "country": "Canada", "region": "Alberta", "category": "Global", "driving_side": "Right",
        "prompt": "a mountain highway through Canadian Rockies Alberta, towering jagged limestone peaks, turquoise glacial rivers, dense lodgepole pine forests"
    },
    {
        "name": "Mexico City, Mexico",
        "lat": 19.4326, "lon": -99.1332,
        "country": "Mexico", "region": "CDMX", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Mexico City, green and white taxi cabs, colonial stone arches, taco street vendors, jacaranda trees, Pemex gas stations, topes speed bumps"
    },
    {
        "name": "Oaxaca, Mexico",
        "lat": 17.0732, "lon": -96.7266,
        "country": "Mexico", "region": "Oaxaca", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Oaxaca Mexico, brightly colored single-story adobe buildings, cobblestone streets, agave cactus plantations on dry hillsides"
    },
    {
        "name": "Rio de Janeiro, Brazil",
        "lat": -22.9068, "lon": -43.1729,
        "country": "Brazil", "region": "Rio de Janeiro", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal avenue in Rio de Janeiro, black and white wave mosaic Copacabana promenade, steep green granite Sugarloaf peaks, favelas on hillsides"
    },
    {
        "name": "São Paulo, Brazil",
        "lat": -23.5505, "lon": -46.6333,
        "country": "Brazil", "region": "São Paulo", "category": "Global", "driving_side": "Right",
        "prompt": "a bustling avenue in São Paulo Brazil, endless sea of concrete residential skyscrapers, concrete utility poles with three horizontal crossarms, red soil"
    },
    {
        "name": "Buenos Aires, Argentina",
        "lat": -34.6037, "lon": -58.3816,
        "country": "Argentina", "region": "Capital Federal", "category": "Global", "driving_side": "Right",
        "prompt": "a wide boulevard in Buenos Aires Argentina, French neoclassical architecture, Obelisco monument, black-and-yellow taxi cabs, purple jacaranda trees"
    },
    {
        "name": "Patagonia, Argentina",
        "lat": -50.3379, "lon": -72.2648,
        "country": "Argentina", "region": "Santa Cruz", "category": "Global", "driving_side": "Right",
        "prompt": "an empty straight gravel highway in Argentine Patagonia, vast dry grassy steppe, Andes mountains in distant horizon, black and white striped road bollards"
    },
    {
        "name": "Santiago, Chile",
        "lat": -33.4489, "lon": -70.6693,
        "country": "Chile", "region": "Santiago Metropolitan", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Santiago Chile, towering snowcapped Andes mountains right behind the modern skyline, white vehicle license plates, clean modern expressways"
    },
    {
        "name": "Bogota, Colombia",
        "lat": 4.7110, "lon": -74.0721,
        "country": "Colombia", "region": "Bogota DC", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Bogota Colombia, red brick architecture, TransMilenio red articulated buses, green Andean mountain ridge overlooking city, yellow taxis"
    },
    {
        "name": "Lima, Peru",
        "lat": -12.0464, "lon": -77.0428,
        "country": "Peru", "region": "Lima", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road in Lima Peru, sheer grey coastal cliffs dropping into Pacific surf, arid treeless hills, colorful mototaxis, overcast garua coastal fog"
    },
    {
        "name": "Cusco, Peru",
        "lat": -13.5319, "lon": -71.9675,
        "country": "Peru", "region": "Cusco", "category": "Global", "driving_side": "Right",
        "prompt": "a cobblestone street in Cusco Peru, ancient precision-cut Inca stone walls, Spanish colonial whitewashed walls with blue wooden balconies, Andes peaks"
    },
    {
        "name": "Montevideo, Uruguay",
        "lat": -34.9011, "lon": -56.1645,
        "country": "Uruguay", "region": "Montevideo", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road along Rambla in Montevideo Uruguay, wide Rio de la Plata estuary, flat grassy plains, eucalyptus trees, people drinking mate gourd"
    },
    {
        "name": "San Jose, Costa Rica",
        "lat": 9.9281, "lon": -84.0907,
        "country": "Costa Rica", "region": "San Jose", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Costa Rica, lush tropical rainforest, green volcanic hills, corrugated iron roof houses, dense tropical flora, eco-tourism signs"
    },

    # --- Oceania ---
    {
        "name": "Sydney, New South Wales, Australia",
        "lat": -33.8688, "lon": 151.2093,
        "country": "Australia", "region": "New South Wales", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Sydney Australia, iconic Opera House and Harbour Bridge, eucalyptus gum trees, sandstone heritage buildings, yellow warning road signs, driving on left"
    },
    {
        "name": "Melbourne, Victoria, Australia",
        "lat": -37.8136, "lon": 144.9631,
        "country": "Australia", "region": "Victoria", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Melbourne Australia, green and yellow street trams, Victorian terrace houses with cast iron lacework, graffiti-covered bluestone laneways, left driving"
    },
    {
        "name": "Australian Outback, Northern Territory, Australia",
        "lat": -23.6980, "lon": 133.8807,
        "country": "Australia", "region": "Northern Territory", "category": "Global", "driving_side": "Left",
        "prompt": "a long straight road through Australian Outback, deep rich red dirt and soil, yellow spinifex grass clumps, stunted mulga trees, endless blue sky, left driving"
    },
    {
        "name": "Auckland, New Zealand",
        "lat": -36.8485, "lon": 174.7633,
        "country": "New Zealand", "region": "Auckland", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Auckland New Zealand, Sky Tower skyline, volcanic hills, pohutukawa trees with red flowers, wooden weatherboard bungalows, driving left"
    },
    {
        "name": "Queenstown, Southern Alps, New Zealand",
        "lat": -45.0312, "lon": 168.6626,
        "country": "New Zealand", "region": "Otago", "category": "Global", "driving_side": "Left",
        "prompt": "a mountain road near Queenstown New Zealand, crystal clear Lake Wakatipu, jagged Remarkables snow peaks, golden tussock grass, driving on left"
    },

    # --- Africa ---
    {
        "name": "Cape Town, South Africa",
        "lat": -33.9249, "lon": 18.4241,
        "country": "South Africa", "region": "Western Cape", "category": "Global", "driving_side": "Left",
        "prompt": "a coastal road in Cape Town South Africa, massive flat-topped Table Mountain backdrop, yellow dashed outer shoulder lines on road, fynbos scrub, driving left"
    },
    {
        "name": "Johannesburg, South Africa",
        "lat": -26.2041, "lon": 28.0473,
        "country": "South Africa", "region": "Gauteng", "category": "Global", "driving_side": "Left",
        "prompt": "a highway in Johannesburg South Africa, tall jacaranda trees with purple blossoms, gold mine dump hills, high security walled residential compounds, driving left"
    },
    {
        "name": "Nairobi, Kenya",
        "lat": -1.2921, "lon": 36.8219,
        "country": "Kenya", "region": "Nairobi", "category": "Global", "driving_side": "Left",
        "prompt": "a road in Nairobi Kenya, colorful customized Matatu minibuses, flat-topped umbrella acacia trees, red soil roadside ditches, driving on left, English signs"
    },
    {
        "name": "Lagos, Nigeria",
        "lat": 6.5244, "lon": 3.3792,
        "country": "Nigeria", "region": "Lagos", "category": "Global", "driving_side": "Right",
        "prompt": "a bustling highway in Lagos Nigeria, bright yellow Danfo commercial minibuses, Third Mainland Bridge, dense market stalls, red earth shoulders"
    },
    {
        "name": "Cairo, Egypt",
        "lat": 30.0444, "lon": 31.2357,
        "country": "Egypt", "region": "Cairo", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Cairo Egypt, unpainted red brick apartment buildings with exposed steel rebar, dusty desert air, Nile river bridges, Arabic calligraphy signs"
    },
    {
        "name": "Marrakech, Morocco",
        "lat": 31.6295, "lon": -7.9811,
        "country": "Morocco", "region": "Marrakech-Safi", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Marrakech Morocco, salmon pink and ochre clay rampart walls, date palm trees, Atlas mountains snow peaks in distance, Arabic and French signs"
    },
    {
        "name": "Dakar, Senegal",
        "lat": 14.7167, "lon": -17.4677,
        "country": "Senegal", "region": "Dakar", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road in Dakar Senegal, colorful Car Rapide buses, sandy Sahelian sidewalks, massive Baobab trees, French language signboards"
    },
    {
        "name": "Accra, Ghana",
        "lat": 5.6037, "lon": -0.1870,
        "country": "Ghana", "region": "Greater Accra", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Accra Ghana, Tro-tro minibuses, yellow license plates, bustling roadside trade stalls, tropical red dirt, open drainage gutters"
    },
    {
        "name": "Gaborone, Botswana",
        "lat": -24.6282, "lon": 25.9231,
        "country": "Botswana", "region": "South-East", "category": "Global", "driving_side": "Left",
        "prompt": "a paved highway in Botswana, flat semi-arid Kalahari bushveld, thorny acacia trees, blue sky, spotless paved roads, driving on left"
    },
    {
        "name": "Tunis, Tunisia",
        "lat": 36.8065, "lon": 10.1815,
        "country": "Tunisia", "region": "Tunis", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Sidi Bou Said Tunis, iconic whitewashed walls with bright blue doors and window shutters, bougainvillea, Mediterranean sea view"
    },

    # --- Middle East & Central Asia ---
    {
        "name": "Dubai, United Arab Emirates",
        "lat": 25.2048, "lon": 55.2708,
        "country": "United Arab Emirates", "region": "Dubai", "category": "Global", "driving_side": "Right",
        "prompt": "Sheikh Zayed Road in Dubai UAE, ultra-modern gleaming glass skyscrapers, Burj Khalifa, multi-lane immaculate highway, manicured date palms, desert sunshine"
    },
    {
        "name": "Riyadh, Saudi Arabia",
        "lat": 24.7136, "lon": 46.6753,
        "country": "Saudi Arabia", "region": "Riyadh", "category": "Global", "driving_side": "Right",
        "prompt": "a wide expressway in Riyadh Saudi Arabia, Kingdom Centre tower, dry golden sand dunes, palm trees along central reservation, Arabic highway signs"
    },
    {
        "name": "Doha, Qatar",
        "lat": 25.2854, "lon": 51.5310,
        "country": "Qatar", "region": "Doha", "category": "Global", "driving_side": "Right",
        "prompt": "Corniche waterfront street in Doha Qatar, traditional wooden dhow boats in bay, futuristic West Bay glass skyscrapers, limestone promenades"
    },
    {
        "name": "Muscat, Oman",
        "lat": 23.5880, "lon": 58.3829,
        "country": "Oman", "region": "Muscat", "category": "Global", "driving_side": "Right",
        "prompt": "a pristine boulevard in Muscat Oman, gleaming white low-rise Arab architecture, dramatic jagged brown barren mountains backdrop, ornate streetlights"
    },
    {
        "name": "Amman & Petra, Jordan",
        "lat": 31.9539, "lon": 35.9106,
        "country": "Jordan", "region": "Amman", "category": "Global", "driving_side": "Right",
        "prompt": "a desert road in Jordan, rolling hills with pale stone houses, ancient red sandstone canyon cliffs of Petra, Bedouin tents, arid landscape"
    },
    {
        "name": "Jerusalem",
        "lat": 31.7683, "lon": 35.2137,
        "country": "Israel", "region": "Jerusalem", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Jerusalem, distinctive golden-yellow Jerusalem stone buildings, olive trees, arched stone alleyways, Hebrew and Arabic street signs"
    },
    {
        "name": "Almaty, Kazakhstan",
        "lat": 43.2220, "lon": 76.8512,
        "country": "Kazakhstan", "region": "Almaty", "category": "Global", "driving_side": "Right",
        "prompt": "a broad street in Almaty Kazakhstan, towering snow-capped Tian Shan mountain range right behind the city, wide tree-lined sidewalks, Cyrillic Kazakh signs"
    },
    {
        "name": "Ulaanbaatar, Mongolia",
        "lat": 47.8864, "lon": 106.9057,
        "country": "Mongolia", "region": "Ulaanbaatar", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Mongolia, endless treeless rolling green steppe under an immense blue sky, traditional felt yurt ger tents, dirt double-track trails, horses"
    }
]