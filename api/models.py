from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='user_following', blank=True)
    following = models.ManyToManyField(User, related_name='user_followers', blank=True)
    def __str__(self) -> str:
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='liked_posts',through='Like')
    comments = models.ManyToManyField(User,related_name='commented_posts',through='Comment')
    
    def __str__(self):
        return f"Post by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    post = models.ForeignKey("Post" , on_delete=models.CASCADE, null= True)  

   
    def __str__(self):
        if self.user and self.post:
          return f"{self.user.username} liked post by {self.post.user.username}"
        return "Invalid Like Entry" 

    
 
class Comment(models.Model):
    user = models.ForeignKey (User, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,null= True)
    comment = models.TextField(blank=True)
   

    def __str__(self):
        if self.user and self.post:
           return f"{self.user.username} commented on {self.post.title}"
        return "Invalid comment"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.username} follows {self.followee.username}"

        