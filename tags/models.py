from __future__ import unicode_literals

from django.db import models
# from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return 'id={}, name="{}"'.format(self.id, self.name)


@python_2_unicode_compatible
class FacebookImage(models.Model):
    url = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return 'id={}, url="{}", tags.length={}'.format(self.id, self.url, self.tags.count())

