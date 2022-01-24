from django.db import models

# Create your models here.

class Restmlimage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_upload = models.CharField(max_length=300, null=True)
    smile_percentage = models.CharField(max_length=2000,null=True)

    class Meta:
        db_table = "RestImage"

class Restmlwebcam(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_upload = models.CharField(max_length = 300, null=True)
    smile_percentage = models.CharField(max_length=2000,null=True)

    class Meta:
        db_table = "RestWebcam"   