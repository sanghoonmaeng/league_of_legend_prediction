def predict_match(model, match_data):
    match_features = list(match_data.columns[:-1])
    match_stats = match_data[match_features].values
    
    prediction = model.predict_proba(match_stats)
    
    probability = {
        'win_probability': float(prediction[0][0]),
        'lose_probability': float(prediction[0][1]),
    }
    
    return probability