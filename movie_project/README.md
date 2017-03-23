
This evaluation consists of a Django project called ICDB, the Internet Cinema
Database, which is a database of cars exposed through a REST API.

The API is currently able to create and list cinemas/movies using JSON representations.


we have to run following to install dependencies:
python setup.py install

Then, we have to create the sqlite database and load the sample data:
    python manage.py syncdb
    python manage.py loaddata sample_movies

Running tests:
    python manage.py test


