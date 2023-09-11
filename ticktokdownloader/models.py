from django.db import models

# Create your models here.

class Files(models.Model):
    uid = models.CharField(max_length=100)
    path_nowatermark = models.TextField()
    path_watermark = models.TextField()
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField()