from pgvector.django import CosineDistance

from ..models import Documentchunk
from .embedding import generate_embedding


def semantic_search(question, user):
    query_embedding = generate_embedding(question)

    return (
        Documentchunk.objects.filter(document__user=user)
        .select_related("document")
        .annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:5]
    )
