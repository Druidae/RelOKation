from unittest.util import _MAX_LENGTH
from django.db import models


class Countries(models.Model):
    country_name = models.CharField(max_length=255)
    