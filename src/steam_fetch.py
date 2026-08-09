'''
This file relates to all information required to make our backlog
functionality function.
'''


import requests
from pathlib import Path

'''
Calls steams endpoint API to find a game 
and pull its details
'''
def get_game_info(game):

    # Get the app ID so users don't have to
    url = f"https://store.steampowered.com/api/storesearch/?term={game}&l=english&cc=US"
    response = requests.get(url).json()

    # Checking we got it
    if not (response.get('items')):
        return "failed"

    top_result = response['items'][0]
    game_id = top_result['id']
    game_title = top_result['name']

    # Ping the steam endpoint with the app ID
    details = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=US"
    details_response = requests.get(details).json()

    

    details_SA = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=ZA"
    details_response_SA = requests.get(details_SA).json()
    game_data = details_response_SA[str(game_id)]
    data = game_data['data']
    
    price_za = data['price_overview']

    details_DE = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=DE"
    details_response_DE = requests.get(details_DE).json()
    game_data = details_response_DE[str(game_id)]
    data = game_data['data']
    price_de = data['price_overview']

    # Checking we got it
    game_data = details_response[str(game_id)]
    if not game_data.get('success'):
        return "failed"

    data = game_data['data']
    game_img = data.get("header_image")

    if data.get('is_free'):
        return {
            "title"         : game_title,
            "game_img"      : game_img,
            "url"           : f"https://store.steampowered.com/app/{game_id}",
            "price"         : "Free to Play",
            "is_discounted"    : False,
            "is_free"       : True
        }

    price_data = data.get('price_overview')
    if not price_data:
        return "failed"
    

    discount_perc = price_data.get('discount_percent', 0)
    is_discounted = discount_perc > 0

    if (is_discounted):
        return {
            "title"         : game_title,
            "game_img"      : game_img,
            "url"           : f"https://store.steampowered.com/app/{game_id}",
            "price_USD"     : price_data['final_formatted'],
            "price_EUR"     : "\u20ac" + price_de['final_formatted'][:-1],
            "price_ZAR"     : price_za['final_formatted'],
            "is_discounted"    : is_discounted,
            "discount %"    : discount_perc,
            "is_free"       : False
        }
    else:
        return {
            "title"         : game_title,
            "game_img"      : game_img,
            "url"           : f"https://store.steampowered.com/app/{game_id}",
            "price_USD"     : price_data['final_formatted'],
            "price_EUR"     : price_de['final_formatted'],
            "price_ZAR"     : price_za['final_formatted'],
            "is_discounted"    : is_discounted,
            "is_free"       : False
        }

'''
Checking if the games been added to the backlog already
'''

def do_we_have_it(title):
    title = title + ".json"
    storage_path = Path("../data/back_log")

    for entry in storage_path.glob("*.json"):
        if title in entry.name:
            return True

    return False

## Example usage
results = get_game_info("Cyberpunk 2077")
print(results["title"].replace(' ', ''))
#print(do_we_have_it("Cyberpunk2077"))