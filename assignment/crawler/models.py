# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PdfDocument(models.Model):

    name = models.CharField(max_length=255)

    def urls_count(self):
        return self.url_set.count()

    def __unicode__(self):
        return self.name


class Url(models.Model):

    url = models.URLField(max_length=255, unique=True)
    pdf = models.ManyToManyField(PdfDocument)
    status = models.CharField(max_length=3, blank=True)  # HTTP Status Code

    def __unicode__(self):
        return self.url
