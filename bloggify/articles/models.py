from django.db import models
from accounts.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Commented by: " + self.user.first_name