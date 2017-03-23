"""Views for the Movies app."""
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from Movies.models import Movies
from Movies.forms import MovieForm

from django.views.generic import View


class MovieView(View):
  """A view for Movies."""
  http_method_names = ['get', 'post', 'put', 'delete']

  def get(self, request):
    """GET returns a list of objects.

    Args:
        request : Httprequest
        make: string
    Returns:
        HttpResponse
    """
    if request.GET.get('name'):
        movies = Movies.objects.filter(make=request.GET.get('name')).values()
    else:
        movies = Movies.objects.all()
    return render_to_response('movies.json', {'Movies': movies},
                                  mimetype='application/json')

  def post(self, request):
      """Adding a movie POST method
       Args:
        request : Httprequest
      Returns:
        HttpResponse
      """
      try:
        data = json.loads(request.body)
      except ValueError:
        return HttpResponseBadRequest('Not valid JSON!')

      form = MovieForm(data)

      if form.is_valid():
        movie = form.save()
        response = HttpResponse(status=201)
        response['Location'] = '/Movies/' + str(movie.id)
        return response
      else:
        return HttpResponseBadRequest('Invalid data!')

  def put(self, request):
    """updating a movie through PUT METHOD
    Args:
        request : Httprequest
    Returns:
        HttpResponse
    """
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest('Not valid JSON!')

    get_id = Movies.objects.get(id=data.get('id'))
    form = MovieForm(data, instance=get_id)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=200)
        return response
    else:
        return HttpResponseBadRequest('Invalid data!')

  def delete(self, request):
    """deleting a movie through DELETE METHOD.

    Args:
        request : Httprequest
    Returns:
        HttpResponse
    """
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest('Not valid JSON!')
    Movies.objects.filter(id=data.get('id')).delete()
    response = HttpResponse(status=202)
    return response
