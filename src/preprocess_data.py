import pandas as pd
from sklearn.preprocessing import MinMaxScaler

pd.options.mode.chained_assignment = None  # default='warn'

def preprocess(team_df, player_df):
    # Checks for any missing player position
    positions = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
    missing = (~player_df['position'].isin(positions)).any()
    
    if missing:
        missing_index = player_df.index[~player_df['position'].isin(positions)].tolist()
        for index in missing_index:
            prev_position = player_df.loc[index - 1]['position']
            positions_index = positions.index(prev_position)
            player_df.loc[missing_index, 'position'] = positions[(positions_index + 1) % len(positions)]
            player_df = player_df.reset_index(drop=True)
    
    # Scales the features
    per_min_features = ['kills', 'deaths', 'assists', 'gold_earned', 'neutral_minions', 'vision_score', 'lane_minions']
    norm_features = ['gold_earned', 'neutral_minions', 'vision_score', 'lane_minions']

    scaler = MinMaxScaler()

    for feature in per_min_features:
        player_df[feature] = player_df[feature] / (player_df['duration'] / 60) # Duration is in seconds

    for feature in norm_features:    
        values = player_df[feature].values.reshape(-1, 1)
        scaler.fit(values)
        normed_feature = scaler.transform(values)    
        player_df[feature] = normed_feature
    
    # Replaces win boolean values with 1 and 0
    bool_mapping = {
        True: 1, 
        False: 0
    }

    team_df = team_df.replace(bool_mapping)
    
    match_data = pd.merge(team_df, player_df, on=['match_id', 'win'])
    
    # Replaces team values of 100 and 200 with blue and red team
    match_data.replace(to_replace={'100' : 'blue', '200' : 'red'}, inplace=True)
    
    # Exclude features that has collinearity problems
    drop_columns = ['total_baron', 'total_dragon', 'total_inhibitor', 'total_herald', 'total_tower']
    match_data.drop(columns=drop_columns, inplace=True)
    
    # Create new columns for the stats by team and position to uniquely identify each row
    position_match = match_data.copy()
    position_match['position_stats'] = position_match['teamId'] + '_' + position_match['position']
    position_data = position_match.pivot_table(
        index='match_id',
        columns='position_stats',
        values=['kills', 'deaths', 'assists', 'gold_earned', 'neutral_minions', 'vision_score', 'lane_minions'],
        aggfunc='first'
    )

    position_data.columns = [f'{pos.lower()}_{col}' for col, pos in position_data.columns]
    position_data.reset_index(inplace=True) 
    
    team_match = match_data.copy()
    team_match['team_stats'] = team_match['teamId']
    team_data = team_match.pivot_table(
        index='match_id',
        columns='team_stats',
        values=['first_baron', 'first_blood', 'first_dragon', 'first_inhibitor', 'first_herald', 'first_tower'],
        aggfunc='first'
    )

    team_data.columns = [f'{pos.lower()}_{col}' for col, pos in team_data.columns]
    team_data.reset_index(inplace=True) 

    won_match = match_data.copy()
    won_match['team_won'] = won_match['teamId']
    winning_team = won_match.pivot_table(
        index='match_id',
        columns='team_won',
        values=['win'],
        aggfunc='first'
    )

    winning_team.columns = [f'{pos.lower()}_{col}' for col, pos in winning_team.columns]
    winning_team.reset_index(inplace=True)

    merged_data = pd.merge(position_data, team_data, on='match_id').merge(winning_team, on='match_id')
    one_team = merged_data.copy()
    final_data = one_team.filter(like='blue', axis=1) # Either blue team or red team features

    return final_data