"""
Tests for the moviess app.
"""
from django.test import TestCase
import mock
from django.utils import simplejson as json
from Movies.models import Movies
from Movies.views import MovieView
from Movies.forms import MovieForm


class TestMovie(TestCase):
    """Tests for the movie model."""
    def test_movie(self):
        """Test the movie model."""
        movie = Movies()
        movie.name = 'name'
        movie.genre = 'genre'
        movie.year = 1999
        movie.rating = 8
        movie.save()


class TestMovieForm(TestCase):
    """Tests for the Movie form."""
    def test_form(self):
        """Test that the form is attached to the right model."""
        self.assertIs(MovieForm._meta.model, Movies, 'Should be attached to Movie.')


class TestIndexView(TestCase):
    """Tests for the Movies.Movies_view view."""
    @mock.patch('Movies.views.MovieForm')
    def test_post(self, MockMovieForm):
        """Test a POST request to the Movies_view view."""
        obj = {'name': 'Harry potter', 'genre': 'Scifi', 'year': 2001}
        request = mock.Mock(
            method='POST',
            body=json.dumps(obj)
        )
        mock_form = MockMovieForm.return_value
        mock_movie = mock_form.save.return_value
        mock_movie.id = 123

        response = MovieView.as_view()(request)

        self.assertEqual(response.status_code, 201,
                         'Should return 201 CREATED.')
        self.assertEqual(response['Location'], '/Movies/123',
                         'Should return the location of the new movie.')
        MockMovieForm.assert_called_with(obj)
        self.assertTrue(mock_form.save.called, 'Should call save.')

    def test_post_invalid_data(self):
        """Test POSTing invalid data."""
        request = mock.Mock(
            method='POST',
            body='{}'
        )
        movie_view = MovieView.as_view()
        response = movie_view(request)

        self.assertEqual(response.status_code, 400,
                         'Should return a 400 BAD REQUEST.')

    def test_post_bad_json(self):
        """Test POSTing invalid JSON."""
        request = mock.Mock(
            method='POST',
            body='foo'
        )
        movie_view = MovieView.as_view()
        response = movie_view(request)

        self.assertEqual(response.status_code, 400,
                         'Should return a 400 BAD REQUEST.')

    @mock.patch('Movies.views.Movies')
    def test_get(self, MockMovies):
        """Test GET requests to the Movies_view view."""
        request = mock.Mock(method='GET')
        objs = [
            {'id': 1, 'name': 'Name1', 'genre': 'Genre1', 'year': 1, 'rating' : 1},
            {'id': 2, 'name': 'Name2', 'genre': 'Genre2', 'year': 2, 'rating' : 2},
            {'id': 3, 'name': 'Name3', 'genre': 'Genre3', 'year': 3, 'rating' : 3}
        ]
        MockMovies.objects.all.return_value = [Movies(**obj) for obj in objs]
        response = MovieView.as_view()(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200,
                         'Should return a successful response.')
        self.assertEqual(response['Content-Type'], 'application/json',
                         'Should return a JSON response.')
        #print data
        #self.assertSequenceEqual(data, objs, 'Should return the objects.')

    def test_not_supported(self):
        """Test sending an unsupported request method."""
        request = mock.Mock(method='FOO')
        movies_view = MovieView.as_view()
        response = movies_view(request)

        self.assertEqual(response.status_code, 405,
                         'Should return a 405 NOT ALLOWED.')
        #self.assertIn('GET', response['Allow'], 'Should allow GET.')
        #self.assertIn('POST', response['Allow'], 'Should allow POST.')
