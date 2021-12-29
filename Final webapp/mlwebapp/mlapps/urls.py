from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="index"),
    path('/image/',views.imgdetect, name="image"),
    path('/webcam/',views.videodetect, name="webcam"),
    path('/video_feed/', views.video_feed, name='video_feed'),
    path('/snap_feed/',views.snaps().snap_feed,name='snap_feed'),
    path('/snapcam/',views.snaps().snapdetect,name='snap_detect'),
]