from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Ml_Image(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_upload = models.CharField(max_length=250,null = True)
    smile_percentage = models.IntegerField(null = True)
    image_type = models.IntegerField(null = True)
    class Meta:
        db_table = 'Image'