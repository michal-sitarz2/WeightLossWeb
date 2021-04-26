from django.db import models

from posts.models import Post
from account.models import Account

class Comment(models.Model):
    # A Post can have many comments
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # User who commented
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # Content of the blog post
    comment = models.TextField()
    # Date when the post was created
    date = models.DateTimeField(auto_now_add=True)
