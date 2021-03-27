#!/bin/sh

psql --username=postgres <<-EOSQL
    CREATE DATABASE "template_postgis" ;
    UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis' ;

EOSQL

psql --username=postgres template_postgis <<-EOSQL
    CREATE EXTENSION postgis;
EOSQL

psql --username=postgres <<-EOSQL
    CREATE ROLE "api" SUPERUSER LOGIN PASSWORD 'nopass';
    CREATE DATABASE "api" TEMPLATE template_postgis OWNER "api";
EOSQL
