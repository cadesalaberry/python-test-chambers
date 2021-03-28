from django.contrib.gis.db.models import PointField
from django.db import models
from rest_framework import serializers


class Asset(models.Model):
    geography = PointField(geography=True, srid=4326)
    asset_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SearchQuerySerializer(serializers.Serializer):
    lat = serializers.DecimalField(required=True, max_digits=18, decimal_places=16)
    lng = serializers.DecimalField(required=True, max_digits=18, decimal_places=16)

class CoordinatesSerializer(serializers.ListField):
    # https://stackoverflow.com/questions/15965166/what-are-the-lengths-of-location-coordinates-latitude-and-longitude
    # max_digits=11, decimal_places=8 should be enough
    # sample data suggests: max_digits=18, decimal_places=16
    child = serializers.DecimalField(required=True, max_digits=18, decimal_places=16)
    max_length = 2
    min_length = 2

class PointSerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=[('Point', 'Point')])
    coordinates = CoordinatesSerializer()

class FeaturePropSerializer(serializers.Serializer):
    asset_id = serializers.SlugField(required=True, min_length=1, max_length=255)

class FeatureSerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=[('Feature', 'Feature')])
    geometry = PointSerializer()
    properties = FeaturePropSerializer()

class FeatureCollectionSerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=[('FeatureCollection', 'FeatureCollection')])
    features = serializers.ListField(child=FeatureSerializer())

class UnknownQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=[
        ('FeatureCollection', 'FeatureCollection'),
        ('Feature', 'Feature'),
    ])
