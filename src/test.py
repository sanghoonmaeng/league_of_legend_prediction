import requests

url = 'http://localhost:9696/predict'
summoner = {'summoner_name': 'garlicduck'}

response = requests.post(url, json=summoner).json()
print(response)
