import time
from jikanpy import Jikan

def fetch_sample_anime():
    jikan = Jikan()
    
    anime_database = []
    
    print("Fetching top anime from MyAnimeList...")
    
    try:
        top_anime = jikan.search('anime', 'sword', page=1)
        
        for anime in top_anime['data']:
            # only extract the data we need
            anime_entry = {
                "mal_id": anime['mal_id'],
                "title": anime['title'],
                "synopsis": anime['synopsis'],
                "genres": [genre['name'] for genre in anime.get('genres', [])]
            }
            anime_database.append(anime_entry)
            print(f"Fetched: {anime_entry['title']}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print(f"\nSuccessfully fetched {len(anime_database)} anime!")
    return anime_database

if __name__ == "__main__":
    data = fetch_sample_anime()
    
    # for testing
    if data:
        print("\nSample Data:")
        print(data[0])