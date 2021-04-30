from django.db import models
from account.models import Account

class Post(models.Model):
    # A user can have many Posts
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # Title of the post
    title = models.CharField(max_length=60, null=False, blank=False)
    # Content of the blog post
    content = models.TextField(null=False, blank=False)
    # Date when the post was created
    date = models.DateTimeField(auto_now_add=True)
    # Whether the user wants this to be anonymous
    anonimity = models.BooleanField(default=True)


    def getAnonymousUser(self):
        if (self.anonimity):
            return "Anonymous"
        else:
            return self.user.username

    def __str__(self):
        return self.user.username + ": '" + self.title + "'"