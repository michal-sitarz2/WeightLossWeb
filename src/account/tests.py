from django.test import TestCase
from django.db.utils import IntegrityError

from django.test import Client

from django.contrib.auth import logout

import unittest
from django.test import RequestFactory
from .models import Account
from .forms import RegistrationForm, AccountAuthenticationForm
from .views import dashboard_view
from progress.models import Progress

# Account Model Unit Tests
class AccountModelTest(unittest.TestCase):
    # Setting up two accounts
    def setUp(self):
        Account.objects.create(username="guest1", email="guest1@gmail.com", password="user512")
        Account.objects.create(username="guest2", email="guest2@gmail.com", password="user513")

    # Tearing down the accounts
    def tearDown(self):
        a1 = Account.objects.get(username="guest1")
        a2 = Account.objects.get(username="guest2")
        a1.delete()
        a2.delete()

    # Checking if valid accounts can be saved
    def test_valid_accounts(self):
        a1 = Account.objects.get(username="guest1")
        a2 = Account.objects.get(username="guest2")
        self.assertEqual(a1.email, 'guest1@gmail.com')
        self.assertEqual(a2.email, 'guest2@gmail.com')

    # Checking if a user can be created if one already exists
    def test_invalid_duplicate_accounts(self):
        with self.assertRaises(IntegrityError) as context:
            Account.objects.create(username="guest2", email="guest2@gmail.com", password="user513")


# Account Registration Form Unit Tests
class AccountFormTest(unittest.TestCase):
    # Testing if the username is blank
    def test_username_not_blank(self):
        form = RegistrationForm(data={'username': ''})

        self.assertEqual(
            form.errors['username'], ['This field is required.']
        )

    # Checking if the username has at least 5 characters
    def test_username_too_short(self):
        form = RegistrationForm(data={'username': 'user'})

        self.assertEqual(
            form.errors['username'], ['Ensure this value has at least 5 characters (it has 4).']
        )

    # Testing whether there is a duplicate account
    def test_account_exists(self):
        a1 = Account.objects.get_or_create(username='guest12364', password='userspass2', email='guest12364@gmail.com')
        form = RegistrationForm(data={'username': 'guest12364'})

        self.assertEqual(
            form.errors['username'], ['Account with this Username already exists.']
        )

        form2 = RegistrationForm(data={'email': 'guest12364@gmail.com'})
        self.assertEqual(
            form2.errors['email'], ['Account with this Email already exists.']
        )

        Account.objects.get(username='guest12364').delete()


    # Testing if password is not too common
    def test_password_too_common(self):
        form = RegistrationForm(data={'password': 'password', 'password2': 'password'})

        self.assertEqual(
            form.errors['password2'], ['This password is too common.']
        )

    # Testing if valid email address was provided
    def test_email_not_valid(self):
        form = RegistrationForm(data={'email':'email'})

        self.assertEqual(
            form.errors['email'], ['Enter a valid email address.']
        )

    # Testing that the user cannot be saved if the password do not match
    def test_passwords_dont_match(self):
        form_data = {
            'username': 'guest123',
            'password1': 'userpassword123',
            'password2': 'userpassword125',
            'email': 'guest123@gmail.com',
        }

        form = RegistrationForm(data=form_data)

        self.assertEqual(
            form.errors['password2'], ['The two password fields didn’t match.']
        )

    # Test if password too similar to the username
    def test_too_similar(self):
        form_data = {
            'username': 'guest123',
            'password1': 'guest123',
            'password2': 'guest123',
            'email': 'guest123@gmail.com',
        }

        form = RegistrationForm(data=form_data)

        self.assertEqual(
            form.errors['password2'], ['The password is too similar to the username.']
        )

    # Test if valid account is saved
    def test_account_creation(self):
        form_data = {
            'username': 'guest12345',
            'password1': 'userpassword12345',
            'password2': 'userpassword12345',
            'email': 'guest12345@gmail.com',
        }
        form = RegistrationForm(data=form_data)

        self.assertTrue(form.is_valid())

