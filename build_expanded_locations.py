# ==============================================================================
# Comprehensive Global and Hyper-Local GeoGuessr Location Database Builder
# Combines existing locations with extensive global, pan-India, and regional places
# Every entry includes precise GPS coordinates, driving side, and micro-clue prompts
# ==============================================================================

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from locations import LOCATIONS as EXISTING_LOCATIONS

# Additional Global, Regional, and Micro-Regional Locations with Rich Micro-Clues
NEW_LOCATIONS = [
    # ==========================================================================
    # 1. UNITED STATES — MAJOR STATES & ECOREGIONS
    # ==========================================================================
    {
        "name": "California - Pacific Coast Highway, Big Sur, United States",
        "lat": 36.2704, "lon": -121.8081,
        "country": "United States", "region": "California", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal highway photo in Big Sur California, rugged ocean cliffs, double yellow center line, eucalyptus and cypress trees, sunny coastal haze, wooden guardrails, US route shields"
    },
    {
        "name": "California - Yosemite Valley, United States",
        "lat": 37.7456, "lon": -119.5936,
        "country": "United States", "region": "California", "category": "Global", "driving_side": "Right",
        "prompt": "a mountain road in Yosemite National Park California, towering granite monoliths El Capitan, pine and cedar conifer trees, double yellow lines, asphalt pavement, national park wooden signs"
    },
    {
        "name": "Texas - Hill Country, Austin, United States",
        "lat": 30.2672, "lon": -97.7431,
        "country": "United States", "region": "Texas", "category": "Global", "driving_side": "Right",
        "prompt": "a rural road in Texas Hill Country, live oak trees, limestone caliche rocks, wide paved shoulders, double yellow lines, cedar shrubs, blue Texas sky, pickup trucks"
    },
    {
        "name": "Texas - West Texas High Desert, Marfa, United States",
        "lat": 30.3094, "lon": -104.0210,
        "country": "United States", "region": "Texas", "category": "Global", "driving_side": "Right",
        "prompt": "a long straight highway in West Texas, desert scrub, yucca and agave plants, flat arid plateau, wide asphalt with rumble strips, distant mountain silhouettes"
    },
    {
        "name": "Florida - Overseas Highway, Florida Keys, United States",
        "lat": 24.7136, "lon": -81.0847,
        "country": "United States", "region": "Florida", "category": "Global", "driving_side": "Right",
        "prompt": "a road bridge in the Florida Keys, turquoise shallow ocean on both sides, concrete barrier walls, palm trees, flat horizon, bright humid tropical sun"
    },
    {
        "name": "Florida - Miami Beach & Art Deco District, United States",
        "lat": 25.7907, "lon": -80.1300,
        "country": "United States", "region": "Florida", "category": "Global", "driving_side": "Right",
        "prompt": "an urban coastal street in Miami Beach, pastel Art Deco architecture, royal palm trees, white concrete curbs, convertible cars, bright sunny Florida sky"
    },
    {
        "name": "Washington - Olympic Peninsula Rainforest, United States",
        "lat": 47.8021, "lon": -123.6044,
        "country": "United States", "region": "Washington", "category": "Global", "driving_side": "Right",
        "prompt": "a road through temperate rainforest in Washington state, moss-covered towering Douglas firs and western red cedars, ferns, damp asphalt, overcast misty sky, green highway signs"
    },
    {
        "name": "Colorado - Rocky Mountain Pass, Trail Ridge Road, United States",
        "lat": 40.4300, "lon": -105.7500,
        "country": "United States", "region": "Colorado", "category": "Global", "driving_side": "Right",
        "prompt": "a high alpine mountain pass road in Colorado, rocky tundra above tree line, snow patches, wooden reflector posts, sharp mountain peaks, deep blue sky"
    },
    {
        "name": "Arizona - Red Rock Country, Sedona, United States",
        "lat": 34.8697, "lon": -111.7610,
        "country": "United States", "region": "Arizona", "category": "Global", "driving_side": "Right",
        "prompt": "a highway in Sedona Arizona, vibrant red sandstone buttes and mesas, juniper trees, arid soil, double yellow lines, sunny desert atmosphere"
    },
    {
        "name": "Arizona - Sonoran Desert & Saguaro, Tucson, United States",
        "lat": 32.2226, "lon": -110.9747,
        "country": "United States", "region": "Arizona", "category": "Global", "driving_side": "Right",
        "prompt": "a desert road in Arizona with giant Saguaro cactus, cholla cactus, creosote bushes, dry gravel soil, rugged desert hills in background, pale clear blue sky"
    },
    {
        "name": "Hawaii - Hana Highway, Maui, United States",
        "lat": 20.7984, "lon": -156.0062,
        "country": "United States", "region": "Hawaii", "category": "Global", "driving_side": "Right",
        "prompt": "a winding tropical coastal road on Maui Hawaii, lush jungle greenery, black basalt volcanic rock, banana and breadfruit trees, one-lane historic bridges, humid Pacific sea air"
    },
    {
        "name": "Hawaii - Volcanoes National Park, Big Island, United States",
        "lat": 19.4194, "lon": -155.2885,
        "country": "United States", "region": "Hawaii", "category": "Global", "driving_side": "Right",
        "prompt": "a paved road through black pahoehoe lava fields in Hawaii, steam vents, ohia lehua trees, dark volcanic rock, ocean horizon"
    },
    {
        "name": "Alaska - Seward Highway & Fjord, United States",
        "lat": 60.9500, "lon": -149.3000,
        "country": "United States", "region": "Alaska", "category": "Global", "driving_side": "Right",
        "prompt": "a scenic highway in Alaska along Turnagain Arm, dramatic snow-capped Chugach mountains, tidal mudflats, spruce forests, wide asphalt with gravel shoulders, cool northern light"
    },
    {
        "name": "Illinois - Downtown Chicago & The Loop, United States",
        "lat": 41.8781, "lon": -87.6298,
        "country": "United States", "region": "Illinois", "category": "Global", "driving_side": "Right",
        "prompt": "a street view in downtown Chicago, elevated 'L' train metal tracks overhead, historic limestone skyscrapers, Lake Michigan breeze, yellow traffic lights, Chicago grid layout"
    },
    {
        "name": "Louisiana - New Orleans French Quarter, United States",
        "lat": 29.9584, "lon": -90.0644,
        "country": "United States", "region": "Louisiana", "category": "Global", "driving_side": "Right",
        "prompt": "a street in the French Quarter New Orleans, ornate cast-iron wrought balcony railings, colorful Creole townhouses, cobblestone gutters, gas lamps, hanging ferns"
    },
    {
        "name": "Massachusetts - Boston Historic Beacon Hill, United States",
        "lat": 42.3588, "lon": -71.0707,
        "country": "United States", "region": "Massachusetts", "category": "Global", "driving_side": "Right",
        "prompt": "a narrow historic street in Boston Beacon Hill, red brick townhouses, cobblestone pavement, antique gas street lamps, black wrought iron fences, leafy elms"
    },
    {
        "name": "Utah - Red Rock Canyons, Moab, United States",
        "lat": 38.5733, "lon": -109.5498,
        "country": "United States", "region": "Utah", "category": "Global", "driving_side": "Right",
        "prompt": "a desert highway in Moab Utah, dramatic towering red sandstone arches and cliffs, juniper bushes, double yellow lines, arid red dirt, blue sky"
    },
    {
        "name": "Nevada - Las Vegas Strip & Mojave Desert, United States",
        "lat": 36.1147, "lon": -115.1728,
        "country": "United States", "region": "Nevada", "category": "Global", "driving_side": "Right",
        "prompt": "a wide multi-lane boulevard in Las Vegas Nevada, towering casino resorts, illuminated mega billboards, palm trees, mountain backdrop across flat Mojave desert"
    },
    {
        "name": "Oregon - Pacific Northwest Coast, Cannon Beach, United States",
        "lat": 45.8918, "lon": -123.9615,
        "country": "United States", "region": "Oregon", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road along Cannon Beach Oregon, towering sea stacks Haystack Rock, misty marine layer, dense Sitka spruce and cedar forests, driftwood"
    },

    # ==========================================================================
    # 2. CANADA — PROVINCES & HIGHWAYS
    # ==========================================================================
    {
        "name": "Canada - Banff National Park, Alberta",
        "lat": 51.1784, "lon": -115.5708,
        "country": "Canada", "region": "Alberta", "category": "Global", "driving_side": "Right",
        "prompt": "a scenic highway in Banff Alberta, towering snow-covered Canadian Rocky Mountains, turquoise glacier river, pine forests, animal overpass bridge, green highway signs in English and French"
    },
    {
        "name": "Canada - Vancouver Sea to Sky Highway, British Columbia",
        "lat": 49.6953, "lon": -123.1558,
        "country": "Canada", "region": "British Columbia", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal fjord highway in British Columbia, Howe Sound deep blue water, steep forested granite mountains, modern concrete barriers, evergreen conifers"
    },
    {
        "name": "Canada - Old Montreal Historic District, Quebec",
        "lat": 45.5074, "lon": -73.5545,
        "country": "Canada", "region": "Quebec", "category": "Global", "driving_side": "Right",
        "prompt": "a historic cobblestone street in Old Montreal Quebec, grey greystone heritage buildings, French road signs 'ARRÊT', wrought iron lampposts, European colonial atmosphere"
    },
    {
        "name": "Canada - Toronto Downtown & Financial District, Ontario",
        "lat": 43.6532, "lon": -79.3832,
        "country": "Canada", "region": "Ontario", "category": "Global", "driving_side": "Right",
        "prompt": "a modern downtown avenue in Toronto, CN Tower visible in background, red TTC streetcars on tracks, high-rise glass bank towers, Canadian flags"
    },
    {
        "name": "Canada - Cabot Trail, Cape Breton, Nova Scotia",
        "lat": 46.8000, "lon": -60.8000,
        "country": "Canada", "region": "Nova Scotia", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal cliff highway in Cape Breton Nova Scotia, Atlantic Ocean vistas, deciduous maple and birch trees, rolling green highlands, fishing villages"
    },

    # ==========================================================================
    # 3. LATIN AMERICA & CARIBBEAN
    # ==========================================================================
    {
        "name": "Mexico - Mexico City Historic Center & Reforma",
        "lat": 19.4326, "lon": -99.1332,
        "country": "Mexico", "region": "Federal District", "category": "Global", "driving_side": "Right",
        "prompt": "a wide grand avenue Paseo de la Reforma Mexico City, modern glass towers, jacaranda trees with purple blossoms, Spanish signage, pink and white CDMX taxis"
    },
    {
        "name": "Mexico - Oaxaca Colonial Town & Highlands",
        "lat": 17.0732, "lon": -96.7266,
        "country": "Mexico", "region": "Oaxaca", "category": "Global", "driving_side": "Right",
        "prompt": "a colonial street in Oaxaca Mexico, green cantera stone buildings, colorful stucco facades, cobblestone streets, agave plants on surrounding hillsides, Spanish signs"
    },
    {
        "name": "Mexico - Yucatan Peninsula & Maya Coast",
        "lat": 20.6843, "lon": -88.5678,
        "country": "Mexico", "region": "Yucatan", "category": "Global", "driving_side": "Right",
        "prompt": "a flat road through low tropical scrub in Yucatan Mexico, white limestone soil, cenote vegetation, single-story colorful village houses, topes speed bumps"
    },
    {
        "name": "Brazil - São Paulo Paulista Avenue",
        "lat": -23.5615, "lon": -46.6559,
        "country": "Brazil", "region": "São Paulo", "category": "Global", "driving_side": "Right",
        "prompt": "a massive urban boulevard Avenida Paulista São Paulo, high-rise office towers, MASP museum red pillars, Portuguese street signs, black-and-white wave patterned mosaic sidewalks"
    },
    {
        "name": "Brazil - Salvador Pelourinho, Bahia",
        "lat": -12.9714, "lon": -38.5114,
        "country": "Brazil", "region": "Bahia", "category": "Global", "driving_side": "Right",
        "prompt": "a steep historic cobblestone street in Pelourinho Salvador Bahia, vibrant pastel colonial houses, baroque church towers, Afro-Brazilian culture, tropical humid sea breeze"
    },
    {
        "name": "Brazil - Parana Pine Forests, Curitiba",
        "lat": -25.4284, "lon": -49.2733,
        "country": "Brazil", "region": "Parana", "category": "Global", "driving_side": "Right",
        "prompt": "a road in southern Brazil surrounded by distinctive Araucaria candelabra pine trees, rolling green hills, red laterite soil, European style houses, cool subtropical air"
    },
    {
        "name": "Argentina - Buenos Aires Avenida 9 de Julio",
        "lat": -34.6037, "lon": -58.3816,
        "country": "Argentina", "region": "Buenos Aires", "category": "Global", "driving_side": "Right",
        "prompt": "the widest avenue in the world 9 de Julio Buenos Aires, iconic white Obelisk in center, grand French-style Haussmann architecture, jacaranda trees, yellow-and-black taxis"
    },
    {
        "name": "Argentina - Patagonia Andes & Lakes, Bariloche",
        "lat": -41.1335, "lon": -71.3103,
        "country": "Argentina", "region": "Rio Negro", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Bariloche Argentina, deep blue glacial lake Nahuel Huapi, alpine wooden and stone chalets, snow-capped Andes mountains, cypress and coihue trees"
    },
    {
        "name": "Chile - Atacama Desert & Salt Flats, San Pedro",
        "lat": -22.9087, "lon": -68.1997,
        "country": "Chile", "region": "Antofagasta", "category": "Global", "driving_side": "Right",
        "prompt": "an ultra-dry highway across the Atacama Desert Chile, Licancabur volcano in background, bone-dry brown salt crust soil, white roadside kilometer posts, clear high-altitude skies"
    },
    {
        "name": "Chile - Santiago Downtown & Andes Backdrop",
        "lat": -33.4489, "lon": -70.6693,
        "country": "Chile", "region": "Metropolitana", "category": "Global", "driving_side": "Right",
        "prompt": "an urban highway in Santiago Chile, Costanera Center skyscraper, dramatic towering snow-covered Andes mountain wall immediately behind city, Spanish signage"
    },
    {
        "name": "Colombia - Medellin & Antioquia Mountain Slopes",
        "lat": 6.2442, "lon": -75.5812,
        "country": "Colombia", "region": "Antioquia", "category": "Global", "driving_side": "Right",
        "prompt": "a steep road overlooking the Aburra Valley in Medellin Colombia, Metrocable gondolas overhead, red brick multi-story houses, lush green Andes mountains, yellow taxi plates"
    },
    {
        "name": "Colombia - Cartagena Colonial Walled City",
        "lat": 10.4241, "lon": -75.5479,
        "country": "Colombia", "region": "Bolivar", "category": "Global", "driving_side": "Right",
        "prompt": "a colonial street inside the walled city of Cartagena Colombia, bougainvillea flowers overflowing wooden balconies, colorful colonial architecture, stone fortification walls, Caribbean sun"
    },
    {
        "name": "Peru - Cusco Historic Inca & Colonial Streets",
        "lat": -13.5319, "lon": -71.9675,
        "country": "Peru", "region": "Cusco", "category": "Global", "driving_side": "Right",
        "prompt": "a narrow cobblestone street in Cusco Peru, ancient precision-carved Inca polygonal stone walls, whitewashed Spanish colonial upper balconies, red tile roofs, Andean altitude"
    },
    {
        "name": "Uruguay - Montevideo Rambla Coastal Promenade",
        "lat": -34.9011, "lon": -56.1645,
        "country": "Uruguay", "region": "Montevideo", "category": "Global", "driving_side": "Right",
        "prompt": "a wide coastal promenade Rambla in Montevideo Uruguay, Rio de la Plata river beach, mid-century apartment buildings, mate gourds held by locals, Spanish signs"
    },
    {
        "name": "Costa Rica - Monteverde Cloud Forest & Hills",
        "lat": 10.3060, "lon": -84.8159,
        "country": "Costa Rica", "region": "Puntarenas", "category": "Global", "driving_side": "Right",
        "prompt": "a gravel or paved mountain road in Costa Rica, dense tropical cloud forest, hanging vines, tree ferns, mist and fog, green road signs, lush biodiversity"
    },

    # ==========================================================================
    # 4. EUROPE — EXPANDED REGIONAL CLUES
    # ==========================================================================
    {
        "name": "United Kingdom - Scottish Highlands & Glencoe",
        "lat": 56.6826, "lon": -5.1023,
        "country": "United Kingdom", "region": "Scotland", "category": "Global", "driving_side": "Left",
        "prompt": "a single-track road in Glencoe Scottish Highlands, dramatic rocky glens and mountains, peat moss and heather, passing places, stone bridges, overcast Scottish skies, yellow rear license plates"
    },
    {
        "name": "United Kingdom - Edinburgh Old Town & Royal Mile",
        "lat": 55.9533, "lon": -3.1883,
        "country": "United Kingdom", "region": "Scotland", "category": "Global", "driving_side": "Left",
        "prompt": "a historic cobblestone street on Edinburgh Royal Mile, towering dark sandstone medieval tenements, Edinburgh Castle in distance, red double-decker buses, left-hand drive"
    },
    {
        "name": "Ireland - Ring of Kerry & Coastal Cliffs",
        "lat": 51.9960, "lon": -9.7420,
        "country": "Ireland", "region": "Kerry", "category": "Global", "driving_side": "Left",
        "prompt": "a narrow rural road in County Kerry Ireland, lush green sheep pastures with dry stone wall fences, wild fuchsia hedges, rugged Atlantic coast, yellow diamond warning signs, left-hand drive"
    },
    {
        "name": "France - Provence Lavender & Olive Country",
        "lat": 43.9298, "lon": 5.2530,
        "country": "France", "region": "Provence", "category": "Global", "driving_side": "Right",
        "prompt": "a country road in Provence France, rows of purple lavender fields, olive groves, cypress trees, stone mas country farmhouses, white bollards with red reflector rings, bright Mediterranean sun"
    },
    {
        "name": "France - Normandy Coast & Half-Timbered Villages",
        "lat": 49.3600, "lon": 0.0700,
        "country": "France", "region": "Normandy", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Normandy France, half-timbered colombage houses with thatched roofs, apple orchards, hedgerows (bocage), chalk cliffs of Etretat, mild oceanic climate"
    },
    {
        "name": "France - French Riviera, Nice & Monaco Coast",
        "lat": 43.7102, "lon": 7.2620,
        "country": "France", "region": "Côte d'Azur", "category": "Global", "driving_side": "Right",
        "prompt": "Promenade des Anglais along the Mediterranean in Nice France, azure blue sea, palm trees, white Belle Époque palaces and hotels, smooth asphalt with cycling lane"
    },
    {
        "name": "Germany - Black Forest (Schwarzwald) Scenic Byway",
        "lat": 48.1800, "lon": 8.1600,
        "country": "Germany", "region": "Baden-Württemberg", "category": "Global", "driving_side": "Right",
        "prompt": "a winding road through dense dark spruce and fir forests in the German Black Forest, traditional timber farmhouses with sloping roofs, wooden roadside guardrails, clean asphalt, German road signs"
    },
    {
        "name": "Germany - Rhine River Valley & Castles",
        "lat": 50.1500, "lon": 7.7100,
        "country": "Germany", "region": "Rhineland-Palatinate", "category": "Global", "driving_side": "Right",
        "prompt": "a riverside road along the Rhine Gorge Germany, steep terraced vineyards on hillsides, medieval hilltop castles, half-timbered villages, river barges on water"
    },
    {
        "name": "Italy - Tuscany Val d'Orcia & Cypress Roads",
        "lat": 43.0642, "lon": 11.6067,
        "country": "Italy", "region": "Tuscany", "category": "Global", "driving_side": "Right",
        "prompt": "a dirt or paved country road lined with iconic slender Italian cypress trees, rolling golden hills of Val d'Orcia Tuscany, stone farmhouse on hilltop, vineyards, warm Italian light"
    },
    {
        "name": "Italy - Amalfi Coast Cliff Highway",
        "lat": 40.6340, "lon": 14.6027,
        "country": "Italy", "region": "Campania", "category": "Global", "driving_side": "Right",
        "prompt": "a narrow cliffside coastal road in Amalfi Coast Italy, sheer limestone drop down to Mediterranean sea, colorful pastel cliffside houses in Positano, bougainvillea, Vespa scooters"
    },
    {
        "name": "Spain - Andalusia White Villages (Pueblos Blancos)",
        "lat": 36.7462, "lon": -5.1612,
        "country": "Spain", "region": "Andalusia", "category": "Global", "driving_side": "Right",
        "prompt": "a road approaching a whitewashed hill town in Andalusia Spain, olive groves, arid red-brown soil, terracotta tile roofs, bright Mediterranean sunlight, Spanish road markers with yellow borders"
    },
    {
        "name": "Spain - Barcelona Eixample District, Catalonia",
        "lat": 41.3879, "lon": 2.1699,
        "country": "Spain", "region": "Catalonia", "category": "Global", "driving_side": "Right",
        "prompt": "an urban boulevard in Barcelona Eixample, octagonal street intersections, Modernisme architecture, plane trees, wide sidewalks with floral tiles, black-and-yellow taxis"
    },
    {
        "name": "Portugal - Lisbon Alfama & Tram Lines",
        "lat": 38.7118, "lon": -9.1300,
        "country": "Portugal", "region": "Lisbon", "category": "Global", "driving_side": "Right",
        "prompt": "a steep cobblestone street in Lisbon Alfama, yellow tram tracks, historic yellow electric tram 28, blue and white azulejo ceramic tile facades, wrought iron balconies with laundry drying"
    },
    {
        "name": "Portugal - Algarve Golden Coast & Sea Caves",
        "lat": 37.0891, "lon": -8.2479,
        "country": "Portugal", "region": "Algarve", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road in Algarve Portugal, golden ochre limestone cliffs and arches, turquoise Atlantic ocean, whitewashed coastal villas with terracotta roofs, umbrella pine trees"
    },
    {
        "name": "Norway - Lofoten Islands Arctic Archipelago",
        "lat": 68.1667, "lon": 13.7500,
        "country": "Norway", "region": "Nordland", "category": "Global", "driving_side": "Right",
        "prompt": "a scenic Arctic road in Lofoten Norway, dramatic jagged granite peaks rising directly from Arctic ocean, red wooden rorbu fisherman cabins on stilts, drying codfish racks, pristine asphalt"
    },
    {
        "name": "Norway - Geirangerfjord & Western Fjords",
        "lat": 62.1000, "lon": 7.2000,
        "country": "Norway", "region": "Møre og Romsdal", "category": "Global", "driving_side": "Right",
        "prompt": "a hairpin switchback road Trollstigen overlooking Geirangerfjord Norway, deep blue fjord with waterfalls Seven Sisters, green mountain slopes, modern wooden and stone guardrails"
    },
    {
        "name": "Sweden - Stockholm Archipelago & Gamla Stan",
        "lat": 59.3293, "lon": 18.0686,
        "country": "Sweden", "region": "Stockholm", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Stockholm Gamla Stan, warm yellow and ochre 17th-century townhouses, cobblestones, waterfront quays with ferries, clean Scandinavian street signs"
    },
    {
        "name": "Finland - Lakeland & Taiga Birch Forests",
        "lat": 61.5000, "lon": 27.5000,
        "country": "Finland", "region": "South Savo", "category": "Global", "driving_side": "Right",
        "prompt": "a straight paved highway through Finnish Lakeland, dense white silver birch and Scots pine taiga forest, blue lake glimpses between trees, red wooden summer cottages (mökki), yellow center lines"
    },
    {
        "name": "Iceland - Vik Black Sand Beach & Basalt Highway",
        "lat": 63.4186, "lon": -19.0060,
        "country": "Iceland", "region": "Southern Region", "category": "Global", "driving_side": "Right",
        "prompt": "Iceland Ring Road Route 1 near Vik, black volcanic basalt sand beach, Reynisdrangar sea stacks, mossy green volcanic mountains, yellow roadside marker posts, treeless Arctic landscape"
    },
    {
        "name": "Poland - Krakow Old Town & Market Square",
        "lat": 50.0614, "lon": 19.9366,
        "country": "Poland", "region": "Lesser Poland", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Krakow Old Town Poland, Gothic brick St Mary's Basilica, Renaissance Cloth Hall, horse-drawn white carriages on cobblestones, Polish road signs"
    },
    {
        "name": "Czech Republic - Prague Charles Bridge & Old Town",
        "lat": 50.0875, "lon": 14.4208,
        "country": "Czech Republic", "region": "Prague", "category": "Global", "driving_side": "Right",
        "prompt": "a historic cobblestone street in Prague Czechia, red and white Tatra trams on tracks, baroque and gothic spires, Vltava river views, distinctive red street sign plates with white text"
    },
    {
        "name": "Hungary - Budapest Danube Promenade & Parliament",
        "lat": 47.4979, "lon": 19.0402,
        "country": "Hungary", "region": "Budapest", "category": "Global", "driving_side": "Right",
        "prompt": "Danube river embankment in Budapest Hungary, neo-Gothic Hungarian Parliament building, Chain Bridge with stone lions, yellow historic streetcars, Austro-Hungarian grandeur"
    },
    {
        "name": "Romania - Transfagarasan Alpine Highway, Transylvania",
        "lat": 45.5997, "lon": 24.6214,
        "country": "Romania", "region": "Transylvania", "category": "Global", "driving_side": "Right",
        "prompt": "a winding alpine mountain highway Transfagarasan in Romania, dramatic hairpin switchbacks across the Fagaras Southern Carpathians, rocky alpine tundra, concrete tunnels and viaducts"
    },
    {
        "name": "Greece - Santorini Island & Caldera Cliffs",
        "lat": 36.3932, "lon": 25.4615,
        "country": "Greece", "region": "South Aegean", "category": "Global", "driving_side": "Right",
        "prompt": "a narrow pedestrian street in Oia Santorini Greece, iconic whitewashed cave houses, cobalt blue church domes, volcanic caldera sea cliff drop, Aegean blue water, pink bougainvillea"
    },
    {
        "name": "Croatia - Dubrovnik Old Town & Adriatic Coast",
        "lat": 42.6412, "lon": 18.1084,
        "country": "Croatia", "region": "Dubrovnik-Neretva", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal highway above Dubrovnik Croatia, ancient medieval limestone city walls, terracotta tile roofs, sparkling sapphire Adriatic sea, cypress and olive trees"
    },
    {
        "name": "Turkey - Cappadocia Fairy Chimneys & Valleys",
        "lat": 38.6431, "lon": 34.8289,
        "country": "Turkey", "region": "Central Anatolia", "category": "Global", "driving_side": "Right",
        "prompt": "a road in Cappadocia Turkey, surreal conical volcanic tuff rock formations fairy chimneys, hot air balloons in morning sky, dry Anatolian plateau, cave houses"
    },

    # ==========================================================================
    # 5. ASIA & OCEANIA — EXPANDED REGIONAL CLUES
    # ==========================================================================
    {
        "name": "Japan - Hokkaido Furano Fields & Snow Country",
        "lat": 43.3418, "lon": 142.3832,
        "country": "Japan", "region": "Hokkaido", "category": "Global", "driving_side": "Left",
        "prompt": "a rural road in Hokkaido Japan, overhead downward-pointing arrows (yahazu) for snow marking, rolling farmland fields, distant Tokachi volcanic mountains, left-hand drive, white-and-red guide posts"
    },
    {
        "name": "Japan - Osaka Dotonbori Canal & Minami",
        "lat": 34.6687, "lon": 135.5013,
        "country": "Japan", "region": "Osaka", "category": "Global", "driving_side": "Left",
        "prompt": "a vibrant canal street in Dotonbori Osaka, giant mechanical crab sign, Glico running man illuminated billboard, pedestrian bridges over canal, dense Japanese kanji and katakana signage"
    },
    {
        "name": "Japan - Mount Fuji Scenic Byway, Shizuoka",
        "lat": 35.3606, "lon": 138.7274,
        "country": "Japan", "region": "Chubu", "category": "Global", "driving_side": "Left",
        "prompt": "a pristine Japanese road with snow-capped Mount Fuji towering in background, green tea plantations, overhead utility poles with wire transformers, left-hand drive, yellow license plates on kei cars"
    },
    {
        "name": "South Korea - Busan Haeundae Beach & Bridges",
        "lat": 35.1587, "lon": 129.1604,
        "country": "South Korea", "region": "Busan", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal highway in Busan South Korea, Gwangan suspension bridge over ocean, high-rise luxury apartments along Haeundae beach, Hangul road signage, blue lane markings for buses"
    },
    {
        "name": "Taiwan - Taroko Gorge Marble Canyon Highway",
        "lat": 24.1593, "lon": 121.6214,
        "country": "Taiwan", "region": "Hualien", "category": "Global", "driving_side": "Right",
        "prompt": "a highway carved into sheer vertical marble cliffs in Taroko Gorge Taiwan, Liwu river canyon below, road tunnels carved through rock, tropical ferns, Traditional Chinese road signs"
    },
    {
        "name": "Thailand - Chiang Mai Old City & Northern Hills",
        "lat": 18.7883, "lon": 98.9853,
        "country": "Thailand", "region": "Chiang Mai", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Chiang Mai Thailand, historic brick city moat, gilded Buddhist temple wats with multi-tiered roofs, red songthaew shared taxis, Thai script signboards, left-hand drive"
    },
    {
        "name": "Indonesia - Bali Ubud Rice Terraces & Hindu Gates",
        "lat": -8.5069, "lon": 115.2625,
        "country": "Indonesia", "region": "Bali", "category": "Global", "driving_side": "Left",
        "prompt": "a narrow road through Tegalalang rice terraces in Ubud Bali, coconut palms, carved stone split candi bentar temple gates, black volcanic stone shrines with checkered poleng cloth, left-hand drive"
    },
    {
        "name": "Vietnam - Hanoi Old Quarter & French Colonial",
        "lat": 21.0333, "lon": 105.8500,
        "country": "Vietnam", "region": "Hanoi", "category": "Global", "driving_side": "Right",
        "prompt": "a dense street in Hanoi Old Quarter Vietnam, sea of motorbikes, French colonial yellow shuttered buildings, tangled overhead electrical cables, street food stalls on sidewalks, Vietnamese text with diacritics"
    },
    {
        "name": "Australia - Melbourne Great Ocean Road, Victoria",
        "lat": -38.6800, "lon": 143.1000,
        "country": "Australia", "region": "Victoria", "category": "Global", "driving_side": "Left",
        "prompt": "a coastal road Great Ocean Road Victoria Australia, Twelve Apostles limestone sea stacks in rough Southern Ocean, eucalyptus gum trees, white guide posts with red reflectors, left-hand drive"
    },
    {
        "name": "Australia - Outback Red Dirt Highway, Northern Territory",
        "lat": -25.3444, "lon": 131.0369,
        "country": "Australia", "region": "Northern Territory", "category": "Global", "driving_side": "Left",
        "prompt": "a remote straight highway through Australian outback, vibrant red iron oxide dirt on road shoulders, spinifex grass, desert mulga scrub, massive red monolith Uluru in distance, cattle road train signs"
    },
    {
        "name": "New Zealand - Queenstown & Lake Wakatipu, South Island",
        "lat": -45.0312, "lon": 168.6626,
        "country": "New Zealand", "region": "Otago", "category": "Global", "driving_side": "Left",
        "prompt": "a lakeside road in Queenstown New Zealand, deep glacial Lake Wakatipu, dramatic jagged Remarkables mountain range, lupin flowers along shoulder, left-hand drive, white wooden marker posts"
    },

    # ==========================================================================
    # 6. AFRICA — ICONIC CLIMATE & ROAD SCENES
    # ==========================================================================
    {
        "name": "Morocco - Marrakech Medina & Koutoubia",
        "lat": 31.6295, "lon": -7.9811,
        "country": "Morocco", "region": "Marrakech-Safi", "category": "Global", "driving_side": "Right",
        "prompt": "an avenue in Marrakech Morocco, terracotta red-pink clay walls, date palm trees, Koutoubia minaret tower, snow-capped Atlas mountains in distance, Arabic and French signage"
    },
    {
        "name": "Kenya - Great Rift Valley & Savanna Highway",
        "lat": -0.9167, "lon": 36.4167,
        "country": "Kenya", "region": "Rift Valley", "category": "Global", "driving_side": "Left",
        "prompt": "a highway in the Kenyan Rift Valley, acacia thorn trees, dry golden savanna grass, Mount Longonot volcanic crater, Google car with black snorkel visible, left-hand drive, yellow line markings"
    },
    {
        "name": "Ghana - Coastal Highway & Tropics, Cape Coast",
        "lat": 5.1054, "lon": -1.2466,
        "country": "Ghana", "region": "Central", "category": "Global", "driving_side": "Right",
        "prompt": "a highway in southern Ghana, lush tropical vegetation, red laterite roadside dirt, Google car with black snorkel and yellow tape on roof bars, tro-tro minibuses with religious slogans"
    },
    {
        "name": "Senegal - Dakar Ocean Peninsula & Baobabs",
        "lat": 14.7167, "lon": -17.4677,
        "country": "Senegal", "region": "Dakar", "category": "Global", "driving_side": "Right",
        "prompt": "a coastal road in Senegal, distinctive massive baobab trees with thick trunks, sandy coastal soil, African Renaissance Monument, colorful Car Rapide buses, Google car with roof rifts"
    },
    {
        "name": "South Africa - Cape Peninsula & Chapman's Peak Drive",
        "lat": -34.0883, "lon": 18.3614,
        "country": "South Africa", "region": "Western Cape", "category": "Global", "driving_side": "Left",
        "prompt": "a breathtaking coastal cliff road Chapman's Peak South Africa, vertical granite cliffs, crashing Atlantic ocean below, fynbos protea vegetation, left-hand drive, yellow edge line markings"
    },

    # ==========================================================================
    # 7. PAN-INDIA — EXPANDED STATES & CULTURAL HUBS
    # ==========================================================================
    {
        "name": "Tamil Nadu - Ooty Nilgiri Tea Hills & Toy Train",
        "lat": 11.4102, "lon": 76.6950,
        "country": "India", "region": "Tamil Nadu", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain road in Ooty Tamil Nadu, steep Nilgiri blue hills, terraced green tea estates, eucalyptus groves, narrow gauge railway track, cool misty mountain air, Tamil shop signs"
    },
    {
        "name": "Tamil Nadu - Kanyakumari Ocean Confluence & Memorial",
        "lat": 8.0883, "lon": 77.5385,
        "country": "India", "region": "Tamil Nadu", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "the southern tip of India at Kanyakumari, confluence of Arabian Sea, Bay of Bengal and Indian Ocean, Vivekananda Rock Memorial and Thiruvalluvar stone statue off shore, coastal breeze"
    },
    {
        "name": "Karnataka - Coorg (Kodagu) Coffee Plantations & Rain",
        "lat": 12.3375, "lon": 75.8069,
        "country": "India", "region": "Karnataka", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a winding hill road through Coorg Karnataka, shaded arabica coffee estates under silver oak trees, black pepper vines clinging to tree trunks, mist and monsoon rain, Kannada signage"
    },
    {
        "name": "Karnataka - Gokarna Coastal Cliffs & Western Ghats",
        "lat": 14.5426, "lon": 74.3188,
        "country": "India", "region": "Karnataka", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a coastal road in Gokarna Karnataka, red laterite rocky cliffs overlooking Arabian Sea beaches Om beach, palm trees, tiled roof houses, Kannada boards"
    },
    {
        "name": "Andhra Pradesh - Tirupati Venkateswara Temple Hills",
        "lat": 13.6288, "lon": 79.4192,
        "country": "India", "region": "Andhra Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a ghat road climbing Tirumala hills Andhra Pradesh, seven sacred hills, dry deciduous forest, granite boulders, Telugu signboards, massive temple gateway arches"
    },
    {
        "name": "Andhra Pradesh - Visakhapatnam Beach Road & Dolphin's Nose",
        "lat": 17.6868, "lon": 83.2185,
        "country": "India", "region": "Andhra Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "RK Beach road in Visakhapatnam Vizag, submarine museum on beach, Dolphin's Nose headland cliff across Bay of Bengal, wide dual carriageway with palm trees"
    },
    {
        "name": "Gujarat - Rann of Kutch White Salt Desert",
        "lat": 23.8340, "lon": 70.3600,
        "country": "India", "region": "Gujarat", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a remote straight highway across the Great Rann of Kutch Gujarat, endless blinding white crystallized salt desert, flat horizon, colorful Kutchi circular bhunga mud huts"
    },
    {
        "name": "Gujarat - Ahmedabad Sabarmati Riverfront",
        "lat": 23.0225, "lon": 72.5714,
        "country": "India", "region": "Gujarat", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a modern concrete riverfront promenade along Sabarmati river in Ahmedabad Gujarat, manicured gardens, wide bridges, modern architecture, Gujarati signage"
    },
    {
        "name": "Rajasthan - Jodhpur Blue City & Mehrangarh Fort",
        "lat": 26.2983, "lon": 73.0183,
        "country": "India", "region": "Rajasthan", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a view overlooking the blue painted houses of Jodhpur old city Rajasthan, colossal red sandstone Mehrangarh Fort perched on cliff above, arid Thar desert hills"
    },
    {
        "name": "Rajasthan - Jaisalmer Golden Desert Fort & Sand Dunes",
        "lat": 26.9157, "lon": 70.9083,
        "country": "India", "region": "Rajasthan", "category": "India - City/Hub", "driving_side": "Left",
        "prompt": "a road in Jaisalmer Rajasthan, golden yellow sandstone fort Sonar Qila, Sam sand dunes with camels, desert scrub, hot dry desert sun, intricate carved jharokha balconies"
    },
    {
        "name": "Uttarakhand - Rishikesh Ganga Ghats & Lakshman Jhula",
        "lat": 30.1330, "lon": 78.3300,
        "country": "India", "region": "Uttarakhand", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a riverside road and suspension pedestrian bridge Lakshman Jhula in Rishikesh Uttarakhand, turquoise holy Ganga river surging from lower Himalayas, ashrams and yoga centers"
    },
    {
        "name": "Himachal Pradesh - Manali Rohtang Pass & Solang Valley",
        "lat": 32.2432, "lon": 77.1892,
        "country": "India", "region": "Himachal Pradesh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a mountain highway through pine forests in Manali Himachal Pradesh, towering snow-clad Pir Panjal peaks, Beas river rapids, wooden Apple orchards, Tibetan prayer flags"
    },
    {
        "name": "Jammu & Kashmir - Gulmarg Meadow of Flowers & Gondola",
        "lat": 34.0484, "lon": 74.3805,
        "country": "India", "region": "Jammu and Kashmir", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "an alpine meadow road in Gulmarg Kashmir, towering pine deodar forests, Apharwat snow peak, cable car gondola towers, wooden slope lodges, crisp mountain light"
    },
    {
        "name": "Ladakh - Nubra Valley & Khardung La Pass",
        "lat": 34.5800, "lon": 77.5600,
        "country": "India", "region": "Ladakh", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "the highest motorable road near Khardung La Ladakh, rocky cold desert mountain slopes, snow and ice, colorful Buddhist prayer flags fluttering, double-humped Bactrian camels"
    },
    {
        "name": "Assam - Kaziranga Elephant Grassland & Tea Plains",
        "lat": 26.5775, "lon": 93.1711,
        "country": "India", "region": "Assam", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "National Highway 715 through Kaziranga Assam, vast tall elephant grasslands, wetlands with water lilies, Brahmaputra river plains, green tea gardens, Assamese script signs"
    },
    {
        "name": "Sikkim - Gangtok Kanchenjunga View & Monasteries",
        "lat": 27.3314, "lon": 88.6138,
        "country": "India", "region": "Sikkim", "category": "India - State/UT", "driving_side": "Left",
        "prompt": "a steep terraced mountain road in Gangtok Sikkim, breathtaking panoramic view of snow-covered Mount Kanchenjunga, Rumtek monastery golden roof, Buddhist prayer wheels"
    },

    # ==========================================================================
    # 8. KERALA — DENSE DISTRICT & VILLAGE MICRO-REGIONS
    # ==========================================================================
    {
        "name": "Sulthan Bathery, Wayanad, Kerala, India",
        "lat": 11.6625, "lon": 76.2570,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a highland town junction in Sulthan Bathery Wayanad, ancient Jain temple, coffee and pepper plantations, eucalyptus trees, misty Western Ghats foothills, Malayalam signboards"
    },
    {
        "name": "Kalpetta, Wayanad, Kerala, India",
        "lat": 11.6090, "lon": 76.0827,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a bustling hill town street in Kalpetta Wayanad, multi-tier hillside shops, tea plantation slopes, spice stalls selling cardamom and cloves, red laterite cut slopes"
    },
    {
        "name": "Vythiri, Wayanad, Kerala, India",
        "lat": 11.5500, "lon": 76.0400,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rainforest resort road in Vythiri Wayanad, dense evergreen canopy, heavy tropical monsoon rain, stream waterfalls, cardamom estates, bamboo groves, Thamarassery ghat entry"
    },
    {
        "name": "Thamarassery Churam Ghat Road, Kozhikode, Kerala, India",
        "lat": 11.5167, "lon": 76.0167,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "the 9 hairpin mountain curves of Thamarassery Churam ghat road connecting Kozhikode and Wayanad, sheer mountain drop into tropical valley, monkeys along stone walls, heavy truck traffic"
    },
    {
        "name": "Beypore Port & Beach, Kozhikode, Kerala, India",
        "lat": 11.1764, "lon": 75.8117,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal road in Beypore Kozhikode, Chaliyar river estuary, historic wooden Uru boat building shipyards, stone sea walk bridge into Arabian sea, coconut groves"
    },
    {
        "name": "Manjeri, Malappuram, Kerala, India",
        "lat": 11.1206, "lon": 76.1212,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a commercial town street in Manjeri Malappuram, gold jewelry showrooms, rubber plantations on outskirts, mosques and minarets, Malayalam and Arabic calligraphic boards"
    },
    {
        "name": "Nilambur Teak Forest, Malappuram, Kerala, India",
        "lat": 11.2764, "lon": 76.2263,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a scenic paved road passing through the historic Conolly Teak Plantation in Nilambur, towering teak trees, Chaliyar river, bamboo clumps, red soil"
    },
    {
        "name": "Kottakkal Arya Vaidya Sala, Malappuram, Kerala, India",
        "lat": 11.0022, "lon": 75.9986,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage Ayurveda town street in Kottakkal Malappuram, traditional tiled hospital buildings, herbal medicinal plant gardens, tranquil scholarly ambiance"
    },
    {
        "name": "Tirur, Malappuram, Kerala, India",
        "lat": 10.9147, "lon": 75.9224,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal railway town street in Tirur Malappuram, Thunchan Memorial birthplace of Malayalam language father, canal bridges, betel leaf plantations, KSRTC buses"
    },
    {
        "name": "Payyambalam Beach, Kannur, Kerala, India",
        "lat": 11.8745, "lon": 75.3522,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a seaside avenue in Payyambalam Kannur, red laterite cliff overlooking golden sandy beach, Casuarina pine trees, seaside park, handloom textile heritage town"
    },
    {
        "name": "Parassinikkadavu Muthappan Temple, Kannur, Kerala, India",
        "lat": 11.9840, "lon": 75.3990,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a temple road in Parassinikkadavu Kannur, Valapattanam river bank, Theyyam dance performance temple, snake park, lush tropical greenery, laterite walls"
    },
    {
        "name": "Thekkady Periyar Wildlife Sanctuary, Idukki, Kerala, India",
        "lat": 9.6031, "lon": 77.1615,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a jungle road in Thekkady Idukki, Periyar tiger reserve artificial lake with submerged tree trunks, spice plantations of cardamom and pepper, elephant crossing signs"
    },
    {
        "name": "Marayoor Sandalwood Forest, Idukki, Kerala, India",
        "lat": 10.2800, "lon": 77.1600,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a rain-shadow dry hill road in Marayoor Idukki, natural sandalwood tree reserve, prehistoric dolmens rock tombs, sugarcane fields producing dark jaggery, cool dry breeze"
    },
    {
        "name": "Guruvayur Temple Town, Thrissur, Kerala, India",
        "lat": 10.5946, "lon": 76.0388,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a bustling pilgrimage town street in Guruvayur Thrissur, gold and brass lamp shops, elephant sanctuary Punnathur Kotta nearby, devotees in traditional white mundu"
    },
    {
        "name": "Chalakudy River & Anamudi Foot, Thrissur, Kerala, India",
        "lat": 10.3070, "lon": 76.3330,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a river valley road in Chalakudy Thrissur, leading to Athirappilly and Sholayar rainforest, rubber plantations, rocky riverbeds, tropical monsoon canopy"
    },
    {
        "name": "Malampuzha Dam & Gardens, Palakkad, Kerala, India",
        "lat": 10.8290, "lon": 76.6850,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a road bordering the massive Malampuzha reservoir dam in Palakkad, Western Ghats mountain backdrop, Yakshi sculpture gardens, ropeway cable cars, sunny breezy Palakkad gap"
    },
    {
        "name": "Nenmara & Nelliyampathy Orange Hills, Palakkad, Kerala, India",
        "lat": 10.5333, "lon": 76.6833,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a winding hairpin ghat road climbing from Nenmara to Nelliyampathy Palakkad, orange and tea plantations, Seetharkundu viewpoint drop, teak forests, cool mountain mist"
    },
    {
        "name": "Silent Valley National Park, Palakkad, Kerala, India",
        "lat": 11.1300, "lon": 76.4500,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a remote forest trail road in Silent Valley Palakkad, pristine virgin tropical evergreen rainforest, Kunthi river, lion-tailed macaque habitat, dense mossy jungle trees"
    },
    {
        "name": "Pala & Meenachil River, Kottayam, Kerala, India",
        "lat": 9.7126, "lon": 76.6841,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a thriving plantation town street in Pala Kottayam, Meenachil river bridge, sprawling Syrian Christian churches, rubber sheet drying sheds, NRI mansions, lush green hills"
    },
    {
        "name": "Vaikom Mahadeva Temple & Backwaters, Kottayam, Kerala, India",
        "lat": 9.7500, "lon": 76.3900,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage temple town street in Vaikom Kottayam on Vembanad lake shore, ancient round sanctum temple, historic satyagraha memorial, coconut palm canals"
    },
    {
        "name": "Kozhencherry & Pamba River Banks, Pathanamthitta, Kerala, India",
        "lat": 9.3400, "lon": 76.7100,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a river town road in Kozhencherry Pathanamthitta, banks of holy Pamba river, Maramon Convention sandy riverbed site, rubber plantations, Malayalam shop signboards"
    },
    {
        "name": "Konni Elephant Reserve & Forests, Pathanamthitta, Kerala, India",
        "lat": 9.2435, "lon": 76.8480,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a forest town road in Konni Pathanamthitta, historic wooden elephant training kraal, Achankovil river, teak and bamboo reserves, winding forest roads"
    },
    {
        "name": "Sabarimala Foothills & Pamba, Pathanamthitta, Kerala, India",
        "lat": 9.4000, "lon": 77.0600,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a pilgrimage forest road through Periyar reserve leading to Pamba base camp Sabarimala, dense rainforest, wild streams, Lord Ayyappa pilgrim buses, spiritual chanting"
    },
    {
        "name": "Ashtamudi Lake & Neendakara Fishing Port, Kollam, Kerala, India",
        "lat": 8.9400, "lon": 76.5400,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a coastal harbor road in Neendakara Kollam, eight-armed Ashtamudi estuary opening into sea, colorful mechanized fishing trawlers, Chinese fishing nets, cashew processing towns"
    },
    {
        "name": "Padmanabhaswamy Temple Fort Area, Thiruvananthapuram, Kerala, India",
        "lat": 8.4828, "lon": 76.9436,
        "country": "India", "region": "Kerala", "category": "Kerala - Micro-Region", "driving_side": "Left",
        "prompt": "a heritage street surrounding East Fort Thiruvananthapuram, golden gopuram of Sree Padmanabhaswamy temple, Padmatheertham pond, granite stone pillared corridors"
    }
]

def merge_and_save():
    print(f"Existing locations count: {len(EXISTING_LOCATIONS)}")
    print(f"New candidate locations count: {len(NEW_LOCATIONS)}")

    seen_names = set()
    combined = []

    # 1. Add all existing locations
    for loc in EXISTING_LOCATIONS:
        norm_name = loc["name"].strip().lower()
        if norm_name not in seen_names:
            seen_names.add(norm_name)
            combined.append(loc)

    # 2. Add new unique locations
    added_count = 0
    for loc in NEW_LOCATIONS:
        norm_name = loc["name"].strip().lower()
        if norm_name not in seen_names:
            seen_names.add(norm_name)
            combined.append(loc)
            added_count += 1

    print(f"Added {added_count} brand-new locations!")
    print(f"Total unified locations: {len(combined)}")

    # 3. Format and write back to locations.py
    output_code = ['# ==============================================================================',
                   '# Comprehensive Global, Pan-India, and Hyper-Local Micro-Regional Locations',
                   '# for StreetCLIP GeoGuessr AI (Unified Database)',
                   '# ==============================================================================\n',
                   'LOCATIONS = [']

    for loc in combined:
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

    print("Successfully wrote updated 'locations.py'!")

if __name__ == "__main__":
    merge_and_save()
