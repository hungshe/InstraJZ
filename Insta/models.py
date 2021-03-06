from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from imagekit.models import ProcessedImageField
# Create your models here.
# Define User Customized  User model
class InstaUser(AbstractUser):
        profile_pic  =  ProcessedImageField(
                upload_to='static/images/profiles',
                format='JPEG',
                options={'quality':100},
                blank=True,
                null=True
                )

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Post(models.Model):
        author  =  models.ForeignKey(
               InstaUser,
               on_delete = models.CASCADE,
               related_name='my_posts' 
        )
        title  =  models.TextField(blank=True, null=True)
        image  =  ProcessedImageField(
                upload_to='static/images/posts',
                format='JPEG',
                options={'quality':100},
                blank=True,
                null=True
                )

        def get_like_count(self): 
                return self.likes.count()
                      
        def get_absolute_url(self):
                return  reverse("post_detail", args=[str(self.id)])

#  user name like post x
# when post x is deleted, like also removed
class Like(models.Model):
        post   =  models.ForeignKey(
                Post,
                on_delete=models.CASCADE,
                related_name='likes')
        user  = models.ForeignKey(
                InstaUser,
                on_delete=models.CASCADE,
                related_name='likes')
        class Meta:
                unique_together  =  ("post", "user")
        
        def __str__(self):
                        return 'Like: ' + self.user.username  +  '  likes  '  + self.post.title