# Testing whether Account and Progress models work well to display dashboard for the user
class AccountDashboardViewTest(unittest.TestCase):
    # Setting up the user and allowing them to make requests with request factory
    def setUp(self):
        self.client = Client()

        self.request_factory = RequestFactory()
        self.account = Account(username='guest123', email='guest123@gmail.com')
        self.account.set_password('userpassword123')
        self.account.save()

    # Destroying the saved user
    def tearDown(self):
        self.account.delete()


    def create_progress(self):
        # Creating a progress for the user so that they can access the dashboard
        self.progress = Progress(user=self.account,
                            starting_height=1.85,
                            starting_weight=100,
                            target_bmi=20)

        self.progress.initial_current_set()
        self.progress.save()

    # Checking whether exception is thrown when user tries to access the dashboard without progress form filled
    def test_accessing_dashboard_view_without_progress(self):
        # Making a request for the dashboard, with the primary key of the current user
        request = self.request_factory.get('account/dashboard', pk=self.account.pk)
        # Setting the current user
        request.user = self.account

        # Trying to call the dashboard view, however expecting Exception as progress is required first
        try:
            response = dashboard_view(request, self.account.pk)
            self.assertTrue(False)
        except Progress.DoesNotExist:
            self.assertTrue(True)

    # Checking whether user can access dashboard with progress
    def test_accessing_dashboard_view(self):
        # Calling method which will create valid progress for the user
        self.create_progress()

        # Making request to get the dashboard for the user who already has progress
        request = self.request_factory.get('account/dashboard', pk=self.account.pk)
        request.user = self.account

        # Not expecting an exception in this case
        try:
            response = dashboard_view(request, self.account.pk)
            self.assertEqual(response.status_code, 200)
        except Progress.DoesNotExist:
            self.assertTrue(False)

        # Deleting the progress for the user
        self.progress.delete()


    # Verifying content of the dashboard, this includes checking account as well as the progress, working together,
    # to display everything necessary on the dashboard page
    def test_starting_dashboard_context(self):
        # Calling method which will create valid progress for the user
        self.create_progress()

        # Logging the client out of the page
        self.client.logout()

        # Logging the user through the view
        response = self.client.post('/login/', {'username': 'guest123', 'password': 'userpassword123'}, follow=True)

        # Going to the account dashboard
        request = self.client.get('/account/dashboard/{}'.format(response.context['user'].pk), follow=True)

        # Checking the progress width variable sent to the template from the view
        self.assertEqual(request.context['progress_width'], 0)
        # Checking the progress percentage variable sent to the template from the view
        self.assertEqual(request.context['progress_percentage'], 100)

        self.assertEqual(request.context['user'].progress.starting_height, 1.85)
        self.assertEqual(request.context['user'].progress.current_height, 1.85)
        self.assertEqual(request.context['user'].progress.starting_weight, 100)
        self.assertEqual(request.context['user'].progress.current_weight, 100)

        # Deleting the progress for the user
        self.progress.delete()

# Account Login Form Tests
class AccountLoginTest(unittest.TestCase):

    # Setting up required components for user to be able to log in
    def setUp(self):
        # Defining a django client to be able to test on it
        self.client = Client()

        # Creating an account so that user can log in
        self.a1 = Account(
            username='userusername1',
            email='userusername1@gmail.com'
        )
        # Setting password for the account
        self.a1.set_password('passwordSecret')
        # Saving the user into the database
        self.a1.save()
        # Creating progress for the user
        self.create_progress()

    # Deleting the user from the database after tests are over
    def tearDown(self):
        a1 = Account.objects.get(username='userusername1')
        a1.delete()

    # Creating a progress, because a progress is required for a user
    def create_progress(self):
        # Creating a progress for the user so that they can access the dashboard
        self.progress = Progress(user=self.a1,
                            starting_height=1.85,
                            starting_weight=100,
                            target_bmi=20)

        self.progress.initial_current_set()
        self.progress.save()

    # Testing whether a user can be logged in and logged out with views
    def test_valid_login(self):
        # Logging the client out
        self.client.logout()

        # Calling the login view, and passing valid parameters for the user
        response = self.client.post('/login/', {'username': 'userusername1', 'password': 'passwordSecret'}, follow=True)
        # Confirming that the user was logged into the website
        self.assertTrue(response.context['user'].is_authenticated)

        # Logging the user out if the view
        response = self.client.get('/logout/', follow=True)
        # Checking whether the user was successfully logged out of the website
        self.assertFalse(response.context['user'].is_authenticated)

    # Checking whether invalid data will log user in or not
    def test_invalid_login(self):
        # Logging the client out
        self.client.logout()

        # Calling the login view with invalid parameters
        response = self.client.post('/login/', {'username': 'userusername123', 'password': 'passwordSecret'},
                                    follow=True)

        # Confirming that the user was not logged into the website
        self.assertFalse(response.context['user'].is_authenticated)