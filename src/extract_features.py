import pandas as pd

def get_features(matches):
    player_stats = []
    team_stats = []
    
    for match in matches:
        # Extracts individual player's statistics
        for player in match['info']['participants']:
            player_stats.append({
                'match_id' : match['metadata']['matchId'],
                'duration' : match['info']['gameDuration'],
                'position' : player['teamPosition'],
                'kills' : player['kills'],
                'deaths' : player['deaths'],
                'assists' : player['assists'],
                'gold_earned' : player['goldEarned'],
                'neutral_minions' : player['neutralMinionsKilled'],
                'vision_score' : player['visionScore'],
                'lane_minions' : player['totalMinionsKilled'],
                'win' : player['win']
            })
            
        # Extracts each team's statistics    
        for team in match['info']['teams']:
            team_stats.append({
                'match_id' : match['metadata']['matchId'],
                'teamId' : str(team['teamId']),
                'first_baron' : team['objectives']['baron']['first'],
                'first_blood' : team['objectives']['champion']['first'],
                'first_dragon' : team['objectives']['dragon']['first'],
                'first_inhibitor' : team['objectives']['inhibitor']['first'],
                'first_herald' : team['objectives']['riftHerald']['first'],
                'first_tower' : team['objectives']['tower']['first'],
                'total_baron' : team['objectives']['baron']['kills'],
                'total_dragon' : team['objectives']['dragon']['kills'],
                'total_inhibitor' : team['objectives']['inhibitor']['kills'],
                'total_herald' : team['objectives']['riftHerald']['kills'],
                'total_tower' : team['objectives']['tower']['kills'],
                 'win' : team['win']
            })

    # Creates each statistics into a dataframe
    team_df = pd.DataFrame(team_stats)
    player_df = pd.DataFrame(player_stats)
   
    return team_df, player_df