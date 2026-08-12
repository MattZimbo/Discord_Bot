'''
This file relates to all information required to make our backlog
functionality function.
'''
# Necessary libs
import requests
# Mongo DB libs
from motor.motor_asyncio import AsyncIOMotorDatabase

'''
Calls steams endpoint API to find a game 
and pull its details
'''
async def get_game_info(db: AsyncIOMotorDatabase, guild_id: str, game: str, reasoning: str):

    # Get the app ID so users don't have to
    url = f"https://store.steampowered.com/api/storesearch/?term={game}&l=english&cc=US"
    response = requests.get(url).json()

    # Checking we got it
    if not (response.get('items')):
        return "failed"

    top_result = response['items'][0]
    game_id = top_result['id']
    game_title = top_result['name']

    collection = db["backlog"]
    existing = await collection.find_one({"guild_id": str(guild_id), "title": game_title})

    if existing:
        print(existing)
        print("yep")
        return "failed"

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
            "is_free"       : True,
            "reasoning"     : reasoning
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
            "price_ZAR"     : price_za['final_formatted'].replace(' ', ''),
            "is_discounted" : is_discounted,
            "discount_%"    : str(discount_perc),
            "is_free"       : False,
            "reasoning"     : reasoning
        }
    else:
        return {
            "title"         : game_title,
            "game_img"      : game_img,
            "url"           : f"https://store.steampowered.com/app/{game_id}",
            "price_USD"     : price_data['final_formatted'],
            "price_EUR"     : price_de['final_formatted'],
            "price_ZAR"     : price_za['final_formatted'].replace(' ', ''),
            "is_discounted" : is_discounted,
            "is_free"       : False,
            "reasoning"     : reasoning
        }