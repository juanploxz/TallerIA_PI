import numpy as np

from .models import Movie
from .openai_utils import get_openai_client


EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(text):
    client = get_openai_client()
    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


def cosine_similarity(a, b):
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def get_movie_embedding(movie):
    if not movie.emb:
        return None
    return np.frombuffer(movie.emb, dtype=np.float32)


def find_best_movie_for_prompt(prompt):
    prompt_embedding = get_embedding(prompt)
    best_movie = None
    best_similarity = -1.0

    for movie in Movie.objects.all():
        movie_embedding = get_movie_embedding(movie)
        if movie_embedding is None or movie_embedding.size == 0:
            continue

        similarity = cosine_similarity(prompt_embedding, movie_embedding)
        if similarity > best_similarity:
            best_similarity = similarity
            best_movie = movie

    return best_movie, best_similarity
