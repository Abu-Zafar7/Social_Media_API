from rest_framework import routers
from django.urls import path
from . import views
from .serializers import UserLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = routers.DefaultRouter()







urlpatterns = [
    path('',views.home),
    path('api/follow/<str:id>', views.follow,name="follow_user"),
    path('api/unfollow/<str:id>', views.unfollow, name= 'unfollow_user'),
    path('api/like/post/<str:id>', views.like, name='like'),
    path('api/unlike/post/<str:id>', views.unlike_post, name= 'unlike'),
    path('api/user/<str:username>/',views.user_details, name='user_detail'),
    path('api/post/add', views.post_add, name="add_post"),
    path('api/post/<str:pk>',views.delete_post, name='delete_post'),
    path('api/comment/post/<str:id>',views.add_comment, name='comment'),
    path('api/all_posts',views.get_posts, name='posts'),
    path('api/get_post/<str:id>',views.get_post,name='post'),
    path('api/authenticate/',TokenObtainPairView.as_view(),name='user_login')
]