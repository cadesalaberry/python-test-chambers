#!/usr/bin/env bash

set -e

docker-compose run --rm test_chamber ./manage.py test
