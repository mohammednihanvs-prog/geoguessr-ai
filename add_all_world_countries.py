# ==============================================================================
# Script to add complete world coverage to locations.py
# ==============================================================================

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from locations import LOCATIONS

ADDITIONAL_GLOBAL_COUNTRIES = [
    {
        "name": "Albania - Tirana Skanderbeg Square & Dajti Mountain",
        "lat": 41.3275, "lon": 19.8187,
        "country": "Albania", "region": "Tirana", "category": "Global", "driving_side": "Right",
        "prompt": "a street in Tirana Albania, Skanderbeg statue, colorful painted facades, Mount Dajti backdrop, concrete dome bunker pillboxes, red-and-black Albanian chevrons"
    },
    {
        "name": "Andorra - Andorra la Vella & Pyrenees Valleys",
        "lat": 42.5063, "lon": 1.5218,
        "country": "Andorra", "region": "Andorra la Vella", "category": "Global", "driving_side": "Right",
        "prompt": "a steep mountain valley highway in Andorra, Pyrenees rocky peaks, grey granite stone buildings, duty-free shopping avenues, Catalan road signs"
    },
    {
        "name": "Armenia - Yerevan Cascade & Mount Ararat View",
        "lat": 40.1792, "lon": 44.4991,
        "country": "Armenia", "region": "Yerevan", "category": "Global", "driving_side": "Right",
        "prompt": "a street view in Yerevan Armenia, pink volcanic tuff stone buildings, Mount Ararat snow peak visible in distance, Cascade stone monument, unique Armenian script"
    },
    {
        "name": "Azerbaijan - Baku Boulevard & Flame Towers",
        "lat": 40.4093, "lon": 49.8671,
        "country": "Azerbaijan", "region": "Baku", "category": "Global", "driving_side": "Right",
        "prompt": "a wide seaside boulevard in Baku Azerbaijan along Caspian Sea, iconic trio of Flame Towers skyscrapers, limestone medieval Old City walls, oil rigs on horizon"
    },
    {
        "name": "Bangladesh - Dhaka Rickshaws & Buriganga River",
        "lat": 23.8103, "lon": 90.4125,
        "country": "Bangladesh", "region": "Dhaka", "category": "Global", "driving_side": "Left",
        "prompt": "a vibrant crowded street in Dhaka Bangladesh, thousands of painted cycle rickshaws, green delta rivers, Bengali script signboards, tropical humid climate, left-hand drive"
    },
    {
        "name": "Belarus - Minsk Independence Avenue & Stalinist Empire",
        "lat": 53.9006, "lon": 27.5590,
        "country": "Belarus", "region": "Minsk", "category": "Global", "driving_side": "Right",
        "prompt": "an immaculately clean broad boulevard in Minsk Belarus, grand Stalinist Empire architecture, Victory Square obelisk, birch trees, Cyrillic road signage"
    },
    {
        "name": "Bhutan - Thimphu Valley & Tiger's Nest Foothills",
        "lat": 27.4728, "lon": 89.6393,
        "country": "Bhutan", "region": "Thimphu", "category": "Global", "driving_side": "Left",
        "prompt": "a mountain road in Thimphu Bhutan, traditional Himalayan wooden architecture with painted floral motifs and phalluses, Buddhist prayer flags, pine covered valleys, left-hand drive"
    },
    {
        "name": "Bolivia - La Paz Cable Car & Illimani Mountain",
        "lat": -16.5000, "lon": -68.1500,
        "country": "Bolivia", "region": "La Paz", "category": "Global", "driving_side": "Right",
        "prompt": "a dramatic high-altitude street overlooking La Paz Bolivia canyon, red Mi Teleférico cable cars gliding overhead, red brick houses clinging to steep cliffs, snow-capped Mount Illimani"
    },
    {
        "name": "Bosnia and Herzegovina - Sarajevo Latin Bridge & Bascarsija",
        "lat": 43.8563, "lon": 18.4131,
        "country": "Bosnia and Herzegovina", "region": "Sarajevo", "category": "Global", "driving_side": "Right",
        "prompt": "a riverside street in Sarajevo Bosnia along Miljacka river, Latin Bridge, Ottoman bazaar Bascarsija wooden shops, minarets and Catholic cathedrals side by side, green Dinaric hills"
    },
    {
        "name": "Botswana - Gaborone & Kalahari Acacia Savanna",
        "lat": -24.6581, "lon": 25.9122,
        "country": "Botswana", "region": "South-East", "category": "Global", "driving_side": "Left",
        "prompt": "a flat asphalt highway in Botswana, Kalahari sandy roadside soil, flat-topped umbrella acacia trees, cattle grazing along fences, left-hand drive, blue European style license plates"
    },
    {
        "name": "Cyprus - Nicosia Historic Venetian Walls & Troodos",
        "lat": 35.1856, "lon": 33.3823,
        "country": "Cyprus", "region": "Nicosia", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Cyprus, olive and carob trees, dry limestone soil, yellow rear license plates, left-hand drive, Greek and English signage, Mediterranean sunshine"
    },
    {
        "name": "Dominican Republic - Santo Domingo Colonial Zone & Malecon",
        "lat": 18.4861, "lon": -69.9312,
        "country": "Dominican Republic", "region": "Distrito Nacional", "category": "Global", "driving_side": "Right",
        "prompt": "a seaside avenue in Santo Domingo Dominican Republic along the Malecon, Caribbean ocean waves, royal palm trees, coral stone colonial churches, colorful motoconcho bikes"
    },
    {
        "name": "Ecuador - Quito Historic Center & Pichincha Volcano",
        "lat": -0.1807, "lon": -78.4678,
        "country": "Ecuador", "region": "Pichincha", "category": "Global", "driving_side": "Right",
        "prompt": "a steep cobblestone street in old town Quito Ecuador, ornate gold-leaf Jesuit church Compania de Jesus, Pichincha active volcano backdrop, yellow taxi license plates"
    },
    {
        "name": "Estonia - Tallinn Medieval Old Town & Baltic Pine",
        "lat": 59.4370, "lon": 24.7535,
        "country": "Estonia", "region": "Harju", "category": "Global", "driving_side": "Right",
        "prompt": "a cobbled street in Tallinn Estonia, medieval stone fortress towers Viru gate, Baltic pine trees, modern digital tech hubs, clean Scandinavian EU road signs"
    },
    {
        "name": "Eswatini - Ezulwini Valley of Heaven, Mbabane",
        "lat": -26.3055, "lon": 31.1367,
        "country": "Eswatini", "region": "Hhohho", "category": "Global", "driving_side": "Left",
        "prompt": "a scenic highway winding through the Ezulwini Valley Eswatini, lush green granite mountains Execution Rock, pine plantations, roadside craft markets, left-hand drive"
    },
    {
        "name": "Ethiopia - Addis Ababa Meskel Square & Entoto Hills",
        "lat": 9.0108, "lon": 38.7613,
        "country": "Ethiopia", "region": "Addis Ababa", "category": "Global", "driving_side": "Right",
        "prompt": "a wide street in Addis Ababa Ethiopia, blue and white Lada minibus taxis, eucalyptus trees on Entoto mountain backdrop, unique ancient Amharic Ge'ez script signage"
    },
    {
        "name": "Georgia - Tbilisi Old Town Balconies & Narikala",
        "lat": 41.7151, "lon": 44.8271,
        "country": "Georgia", "region": "Tbilisi", "category": "Global", "driving_side": "Right",
        "prompt": "a picturesque street in Tbilisi Georgia, ornate carved wooden overhanging balconies, Narikala cliff fortress above Kura river, sulfur bath domes, unique curved Georgian script"
    },
    {
        "name": "Guatemala - Antigua Cobblestones & Volcan de Agua",
        "lat": 14.5586, "lon": -90.7339,
        "country": "Guatemala", "region": "Sacatepequez", "category": "Global", "driving_side": "Right",
        "prompt": "a historic cobblestone street under the Santa Catalina yellow arch in Antigua Guatemala, perfect cone of Volcan de Agua volcano towering at end of street, colorful baroque facades"
    },
    {
        "name": "Jordan - Petra Rose City Canyon & Desert Highway",
        "lat": 30.3285, "lon": 35.4444,
        "country": "Jordan", "region": "Ma'an", "category": "Global", "driving_side": "Right",
        "prompt": "a narrow desert canyon road approaching Petra Treasury carved into pink rose sandstone cliffs, bedouin camels, dry arid desert rock, Arabic and English road markers"
    },
    {
        "name": "Kazakhstan - Almaty Medeu Gorge & Tien Shan Peaks",
        "lat": 43.2220, "lon": 76.8512,
        "country": "Kazakhstan", "region": "Almaty", "category": "Global", "driving_side": "Right",
        "prompt": "a mountain highway climbing Medeu canyon in Almaty Kazakhstan, towering snow-covered Tien Shan peaks, Tien Shan spruce fir trees, wide asphalt, Cyrillic and Kazakh signage"
    },
    {
        "name": "Kyrgyzstan - Ala Archa Gorge & Bishkek Foothills",
        "lat": 42.8746, "lon": 74.5698,
        "country": "Kyrgyzstan", "region": "Chuy", "category": "Global", "driving_side": "Right",
        "prompt": "a mountain highway through Ala Archa canyon Kyrgyzstan, jagged glacier snow peaks, rushing mountain torrents, juniper bushes, felt yurt tents on roadsides, Cyrillic signage"
    },
    {
        "name": "Laos - Luang Prabang Mekong Riverfront & Temples",
        "lat": 19.8893, "lon": 102.1357,
        "country": "Laos", "region": "Luang Prabang", "category": "Global", "driving_side": "Right",
        "prompt": "a quiet riverside street in Luang Prabang Laos along the Mekong, French colonial villas with dark teak shutters, saffron-robed Buddhist monks, frangipani blossoms, Lao script"
    },
    {
        "name": "Latvia - Riga Art Nouveau District & Daugava River",
        "lat": 56.9496, "lon": 24.1052,
        "country": "Latvia", "region": "Riga", "category": "Global", "driving_side": "Right",
        "prompt": "Alberta iela street in Riga Latvia, world-famous Art Nouveau facades with gargoyles and statues, cobblestone streets, red brick churches, Baltic pine forests on outskirts"
    },
    {
        "name": "Lebanon - Beirut Corniche & Pigeon Rocks",
        "lat": 33.8938, "lon": 35.5018,
        "country": "Lebanon", "region": "Beirut", "category": "Global", "driving_side": "Right",
        "prompt": "the seaside Corniche promenade in Beirut Lebanon, Raouche Pigeon Rocks natural limestone arches in Mediterranean sea, palm trees, Mount Lebanon backdrop, Arabic and French signs"
    },
    {
        "name": "Lesotho - Sani Pass & Drakensberg Escarpment",
        "lat": -29.5847, "lon": 29.2858,
        "country": "Lesotho", "region": "Mokhotlong", "category": "Global", "driving_side": "Left",
        "prompt": "a dramatic high-altitude pass road on Sani Pass Lesotho, rugged barren mountain escarpment above 2800 meters, stone rondavel huts, Basotho blanket horsemen, left-hand drive"
    },
    {
        "name": "Lithuania - Vilnius Baroque Old Town & Gediminas Tower",
        "lat": 54.6872, "lon": 25.2797,
        "country": "Lithuania", "region": "Vilnius", "category": "Global", "driving_side": "Right",
        "prompt": "a picturesque street in Vilnius Lithuania, red brick Gediminas Castle hill, Gothic St Anne Church, cobblestone alleys, EU blue plate strip, Lithuanian signage"
    },
    {
        "name": "Luxembourg - Luxembourg City Grund & Alzette Viaduct",
        "lat": 49.6116, "lon": 6.1319,
        "country": "Luxembourg", "region": "Luxembourg", "category": "Global", "driving_side": "Right",
        "prompt": "a view overlooking the deep Alzette river valley Grund in Luxembourg City, stone arch viaducts, medieval fortifications, slate roofed fairytale stone houses, pristine streets"
    },
    {
        "name": "Madagascar - Avenue of the Baobabs, Morondava",
        "lat": -20.2508, "lon": 44.4184,
        "country": "Madagascar", "region": "Menabe", "category": "Global", "driving_side": "Right",
        "prompt": "an unpaved red dirt road lined by colossal ancient Grandidier's Baobab trees in Madagascar, flat savanna landscape, zebu cattle carts, sunny tropical African light"
    },
    {
        "name": "Malta - Valletta Grand Harbour & Limestone Streets",
        "lat": 35.8989, "lon": 14.5146,
        "country": "Malta", "region": "South Eastern", "category": "Global", "driving_side": "Left",
        "prompt": "a steep narrow street in Valletta Malta, iconic colorful enclosed wooden balconies gallarija, warm honey-colored globigerina limestone walls, Grand Harbour view, left-hand drive"
    },
    {
        "name": "Mongolia - Ulaanbaatar & Endless Grassland Steppe",
        "lat": 47.9212, "lon": 106.9186,
        "country": "Mongolia", "region": "Ulaanbaatar", "category": "Global", "driving_side": "Right",
        "prompt": "a remote two-track dirt trail or asphalt highway through vast rolling green Mongolian steppe, white round felt ger yurt tents, grazing horses, clear big sky, Google car with roof rack"
    },
    {
        "name": "Montenegro - Bay of Kotor Fjord & Limestone Peaks",
        "lat": 42.4247, "lon": 18.7712,
        "country": "Montenegro", "region": "Kotor", "category": "Global", "driving_side": "Right",
        "prompt": "a narrow coastal road bordering the glassy waters of Bay of Kotor Montenegro, sheer towering limestone cliffs rising directly from water, medieval stone walled towns, red tile roofs"
    },
    {
        "name": "Namibia - Sossusvlei Giant Red Dunes & Dead Vlei",
        "lat": -24.7267, "lon": 15.3400,
        "country": "Namibia", "region": "Hardap", "category": "Global", "driving_side": "Left",
        "prompt": "a paved or salt-and-sand road through Namib-Naukluft National Park Namibia, towering 300-meter high red iron oxide sand dunes Dune 45, white salt pan, left-hand drive, deep blue sky"
    },
    {
        "name": "Nepal - Kathmandu Durbar Square & Himalayan Valley",
        "lat": 27.7172, "lon": 85.3240,
        "country": "Nepal", "region": "Bagmati", "category": "Global", "driving_side": "Left",
        "prompt": "a street in Kathmandu Nepal, multi-tiered carved wooden pagoda temples, sacred pigeons, Hindu and Buddhist shrines, motorbikes, Devanagari script signboards, left-hand drive"
    },
    {
        "name": "Nigeria - Lagos Victoria Island & Lekki Tollway",
        "lat": 6.4281, "lon": 3.4219,
        "country": "Nigeria", "region": "Lagos", "category": "Global", "driving_side": "Right",
        "prompt": "a wide multi-lane expressway Lekki-Epe tollway in Lagos Nigeria, modern commercial glass towers, yellow Danfo minibuses, palm trees, lagoon bridges, bright Nigerian sun"
    },
    {
        "name": "North Macedonia - Ohrid Lake & Medieval Churches",
        "lat": 41.1172, "lon": 20.8019,
        "country": "North Macedonia", "region": "Southwestern", "category": "Global", "driving_side": "Right",
        "prompt": "a cobbled lakeside street in Ohrid North Macedonia, crystal clear ancient Lake Ohrid, Church of St John at Kaneo on cliff, red terracotta roofs, Cyrillic and Latin signs"
    },
    {
        "name": "Oman - Muscat Muttrah Corniche & Desert Mountains",
        "lat": 23.6190, "lon": 58.5680,
        "country": "Oman", "region": "Muscat", "category": "Global", "driving_side": "Right",
        "prompt": "Muttrah Corniche waterfront in Muscat Oman, pure white and cream Islamic architecture, dramatic craggy dark brown desert mountains, traditional wooden Dhow boats, clean highways"
    },
    {
        "name": "Panama - Panama City Cinta Costera & Skyline",
        "lat": 8.9824, "lon": -79.5199,
        "country": "Panama", "region": "Panama", "category": "Global", "driving_side": "Right",
        "prompt": "a modern coastal highway Cinta Costera curving around Panama Bay, gleaming skyscraper skyline, Pacific ocean views, tropical palm trees, Casco Viejo colonial district"
    },
    {
        "name": "Philippines - Manila Intramuros & Jeepneys",
        "lat": 14.5896, "lon": 120.9747,
        "country": "Philippines", "region": "Metro Manila", "category": "Global", "driving_side": "Right",
        "prompt": "a bustling street in Manila Philippines, iconic flashy chrome-and-color Jeepneys, Spanish stone fortress walls Intramuros, tropical rain trees, English and Tagalog signage"
    },
    {
        "name": "Qatar - Doha Corniche & West Bay Skyline",
        "lat": 25.2854, "lon": 51.5310,
        "country": "Qatar", "region": "Doha", "category": "Global", "driving_side": "Right",
        "prompt": "the curving waterfront promenade of Doha Corniche Qatar, futuristic illuminated West Bay skyscrapers, traditional wooden dhow boats in bay, date palm trees, smooth highway"
    },
    {
        "name": "Rwanda - Kigali Clean Avenues & Green Hills",
        "lat": -1.9441, "lon": 30.0619,
        "country": "Rwanda", "region": "Kigali", "category": "Global", "driving_side": "Right",
        "prompt": "an immaculately clean tree-lined boulevard in Kigali Rwanda, landscaped flower medians, moto-taxi riders in uniform red helmets, rolling lush green terraced hillsides, modern glass convention center"
    },
    {
        "name": "Saudi Arabia - Riyadh Kingdom Centre & Desert Highway",
        "lat": 24.7136, "lon": 46.6753,
        "country": "Saudi Arabia", "region": "Riyadh", "category": "Global", "driving_side": "Right",
        "prompt": "King Fahd road in Riyadh Saudi Arabia, iconic Kingdom Centre tower with sky bridge opening, wide multi-lane freeway with palm trees, desert sandstone architecture, Arabic signs"
    },
    {
        "name": "Serbia - Belgrade Kalemegdan & Danube Confluence",
        "lat": 44.8125, "lon": 20.4612,
        "country": "Serbia", "region": "Belgrade", "category": "Global", "driving_side": "Right",
        "prompt": "a street bordering Kalemegdan fortress in Belgrade Serbia, confluence of Sava and Danube rivers, Victor monument, red and white tram cars, Cyrillic and Latin road signs"
    },
    {
        "name": "Slovakia - High Tatras Alpine Mountain Highway",
        "lat": 49.1667, "lon": 20.1333,
        "country": "Slovakia", "region": "Presov", "category": "Global", "driving_side": "Right",
        "prompt": "a highway running along the foot of the jagged granite High Tatras mountains Slovakia, dense pine forests, alpine ski resorts Strbske Pleso, European road bollards"
    },
    {
        "name": "Slovenia - Lake Bled Castle & Julian Alps",
        "lat": 46.3683, "lon": 14.1146,
        "country": "Slovenia", "region": "Upper Carniola", "category": "Global", "driving_side": "Right",
        "prompt": "a scenic road circling Lake Bled Slovenia, fairytale island church in middle of emerald lake, medieval castle perched on sheer cliff, snow-dusted Julian Alps, clean asphalt"
    },
    {
        "name": "Sri Lanka - Kandy Hill Country & Tea Terraces",
        "lat": 7.2906, "lon": 80.6337,
        "country": "Sri Lanka", "region": "Central", "category": "Global", "driving_side": "Left",
        "prompt": "a winding hill road through Kandy Sri Lanka, Temple of the Sacred Tooth Relic by lake, rolling Ceylon tea plantations, blue mountain trains, Sinhala and Tamil script, left-hand drive"
    },
    {
        "name": "Tunisia - Sidi Bou Said Blue & White Mediterranean Coast",
        "lat": 36.8703, "lon": 10.3418,
        "country": "Tunisia", "region": "Tunis", "category": "Global", "driving_side": "Right",
        "prompt": "a cobbled pedestrian street in Sidi Bou Said Tunisia, whitewashed walls with brilliant cobalt blue doors and window grilles (moucharabieh), bougainvillea, Mediterranean sea panorama"
    },
    {
        "name": "Uganda - Kampala Red Dirt Hills & Lake Victoria",
        "lat": 0.3476, "lon": 32.5825,
        "country": "Uganda", "region": "Central", "category": "Global", "driving_side": "Left",
        "prompt": "a road winding through the seven hills of Kampala Uganda, deep red laterite clay soil, lush green banana and matoke trees, boda-boda motorcycle taxis, left-hand drive"
    },
    {
        "name": "Uzbekistan - Samarkand Registan Silk Road Square",
        "lat": 39.6547, "lon": 66.9758,
        "country": "Uzbekistan", "region": "Samarkand", "category": "Global", "driving_side": "Right",
        "prompt": "a grand avenue facing Registan Square in Samarkand Uzbekistan, monumental Silk Road madrasahs with dazzling turquoise ceramic tile mosaics, ribbed turquoise domes, arid desert sun"
    }
]

def add_global_countries():
    print(f"Current locations: {len(LOCATIONS)}")
    seen = {l["name"].strip().lower() for l in LOCATIONS}
    added = 0
    new_list = list(LOCATIONS)
    for item in ADDITIONAL_GLOBAL_COUNTRIES:
        n = item["name"].strip().lower()
        if n not in seen:
            seen.add(n)
            new_list.append(item)
            added += 1

    print(f"Added {added} global countries and regions!")
    print(f"Total locations now: {len(new_list)}")

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

    print("Saved updated locations.py!")

if __name__ == "__main__":
    add_global_countries()
