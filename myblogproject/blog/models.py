from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(default=timezone.now) 
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # likes = models.ManyToManyField(User, related_name='comment_likes')
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

# class Like(models.Model):
#     post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
