from django.contrib import admin
from .models import Link


@admin.register(Link)
class Link(admin.ModelAdmin):
    pass

