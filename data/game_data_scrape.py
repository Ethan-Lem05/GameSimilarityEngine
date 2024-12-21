import requests
from dotenv import load_dotenv
import os
import pandas as pd
import random

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
    headers = {
        'Client-ID': f"{IGDB_CLIENT_ID}",
        'Authorization': f"Bearer {IGDB_TOKEN}"
    }

    body = f'''fields name, genres.name, summary, storyline, cover.url, themes.name, keywords.name, rating, websites.url;
    limit 500;
    sort total_rating desc;
    where total_rating != null;
    offset {500};
    '''
    try:
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=body)
        # Check if the request was successful
        if response.status_code == 200:
            # Try parsing the response as JSON
            data = response.json()
            print(data)

            columns_order = ['id', 'name', 'summary', 'storyline', 'themes', 'keywords', 'genres', 'cover','rating', 'websites']

            df = pd.DataFrame(data)
            df = df.reindex(columns=columns_order)

            # Processing each row to handle nested fields
            for index, row in df.iterrows():
                print(f"Processing row {index}")

                # Handle websites
                websites = row.get('websites', [])
                if isinstance(websites, list):
                    df.at[index, 'websites'] = ', '.join([website['url'] for website in websites])
                else:
                    df.at[index, 'websites'] = ''
                
                # Handle genres
                genres = row.get('genres', [])
                if isinstance(genres, list):
                    df.at[index, 'genres'] = ', '.join([genre['name'] for genre in genres])
                else:
                    df.at[index, 'genres'] = ''

                # Handle themes
                themes = row.get('themes', [])
                if isinstance(themes, list):
                    df.at[index, 'themes'] = ', '.join([theme['name'] for theme in themes])
                else:
                    df.at[index, 'themes'] = ''

                # Handle keywords
                keywords = row.get('keywords', [])
                if isinstance(keywords, list):
                    df.at[index, 'keywords'] = ', '.join([keyword['name'] for keyword in keywords])
                else:
                    df.at[index, 'keywords'] = ''
                
                images = row.get('cover', [])
                if isinstance(images, dict):
                    df.at[index, 'cover'] = images['url']
                else:
                    df.at[index, 'cover'] = ''

                # Print the processed row
                print(df.iloc[index].to_string())
                # Save the raw response to a file
            with open('data/response.csv', 'a', encoding='utf-8') as file:
                file.write(df.to_csv(index=False, header=False))
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