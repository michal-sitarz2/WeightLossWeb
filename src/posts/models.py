from django.db import models
from account.models import Account

class Post(models.Model):
    # A user can have many Posts
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # Title of the post
    title = models.CharField(max_length=60, blank=False)
    # Content of the blog post
    content = models.TextField()
    # Date when the post was created
    date = models.DateTimeField(auto_now_add=True)

    ### keywords as ENUM

    def __str__(self):
        return self.user.username + " " + self.title