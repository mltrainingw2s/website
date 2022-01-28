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

class Restmltext(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdf = models.CharField(max_length=100,null=True)
    docx = models.CharField(max_length=100,null=True)
    txt = models.CharField(max_length=100,null=True)
    final_abstract = models.CharField(max_length=100,null=True)

    class Meta:
        db_table = "RestText"