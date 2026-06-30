import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

COLLECTION_NAME = "anime"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 output dimension


def load_data(filename="anime_data_with_embeddings.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def setup_collection(client):
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' created.")


def upload_anime(client, anime_list):
    """
    Converts each anime entry into a Qdrant PointStruct and upserts
    them in a single batch call
    """
    points = []

    for anime in anime_list:
        point = PointStruct(
            id=anime["mal_id"],  # no need to generate our own id for now at least, just use the MAL one
            vector=anime["embedding"],
            payload={
                "title": anime["title"],
                "synopsis": anime["synopsis"],
                "genres": anime["genres"],
            }
        )
        points.append(point)

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Uploaded {len(points)} anime to Qdrant.")


def test_search(client, query_vector, top_k=3):
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )

    print(f"\nTop {top_k} results for test query:")
    for result in response.points:
        print(f"  Score: {result.score:.4f} | {result.payload['title']}")



if __name__ == "__main__":
    client = QdrantClient(host="localhost", port=6333)

    setup_collection(client)

    anime_list = load_data()
    upload_anime(client, anime_list)

    # for testing
    test_search(client, anime_list[0]["embedding"])