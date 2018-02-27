from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import datetime


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

    def field_to_datetime(self):
        y = self.creation_date.year
        m = self.creation_date.month
        d = self.creation_date.day
        h = self.creation_date.hour
        s = self.creation_date.second
        return datetime.datetime(y, m, d, h, s)

    @property
    def valid_for(self):
        return 'Link will be valid until {}.'\
            .format(self.field_to_datetime() + timedelta(days=1))

    @property
    def is_valid(self):
        if (datetime.datetime.now() - self.field_to_datetime()).seconds < \
                                                                  24 * 3600:
            return True
        else:
            # set link as not valid
            self.valid = False
            self.save()
            return False

    def __str__(self):
        return "Link ID:" + str(self.id) + " " + self.link_info



