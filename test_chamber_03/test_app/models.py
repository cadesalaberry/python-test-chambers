from django.contrib.gis.db.models import PointField
from django.db import models


class Asset(models.Model):
    geography = PointField(geography=True)
    asset_id = models.CharField(max_length=255, unique=True)
