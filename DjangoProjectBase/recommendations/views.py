from django.shortcuts import render

from movie.recommendation_utils import find_best_movie_for_prompt


def search(request):
    prompt = request.GET.get('prompt', '').strip()
    movie = None
    similarity = None
    error = None
    info = None

    if prompt:
        try:
            movie, similarity = find_best_movie_for_prompt(prompt)
            if movie is None:
                info = (
                    "No se encontro una recomendacion disponible. "
                    "Verifica que existan embeddings cargados para las peliculas."
                )
        except Exception as exc:
            error = str(exc)

    return render(
        request,
        'recommendations/search.html',
        {
            'prompt': prompt,
            'movie': movie,
            'similarity': similarity,
            'error': error,
            'info': info,
        },
    )
