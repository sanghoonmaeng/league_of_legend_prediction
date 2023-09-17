import pickle
import user_config
import request_data
import extract_features
import preprocess_data
import predict_outcome
from flask import Flask, jsonify, request

model_file = user_config.MODEL_FILE_PATH

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

app = Flask('win predictor')

@app.route('/predict', methods=['POST'])
def predict():
    # Call request_data.py to make Riot API calls for match data
    summoner = request.get_json()
    name = [summoner['summoner_name']]
    puuid_list = request_data.get_player_ids(name)
    match_ids = request_data.get_match_ids(puuid_list)
    matches = request_data.get_match_data(match_ids)
    
    # Call extract_features.py to get necessary features
    team_df, player_df = extract_features.get_features(matches)
    
    # Call preprocess_data.py to clean and transform the features
    match_data = preprocess_data.preprocess(team_df, player_df)
    outcome = predict_outcome.predict_match(model, match_data)
    return jsonify(outcome)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)