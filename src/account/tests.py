from django.test import TestCase
from django.db.utils import IntegrityError

import unittest
from .models import Account
from .forms import RegistrationForm

class AccountModelTest(unittest.TestCase):
    def setUp(self):
        Account.objects.create(username="guest1", email="guest1@gmail.com", password="user512")
        Account.objects.create(username="guest2", email="guest2@gmail.com", password="user513")

    def tearDown(self):
        a1 = Account.objects.get(username="guest1")
        a2 = Account.objects.get(username="guest2")
        a1.delete()
        a2.delete()

    def test_valid_accounts(self):
        a1 = Account.objects.get(username="guest1")
        a2 = Account.objects.get(username="guest2")
        self.assertEqual(a1.email, 'guest1@gmail.com')
        self.assertEqual(a2.email, 'guest2@gmail.com')

    def test_invalid_duplicate_accounts(self):
        with self.assertRaises(IntegrityError) as context:
            Account.objects.create(username="guest2", email="guest2@gmail.com", password="user513")


class AccountFormTest(unittest.TestCase):

    def test_username_not_blank(self):
        form = RegistrationForm(data={'username': ''})

        self.assertEqual(
            form.errors['username'], ['This field is required.']
        )

    def test_username_too_short(self):
        form = RegistrationForm(data={'username': 'user'})

        self.assertEqual(
            form.errors['username'], ['Ensure this value has at least 5 characters (it has 4).']
        )

    def test_account_exists(self):
        a1 = Account.objects.get_or_create(username='guest123', password='userspass2', email='guest123@gmail.com')
        form = RegistrationForm(data={'username': 'guest123'})

        self.assertEqual(
            form.errors['username'], ['Account with this Username already exists.']
        )

        form2 = RegistrationForm(data={'email': 'guest123@gmail.com'})
        self.assertEqual(
            form2.errors['email'], ['Account with this Email already exists.']
        )

        Account.objects.get(username='guest123').delete()

    def test_email_not_valid(self):
        form = RegistrationForm(data={'password': 'password', 'password2': 'password'})

        self.assertEqual(
            form.errors['password2'], ['This password is too common.']
        )

    def test_password_too_short(self):
        form = RegistrationForm(data={'email':'email'})

        self.assertEqual(
            form.errors['email'], ['Enter a valid email address.']
        )

    def test_password_too_common(self):
        form = RegistrationForm(data={'password': 'password', 'password2': 'password'})

        self.assertEqual(
            form.errors['password2'], ['This password is too common.']
        )


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

    def test_account_creation(self):
        form_data = {
            'username': 'guest123',
            'password1': 'userpassword123',
            'password2': 'userpassword123',
            'email': 'guest123@gmail.com',
        }
        form = RegistrationForm(data=form_data)

        self.assertTrue(form.is_valid())
