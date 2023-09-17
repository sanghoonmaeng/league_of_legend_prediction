# Config for Riot API requests
API_KEY = 'YOUR API KEY'
SERVER = 'NA1' # NA1, EUW1, AP-SOUTHEAST-1, etc.
REGION = 'americas' # Will be different based on your server
QUEUE = 'RANKED_SOLO_5x5' # Game type for ranked match
QUEUE_ID = 420 # Solo ranked matches only
PLAYERS = 1 # Number of players from a ranked queue
NUM_GAMES = 1 # Number of games played per player

# File path to the best prediction model
MODEL_FILE_PATH = 'model/win_prediction_xgb_model.bin'