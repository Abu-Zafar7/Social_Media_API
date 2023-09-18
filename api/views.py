from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from rest_framework import views,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import FollowSerializer, LikeSerializer, PostSerializer, PostCreateSerializer, CommentSerializer
from .permissions import IsLikedOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

def home(request):
    return HttpResponse("<h1>Hello! Welcome to my API</h1>")



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAuthenticated,))   
def user_details(request,username):
    try:
        user = get_object_or_404(User,username = username)
    except User.DoesNotExist:
        return Response({'detail': 'User does not exist'})    

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response({'detail': 'UserProfile does not exist'}, status=status.HTTP_404_NOT_FOUND)



    user_post = Post.objects.filter(user=user_profile.user)    
    post_serializer = PostSerializer(user_post , many=True )

    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()

    user_data = {
        "username": user_profile.user.username,
        "posts": post_serializer.data,
        "followers": followers_count,
        "following": following_count,
    }
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def follow(request,id):

    try:
        followee = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status= status.HTTP_404_NOT_FOUND)    

    serializer = FollowSerializer(data={'follower': request.user.id, 'followee': id})   

    if serializer.is_valid():
        serializer.save()
        return Response({"detail": f'You are now following {followee.username}'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unfollow(request,id):
    try:
        unfollowed = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'detail':'User Not Found'}, status=status.HTTP_404_NOT_FOUND )
    
    try:
        unfollowe = Follow.objects.filter(follower = request.user.id, followee = unfollowed )
    except Follow.DoesNotExist:
        return Response({'detail' : 'You are not following this user.'}, status=status.HTTP_201_CREATED)


    unfollowe.delete()
    return Response({'detail': 'Unfollowed!'}, status= status.HTTP_200_OK)


@api_view(['POST'])    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsOwnerOrReadOnly, IsLikedOrReadOnly])
def like(request,id):

    try:
        post = Post.objects.get(id= id)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found'})    
    like_data = {'user': request.user.id, 'post': post.id}
    serializer = LikeSerializer(data=like_data)

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': f'{request.user.username} liked post by {post.user.username}'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsOwnerOrReadOnly])
def unlike_post(request,id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"detail":"Post does not exist"})    

    try:
        like = Like.objects.filter(user = request.user.id , post = post)    
    except Like.DoesNotExist:
        return Response({"detail": "you haven't liked this post"})    

    like.delete()    
    return Response({"detail":"Unliked successfully"})


@api_view(['POST'])   
@authentication_classes(JWTAuthentication)
@permission_classes([IsAuthenticated])
def post_add(request):
    title = request.data.get('title')
    description = request.data.get('description')

    
    if not title or not description:
        return Response({'detail': 'Title and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

    
    serializer = PostCreateSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes((JWTAuthentication)) 
@permission_classes([IsAuthenticated,IsOwnerOrReadOnly])
def delete_post (request , pk ):
    try:
        post = Post.objects.get(id = pk)
    except Post.DoesNotExist:
        return Response({'detail':'Post not found'})     

    post.delete()    
    return Response({'detail':'Post deleted successfully!'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request, id):
    try:
        post = Post.objects.get(id = id)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found'},status=status.HTTP_400_BAD_REQUEST)    
    
    serializer_data = {'user': request.user.id, 'post': post.id, 'comment': request.data.get('comment', '')}
    serializer = CommentSerializer(data=serializer_data) 


    if serializer.is_valid():
        serializer.save()
        comment_data = {
            'id': serializer.data['id'],
            'comment': serializer.data['comment'],
        }
        response_data = {
            'detail': f'{request.user.username} commented on {post}',
            'comment': comment_data,
        }
        return Response(response_data,status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors)    


@api_view(['GET'])    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_posts(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')

    
    post_data = []
    for post in posts:
        serializer = PostSerializer(post)
        post_data.append(serializer.data)

    return Response(post_data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def get_post(request,id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({'detail':'Post does not exist'},status=status.HTTP_400_BAD_REQUEST) 
       
    
    serializer = PostSerializer(post)    
    return Response(serializer.data,status=status.HTTP_200_OK)
      