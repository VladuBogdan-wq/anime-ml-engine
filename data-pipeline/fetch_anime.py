import time
import json
from jikanpy import Jikan

def fetch_top_anime(num_pages=4):
    jikan = Jikan()
    anime_database = []

    print(f"Fetching top anime from MyAnimeList ({num_pages} pages)...")

    for page in range(1, num_pages + 1):
        try:
            print(f"\nFetching page {page}")
            response = jikan.top(type='anime', page=page)

            for anime in response['data']:
                anime_entry = {
                    "mal_id": anime['mal_id'],
                    "title": anime['title'],
                    "synopsis": anime.get('synopsis') or "",
                    "genres": [genre['name'] for genre in anime.get('genres', [])]
                }

                # Skip entries with no synopsis
                if not anime_entry["synopsis"]:
                    print(f"Skipped (no synopsis): {anime_entry['title']}")
                    continue

                anime_database.append(anime_entry)
                print(f"Fetched: {anime_entry['title']}")

            # Jikan rate limit: 3 requests/second, 60/minute
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred on page {page}: {e}")
            continue

    print(f"\nSuccessfully fetched {len(anime_database)} anime!")
    return anime_database


def save_to_json(data, filename="anime_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} anime entries to {filename}")


if __name__ == "__main__":
    data = fetch_top_anime(num_pages=4)

    if data:
        save_to_json(data)
        print("\nSample Data:")
        print(data[0])