import requests
import os
import time
import csv
import schedule
from dotenv import load_dotenv

load_dotenv()

polygon_api_key = os.getenv("POLYGON_API_KEY")
print("API Key:", polygon_api_key)

LIMIT = 1000

# Example ticker schema for CSV structure
example_ticker = {'ticker': 'GVI', 
                  'name': 'iShares Intermediate Government/Credit Bond ETF', 
                  'market': 'stocks', 
                  'locale': 'us',
                  'primary_exchange': 'BATS', 
                  'type': 'ETF', 'active': True, 
                  'currency_name': 'usd', 
                  'cik': '0000913414', 
                  'composite_figi': 'BBG000QN3319', 
                  'share_class_figi': 'BBG001SSD885', 
                  'last_updated_utc': '2025-09-19T06:05:18.516588033Z'}

# Create CSV file with the same data structure as example_ticker
def create_tickers_csv(tickers_data, filename='stock_tickers.csv'):
    """
    Create a CSV file with the same structure as example_ticker
    """
    if not tickers_data:
        print("No ticker data to write to CSV")
        return
    
    # Get the fieldnames from the first ticker (or example_ticker if no data)
    fieldnames = list(example_ticker.keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write ticker data
        for ticker in tickers_data:
            # Ensure all fields from example_ticker are present
            row = {}
            for field in fieldnames:
                row[field] = ticker.get(field, '')  # Use empty string if field is missing
            writer.writerow(row)
    
    print(f"✅ CSV file '{filename}' created successfully with {len(tickers_data)} tickers")

def run_stock_ticker_scraper_job():
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={polygon_api_key}'
    tickers = []

    def get_response(url):
        """
        Helper function to get a response and handle rate limits.
        """
        while True:
            response = requests.get(url)
            if response.status_code == 429:
                print("Rate limit hit. Sleeping for 60 seconds...")
                time.sleep(60)
            else:
                return response

    # First request
    response = get_response(url)
    data = response.json()

    # Add first page of results
    if 'results' in data:
        for ticker in data['results']:
            tickers.append(ticker)
    else:
        print("First page: No 'results' found.")
        print(data)

    # Loop through paginated results
    while 'next_url' in data:
        print('Requesting next page:', data['next_url'])
        time.sleep(1.5)  # Small delay to avoid rapid-fire requests

        response = get_response(data['next_url'] + f"&apiKey={polygon_api_key}")
        data = response.json()

        if 'results' in data:
            for ticker in data['results']:
                tickers.append(ticker)
        else:
            print("❌ 'results' not found in response:", data)
            break  # Exit if something goes wrong

    print(f"\n✅ Total tickers collected: {len(tickers)}")

    # Create CSV file with the same data structure as example_ticker
    create_tickers_csv(tickers)

## Prompt to Cursor AI to create the csv file: in the script2.py, write the code that uses the example_ticker schema to create a csv file of the stock ticker with same data structure

if __name__ == "__main__":
    run_stock_ticker_scraper_job()