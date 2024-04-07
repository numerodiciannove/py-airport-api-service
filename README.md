# Airport API Service

API service for tracking flights from airports across the whole globe.

## For testing on externul domain you can use this:

- Works only on http!
- [http://huy.skin/](http://huy.skin/)
- https://huy.skin/admin/
- login: admin@admin.com
- pass: admin

## Installing using GitHub:

Install PostgreSQL and create db

```shell
git clone https://github.com/numerodiciannove/py-airport-api-service
cd py-airport-api-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DJANGO_DEBUG=<True/False>
set DJANGO_SECRET_KEY=<your secret key>
set POSTGRES_DB=<your db name>
set POSTGRES_HOST=<your db hostname>
set POSTGRES_PORT=<your db port>
set POSTGRES_USER=<your db username>
set POSTGRES_PASSWORD=<your db user password>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Run with docker:

Docker should be installed

```shell
docker-compose build
docker-compose up
```

## Getting access:

- create user via /api/v1/user/register/
- get access token via /api/v1/user/token/

## Documentation:

- Documentation available via /api/v1/doc/swagger/

## Test Data Fixtures:

You can use the following fixture files for testing the database:

- 1_countries_cities_airports_db_fixture.json
- 2_airplane_types_airplanes_db_fixture.json
- 3_routes_db_fixture.json
- 4_crew_db_fixture.json
- 5_flight_db_dixture.json

To load fixtures into the database, you can use the following command:

```shell
python manage.py loaddata <fixture_file_name>
```

## DB-structure diagram:

![bd_diagram.jpg](github_imgs%2Fbd_diagram.jpg)

## Browsable API examples:

![api_root.jpg](github_imgs%2Fapi_root.jpg)

![Authentication_1.jpg](github_imgs%2FAuthentication_1.jpg)

![user.jpg](github_imgs%2Fuser.jpg)

![airport_list.jpg](github_imgs%2Fairport_list.jpg)

![paginated.jpg](github_imgs%2Fpaginated.jpg)

![flights.jpg](github_imgs%2Fflights.jpg)

## Swagger:

![Airport_System_API.jpg](github_imgs%2FAirport_System_API.jpg)
