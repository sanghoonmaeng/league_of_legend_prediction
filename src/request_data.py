# Imports necesary libraries
import requests
import time
import user_config

def get_summoners():
    summoners_url = f'https://{user_config.SERVER}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{user_config.QUEUE}?api_key={user_config.API_KEY}'
    response = requests.get(summoners_url)
    summoners = response.json()
    
    summoner_names = []
    for i in range(user_config.PLAYERS): # Chooses the players from the Master's league
        name = summoners['entries'][i]['summonerName'] # Process the result and extract summoner name
        summoner_names.append(name)
    return summoner_names

def get_player_ids(summoner_names):
    puuid_list = []
    counter = user_config.PLAYERS
    while counter > 0:
        for _ in range(5): # Request in a batch of five to meet the rate limit of 100 requests every 2 minutes
            limit = min(20, len(summoner_names))      
            #time.sleep(1.5)
            for i in range(limit): # 20 requests per second
                summoner = summoner_names[i]
                puuid_url = f'https://{user_config.SERVER}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={user_config.API_KEY}'
                response = requests.get(puuid_url)
                if response.status_code == 429:
                    print("Exceeded API rate limit")
                    #time.sleep(120)
                    continue
                player = response.json()
                try: # Unsure why but some players do not have puuid
                    puuid_list.append(player["puuid"]) # Process the result and extract player IDs
                except:
                    continue
            counter -= limit
            summoner_names = summoner_names[limit:]
        #time.sleep(120) # 100 requests every 2 minutes
    return puuid_list

def get_match_ids(puuid_list):
    match_ids = []
    counter = len(puuid_list)
    
    while counter > 0:
        for _ in range(5): # Makes five of 20 requests per second
            limit = min(20, len(puuid_list))
            #time.sleep(1.5)
            for i in range(limit): # 20 requests per second
                puuid = puuid_list[i]
                match_id_url = f'https://{user_config.REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={user_config.QUEUE_ID}&start=0&count={user_config.NUM_GAMES}&api_key={user_config.API_KEY}'
                response = requests.get(match_id_url)
                if response.status_code == 429:
                    print("Exceeded API rate limit")
                    #time.sleep(120)
                    continue
                match_id = response.json()
                match_ids.extend(match_id) # Process the result and extract match IDs
            counter -= limit
            puuid_list = puuid_list[limit:]
        #time.sleep(120) # 100 requests every 2 minutes
    return match_ids

def get_match_data(match_ids):
    match_list = []
    unique_ids = list(set(match_ids)) # Remove any duplicate matches by chance
    counter = len(unique_ids)
    
    while counter > 0:
        for _ in range(5): # Makes five of 20 requests per second
            limit = min(20, len(unique_ids))
            #time.sleep(1.5)
            for i in range(limit): # 20 requests per second
                match_id = unique_ids[i]
                match_url = f'https://{user_config.REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={user_config.API_KEY}'
                response = requests.get(match_url)
                if response.status_code == 429:
                    print("Exceeded API rate limit")
                    #time.sleep(120)
                    continue
                match = response.json()
                match_list.append(match) # Process the result and extract match
            counter -= limit
            unique_ids = unique_ids[limit:]
        #time.sleep(120) # 100 requests every 2 minutes
    return match_list