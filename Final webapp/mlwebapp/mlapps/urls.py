from django.urls import path
from . import views
from .views import UpdatePostView

urlpatterns = [

    path('',views.index, name="index"),
    path('image/',views.imgdetect, name="image"),
    path('mlmodel/',views.dash,name="mlmodel"),
    path('webcam/',views.videodetect, name="webcam"),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('snap_feed/',views.snaps().snap_feed,name='snap_feed'),
    path('snapcam/',views.snaps().snapdetect,name='snap_detect'),
    

    path("", views.index, name="index"),
    path("blogs/", views.blogs, name="blogs"),
    path("all_blog/", views.all_blog, name="all_blog"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("all_blog/blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("blogs/blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("blogs/delete_blog_post/<str:slug>/", views.Delete_Blog_Post, name="delete_blog_post"),
    path("search/", views.search, name="search"),
    
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    
]