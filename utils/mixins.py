from django.db import models
import uuid

class TimeStampsMixin(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDFieldMixin(models.Model):
    """
    Adds a unique and uneditable UUIDField
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
