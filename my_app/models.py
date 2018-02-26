from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime


class Link(models.Model):
    path = models.CharField(max_length=128, null=True)
    file = models.FileField(null=True, upload_to='uploads/')
    link_password = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True)
    my_user = models.ForeignKey(User, on_delete=models.CASCADE)
    valid = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, unique=True)
    # how many times link was displayed
    link_displays = models.IntegerField(default=0)

    @property
    def link_info(self):
        return "Added: {} by {}".format(self.creation_date
                                            .strftime("%Y-%m-%d, %H:%M:%S"),
                                        self.my_user.username)

    @property
    def valid_for(self):
        return 'Link will be valid until {} which is exactly 24H.'\
            .format(self.creation_date + timedelta(days=1))

    @property
    def is_valid(self):
        if (self.creation_date - datetime.datetime.now()).seconds < 10:
            return True
        else:
            self.valid = False
            return False

    def __str__(self):
        return "Link ID:" + str(self.id) + " " + self.link_info



