import json
import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Process IP address.')
    
# Add the --ip argument
parser.add_argument('--ip', required=True, help='IP address to process')
    
 # Parse the arguments
args = parser.parse_args()

def post_data():
    try:
        # URL to send the JSON data to
        url = 'http://localhost:8000/api/trpc/cpe_status.update'

            
        # Open and read the JSON file
        with open(f'status-{args.ip}.json', 'r') as file:
            json_data = json.load(file)

        # Send the JSON data to the API endpoint
        response = requests.post(url, json=json_data)

        # Print the response (for verification purposes)
        print(response.status_code)
        print(response.text)
    finally:
        print('finsihed updating database')
    

if __name__ == "__main__":
   post_data()
   sys.exit()
