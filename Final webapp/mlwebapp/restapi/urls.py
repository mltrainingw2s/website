from django.urls import path
from . import views

urlpatterns = [
    path('mlimage/',views.Image_detect.as_view(),name='restimage'),
]