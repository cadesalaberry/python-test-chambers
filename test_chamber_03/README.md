# Test Chamber 3

## Various important advices
- Even if a programm can work for some specific cases, it's not necessarily correct
- Usually, a problem can be solved in different ways. Between 2 solutions, the best one is the easiest one, the most performant (in time, memory...), although these criteria are often contradictory

### Useful links

- Django Documentation  https://docs.djangoproject.com/en/2.0/
- Docker Documentation  https://docs.docker.com/
- Pycharm Professional (Trial) https://www.jetbrains.com/pycharm/
- Geojson online editor http://geojson.io/
- GeoJson http://geojson.org/

## Exercice 1: Installation

### Exercice 1.1

#### Linux / OSX

Install Docker & PyCharm.

Configure Pycharm to use the python3 interpreter of the container.
https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter-1.html

#### Windows

If you do not have Windows 10 pro or Enterprise, you cannot use Docker For Windows, you have to use Docker Toolbox : https://docs.docker.com/toolbox/toolbox_install_windows/

Do not forget to upgrade docker-machine after the install

```ShellSession
$ docker-machine upgrade default
```

If you use docker-machine (for Windows with Docker  Toolbox for instance) replace `localhost` with the virtual machine IP ex: `192.168.99.100`

#### Start the services

```ShellSession
$ docker-compose up -d test_chamber database traefik
```

If everything goes well, an http service should be available on `http://localhost:81/assets` (or `http://192.168.99.100/assets` if you use Docker Toolbox.)

**Example request using httpie**

```
$ http GET http://localhost:81/assets
```

```http
HTTP/1.1 400 Bad Request
Content-Length: 45
Content-Type: application/json
Date: Tue, 15 May 2018 06:09:05 GMT
Server: gunicorn/19.8.1
X-Frame-Options: SAMEORIGIN

{
    "message": "Unimplemented get_assets view."
}
```

### Exercice 1.2

Add the environment variable `DEVELOPMENT=yes` to the test_chamber service.

**Container update**
```ShellSession
$ docker-compose up -d test_chamber
```

The application code should be automatically updated.

## Exercice 2: API REST

A sample dataset (sample_data.json) is provided within the project.

### Exercice 2.1

Develop a view `add_asset` in the views.py file to add an `Asset` with a geojson format

```http
POST /assets
Content-Type: application/json

{
    "type": "Feature",
    "properties": {
        "asset_id": "wgs_montpellier"
    },
    "geometry": {
        "type": "Point",
            "coordinates": [
                3.8793405890464783,
                43.60545245109081
            ]
    }
}
```

### Exercice 2.2

Develop a view `get_asset` in the views.py file to return an `Asset` with a geojson format

```http
GET /assets/wgs_montpellier
Accept-Encoding: gzip, deflate
```

**Exemple de réponse http**
```http
Content-Type: application/json

{
    "type": "Feature",
    "properties": {
        "asset_id": "wgs_montpellier"
    },
    "geometry": {
    "type": "Point",
        "coordinates": [
            3.8793405890464783,
            43.60545245109081
        ]
    }
}
```

### Exercice 2.3
Add the functionnality to import several `Asset` in one time with a geojson format

```http
POST /assets
Content-Type: application/json

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "asset_id": "wgs_montpellier"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          3.8793405890464783,
          43.60545245109081
        ]
      }
    },
    {
        "type": "Feature",
        "properties": {
            "asset_id": "bcb"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                3.880721926689148,
                43.61530638830013
            ]
        }
    },
  ]
}
```

## Exercice 3: Search around a point

### Exercice 3.1
Add a view which returns the 3 closest assets from coordinates (latitude, longitude) sent as request params (GET) with a geojson format.
These assets have to be sorted by distance.

```http
GET /assets/search?lng=3.883&lat=43.6
Accept-Encoding: gzip, deflate
```

```http
Content-Type: application/json

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "asset_id": "wgs_montpellier"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          3.8793405890464783,
          43.60545245109081
        ]
      }
    }
  ]
}
```

### Exercice 3.2

For each asset returned by the search request `/assets/search?lng=3.883&lat=43.6`, add a `distance` field which is the distance between the asset and the coordinates sent as params.

## Exercice 4: Migrations & databases

### Exercice 4.1

Add a field `created_at` of type `Datetime` to the `Asset` model which is defined in the models.py file.
Add a database index to the `asset_id` field.
```python
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import CharField


class Asset(models.Model):
    geography = PointField(geography=True)
    asset_id = CharField(max_length=255, unique=True)
```

Don't forget to build the migration:
```ShellSession
$ docker-compose run --rm test_chamber ./manage.py makemigrations
```

### Exercice 4.2

Add `created_at` to the serialized assets.

### Exercice 4.3
Use `postgresql` instead of `sqlite` database. (https://docs.djangoproject.com/en/2.0/ref/contrib/gis/)

Use the connection configuration defined in the file `databases/woosmapdb/initdb-postgis-database.sh`
and use `database` as host (cf `docker-compose.yml`)

Add psycopg2-binary to the requirements.

Rebuild the image:
```ShellSession
$ docker-compose build test_chamber
```

### Bonus
Send these settings through environment variables in the docker-compose.yml

### Problems & Solutions

#### 404 with Traefik

https://docs.traefik.io/

If you get a 404 error, the problem might come from the reverse proxy (traefik) configuration. To check the configuration of traefik, you can go to the web admin `http://192.168.99.100:8082`
The frontend "_Route Rule_" may have a badly configured host, in this case, you have to set the good value to the HOSTNAME environment variable.
```ShellSession
$ export HOSTNAME=192.168.99.100
```

#### docker compose error withs windows

If you get this error, you can try to restart traefik with Docker for Windows.

```
ERROR: for test_chamber_03_solution_traefik_1  Cannot create container for service traefik: b'Mount denied:\nThe source path "\\\\var\\\\run\\\\docker.sock:/var/run/docker.sock"\nis not a valid Windows path'
ERROR: for traefik  Cannot create container for service traefik: b'Mount denied:\nThe source path "\\\\var\\\\run\\\\docker.sock:/var/run/docker.sock"\nis not a valid Windows path'
ERROR: Encountered errors while bringing up the project.
```

You have to add `COMPOSE_CONVERT_WINDOWS_PATHS=1` to the environment variables before launching the docker-compose command

**PowerShell**

``` powershell
$env:COMPOSE_CONVERT_WINDOWS_PATHS=1
```
