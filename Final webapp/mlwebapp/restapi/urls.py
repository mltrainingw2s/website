from django.urls import path
from . import views

urlpatterns = [
    path('mlimage/',views.Image_detect.as_view(),name='restimage'),
    path('mltexts/',views.Text_file.as_view(),name='restfile'),
]