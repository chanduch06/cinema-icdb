"""
Forms for the movies app.
"""
from django import forms
from Movies.models import Movies


class MovieForm(forms.ModelForm):
    """Form for the Movie model."""
    class Meta:
        model = Movies
