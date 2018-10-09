# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.


class UrlMapper(models.Model):
    url = models.TextField()
    key = models.CharField(max_length=settings.URL_SHORTNER_SIZE, null=False, unique=True, db_index=True)
