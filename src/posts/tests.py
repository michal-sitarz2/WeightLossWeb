from django.test import TestCase
from .models import Post
from django.test import Client
from account.models import Account
from django.db.utils import IntegrityError

import time


class PostsModelTest(TestCase):
    # Testing that a valid post can be saved
    def test_saving_valid(self):
        # Creating an account
        account = Account(username='username1', email='user1@gmail.com')
        account.set_password('password1')
        account.save()

        # Testing that the user does not have any posts
        posts = Post.objects.filter(user=account)
        self.assertEqual(len(posts), 0)

        # Making a post with valid inputs
        post = Post(user=account, title="Blog Test", content="Content of the Blog")
        # Saving the post
        post.save()

        # Testing that the user got his first post
        posts = Post.objects.filter(user=account)
        self.assertEqual(len(posts), 1)

        post.delete()
        account.delete()

    # Testing that the post requires a user to save a blog post
    def test_saving_no_user(self):
        # Making a post with valid inputs
        post = Post(title="Blog Test", content="Content of the Blog")
        # Expecting an Integrity Error as the user is required
        with self.assertRaises(IntegrityError) as context:
            post.save()

    def test_user_having_many_posts(self):
        # Creating an account
        account = Account(username='username1', email='user1@gmail.com')
        account.set_password('password1')
        account.save()

        # Testing that the user does not have any posts
        posts = Post.objects.filter(user=account)
        self.assertEqual(len(posts), 0)

        # Making a post with valid inputs
        post = Post(user=account, title="Blog Test", content="Content of the Blog")
        # Saving the post
        post.save()

        # Making a second post with valid inputs
        post2 = Post(user=account, title="Blog Test 2", content="Content of the Blog 2")
        # Saving the post
        post2.save()

        # Testing that the user got his two posts
        posts = Post.objects.filter(user=account)
        self.assertEqual(len(posts), 2)

        post.delete()
        post2.delete()
        account.delete()

    # Testing a helper function which either returns user's username, or if the anonimity is set to true
    # Just "Anonymous"
    def test_anonimity(self):
        # Creating an account
        account = Account(username='username1', email='user1@gmail.com')
        account.set_password('password1')
        account.save()

        # Making a post with valid inputs
        post = Post(user=account, title="Blog Test", content="Content of the Blog", anonimity=True)
        # Testing anonymity being set to true
        self.assertEqual(post.getAnonymousUser(), "Anonymous")
        # Making a post with valid inputs
        post = Post(user=account, title="Blog Test", content="Content of the Blog", anonimity=False)
        # Testing anonymity being set to true
        self.assertEqual(post.getAnonymousUser(), account.username)

        account.delete()
