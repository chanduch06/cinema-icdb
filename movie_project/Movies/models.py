"""
Models for the Movies app.
"""
from django.db import models


class Movies(models.Model):
    """A Movie."""
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.IntegerField()