from rest_framework import serializers
from .models import Restmlimage,Restmlwebcam

class mlimageserializer(serializers.ModelSerializer):
    class Meta:
        model = Restmlimage
        fields = ['id','image_upload','smile_percentage']

