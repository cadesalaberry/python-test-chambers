FROM postgres:10.3

ENV POSTGIS_MAJOR 2.4

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-${POSTGIS_MAJOR} \
           postgresql-$PG_MAJOR-postgis-${POSTGIS_MAJOR}-scripts \
      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis-database.sh /docker-entrypoint-initdb.d/postgis.sh
COPY ./docker-healthcheck.sh /usr/local/bin/docker-healthcheck.sh

HEALTHCHECK CMD /usr/local/bin/docker-healthcheck.sh
