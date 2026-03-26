from django.db import models
import numpy as np


def get_default_embedding_bytes():
    return np.zeros(1536, dtype=np.float32).tobytes()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500, blank=True)
    image = models.ImageField(
        upload_to='movie/images/',
        default='movie/images/default.JPG',
    )
    url = models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)
    emb = models.BinaryField(default=get_default_embedding_bytes)

    def __str__(self):
        return self.title
