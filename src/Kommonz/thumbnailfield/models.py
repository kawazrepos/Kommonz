from django.db import models

from django.db.models.fields.files import ImageField
class ThumbnailField(ImageField):
    def __init__(self):
