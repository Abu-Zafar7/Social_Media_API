from rest_framework import serializers
from .models import *

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user','post']      
   

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['username','title','description','likes_count','comments']   

    def get_likes_count(self,obj):
        return obj.likes.count()         

    def get_username(self,obj):
        return obj.user.username
        


class PostCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True) 
    class Meta:
        model = Post
        fields = ['id','title','description','created_at']        
    def create(self, validated_data):
        
        user = self.context['request'].user
        post = Post.objects.create(user=user, **validated_data)
        return post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','comment','user','post']    


class AdminPostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'user_id']        


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)        