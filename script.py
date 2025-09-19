import requests
import os
import openai 
import time
from dotenv import load_dotenv

load_dotenv()

polygon_api_key = os.getenv("POLYGON_API_KEY")
print(polygon_api_key)
LIMIT = 1000
url =  f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={polygon_api_key}'
response = requests.get(url)
# print(response.json())
tickers = []

data = response.json()
# print(data['next_url'])
for ticker in data['results']:
    tickers.append(ticker)
while 'next_url' in data:
    print('requesting next page', data['next_url'])
    time.sleep(60)
    response = requests.get(data['next_url'] + f'&apiKey={polygon_api_key}')
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)
    
print(len(tickers))