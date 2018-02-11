from django.db import models
from django.contrib.auth.models import User
import random


class Link(models.Model):
    path = models.CharField(max_length=128)
    link_password = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True)
    my_user = models.ForeignKey(User, on_delete=models.CASCADE)
    valid = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, unique=True)
    link_displays = models.IntegerField(default=0)

    @property
    def link_info(self):
        return "Added: {} by {}".format(self.creation_date
                                            .strftime("%Y-%m-%d, %H:%M:%S"),
                                        self.my_user.username)

    def __str__(self):
        return "Link ID:" + str(self.id) + " " + self.link_info

