from __future__ import unicode_literals

from django.db import models
# from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return 'id={}, name="{}"'.format(self.id, self.name)


# TODO
# @python_2_unicode_compatible
# class UserTag(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     num = models.IntegerField()
#
#     def __str__(self):
#         return 'id={}, user_id={}, tag_id={}, num={}'.format(
#             self.id, self.user_id, self.tag_id, self.num
#         )
#
