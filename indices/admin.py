import inspect

from django.contrib import admin
from django.db import models
import indices.models


# auto register models to admin site
for _, cls in inspect.getmembers(indices.models, predicate=inspect.isclass):
    if cls.__module__ == 'indices.models' and issubclass(cls, models.Model):
        admin.site.register(cls)
