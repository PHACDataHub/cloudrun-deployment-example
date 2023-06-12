from django.contrib import admin
# make hello world app modifyable in the admin page
from .models import City

admin.site.register(City)
