
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('',views.home),
    path('api/authenticate/',TokenObtainPairView.as_view(),name='user_login'), #authenticates a user
    path('api/follow/<str:id>', views.follow,name="follow_user"), #authenticated user follows an authenticated user
    path('api/unfollow/<str:id>', views.unfollow, name= 'unfollow_user'), #authenticated user unfollows an authenticated user
    path('api/like/post/<str:id>', views.like, name='like'), #authenticated user likes a post with <id>
    path('api/unlike/post/<str:id>', views.unlike_post, name= 'unlike'), #authenticated user unlikes a post with <id>
    path('api/user/<str:username>/',views.user_details, name='user_detail'), #returns details of a user such as their posts,the number of likes in their posts, followers and followings.
    path('api/post/add', views.post_add, name="add_post"), #authenticated user can add their own post
    path('api/post/<str:pk>',views.delete_post, name='delete_post'), #authenticated user can delete a post
    path('api/comment/post/<str:id>',views.add_comment, name='comment'), #authenticated user can add comment on a post with <id>
    path('api/all_posts',views.get_posts, name='posts'), #returns all posts of a user
    path('api/get_post/<str:id>',views.get_post,name='post'), #returns a particular post with <id>
    
]