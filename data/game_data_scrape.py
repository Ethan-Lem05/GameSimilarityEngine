import requests
from dotenv import load_dotenv
import os

load_dotenv()
IGDB_CLIENT_ID = os.getenv('IGDB_API_CLIENT')
IGDB_SECRET = os.getenv('IGDB_API_SECRET')
IGDB_TOKEN = os.getenv('ACCESS_TOKEN')

def get_api_key():
    try:
        response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={IGDB_CLIENT_ID}&client_secret={IGDB_SECRET}&grant_type=client_credentials")
    except Exception as e:
        print(e)
        return
    print(str(response.text))

def get_game_data():
    headers = {'Client-ID': f"{IGDB_CLIENT_ID}", 'Authorization': f"Bearer {IGDB_TOKEN}"}
    body = '''
    fields name, genres.name, summary, storyline, screenshots, themes.name, keywords.name; limit 2;
    '''

    try:
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=body)

        # Check if the request was successful
        if response.status_code == 200:
            # Try parsing the response as JSON
            data = response.json()
            with open('response.txt', 'w', encoding='utf-8') as file:
                file.write(str(data))  # Write the parsed JSON to the file
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # get_api_key()
    get_game_data()
    pass

if __name__ == "__main__":
    main()