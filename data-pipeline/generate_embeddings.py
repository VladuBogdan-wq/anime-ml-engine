import json
from sentence_transformers import SentenceTransformer

def load_anime_data(filename="anime_data.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_embeddings(anime_list, model_name="all-MiniLM-L6-v2"):
    """
    generates a vector embedding for each anime's synopsis.
    """
    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)

    # Pull out just the synopses, in the same order as anime_list
    synopses = [anime["synopsis"] for anime in anime_list]

    print(f"Generating embeddings for {len(synopses)} anime...")
    embeddings = model.encode(synopses, show_progress_bar=True)

    # Attach each embedding back onto its anime entry
    for anime, embedding in zip(anime_list, embeddings):
        anime["embedding"] = embedding.tolist()  # numpy array -> plain list for JSON

    return anime_list


def save_with_embeddings(data, filename="anime_data_with_embeddings.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} anime entries with embeddings to {filename}")


if __name__ == "__main__":
    anime_list = load_anime_data()
    anime_list = generate_embeddings(anime_list)
    save_with_embeddings(anime_list)

    # for testing
    sample = anime_list[0]
    print(f"\nSample: {sample['title']}")
    print(f"Embedding length: {len(sample['embedding'])}")
    print(f"First 5 values: {sample['embedding'][:5]}")