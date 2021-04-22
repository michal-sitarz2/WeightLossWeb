from django.test import TestCase
from django.db.utils import IntegrityError
import unittest
from .models import Progress
from .forms import InitialProgressForm
from account.models import Account
from pages.scripts.bmi_calculate import calculate_BMI
from django.test import Client


class ProgressTestCase(unittest.TestCase):
    # Progress requires intial_current_set() to be called so that the BMI is calculated
    # (progress cannot be saved without BMI)
    def test_invalid_progress(self):
        user = Account.objects.create(username='user1', password='user123', email='user123@gmail.com')

        progress = Progress(starting_height=1.85,
                            starting_weight=100,
                            user=user,
                            target_bmi=20)

        # Checking for IntegrityError when saving as the BMI is not calculated
        with self.assertRaises(IntegrityError) as context:
            progress.save()
        user.delete()

    # Testing that progress cannot be saved without a user
    def test_invalid_progress_user(self):
        progress = Progress(starting_height=1.85,
                            starting_weight=100,
                            target_bmi=20)

        # Checking for IntegrityError when saving as the BMI is not calculated
        with self.assertRaises(IntegrityError) as context:
            progress.save()

    # Testing invalid inputs for starting_weight
    def test_invalid_progress_weight(self):
        user = Account.objects.create(username='user154', password='user154', email='user154@gmail.com')

        progress = Progress(starting_height=1.85,
                            user=user,
                            target_bmi=20)

        # Weight has to be defined, otherwise bmi can't be set
        with self.assertRaises(ValueError) as context:
            progress.initial_current_set()

        progress.starting_weight = 1000

        # Weight has to be defined in kilograms, hence there is an upper bound so that users don't enter value
        # that is too high
        with self.assertRaises(IntegrityError) as context:
            progress.save()

        progress.starting_weight = -1

        # Weight has to be positive
        with self.assertRaises(IntegrityError) as context:
            progress.save()

        user.delete()


    # Testing if target bmi is valid
    def test_invalid_progress_target_bmi(self):
        user = Account.objects.create(username='user1512', password='user1512', email='user1512@gmail.com')

        progress = Progress(starting_weight=100,
                            starting_height=1.85,
                            user=user)

        progress.initial_current_set()
        # BMI has to be defined
        with self.assertRaises(IntegrityError) as context:
            progress.save()

        user.delete()

    # Testing invalid inputs for starting_height
    def test_invalid_progress_height(self):
        user = Account.objects.create(username='user151', password='user151', email='user151@gmail.com')

        progress = Progress(starting_weight=100,
                            user=user,
                            target_bmi=20)

        # Height has to be defined, otherwise bmi can't be set
        with self.assertRaises(ValueError) as context:
            progress.initial_current_set()

        progress.starting_height = 185

        # Height has to be defined in meters, hence there is an upper bound so that users don't enter
        # centimeters by accident
        with self.assertRaises(IntegrityError) as context:
            progress.save()

        progress.starting_height = -1

        # Height has to be positive
        with self.assertRaises(IntegrityError) as context:
            progress.save()

        user.delete()

    def test_valid_progress_creation(self):
        user = Account.objects.create(username='user2', password='user123', email='user1234pyt@gmail.com')

        progress = Progress(starting_height=1.85,
                            starting_weight=100,
                            user=user,
                            target_bmi=20)

        progress.initial_current_set()
        self.assertEqual(progress.starting_weight, progress.current_weight)
        self.assertEqual(progress.starting_height, progress.current_height)

        self.assertEqual(progress.current_bmi,
                         calculate_BMI(progress.current_weight, progress.current_height))

        user.delete()

    def test_progress_update(self):
        user = Account.objects.create(username='user3', password='user1234', email='user12345@gmail.com')
        progress = Progress(starting_height=1.85,
                            starting_weight=100,
                            user=user,
                            target_bmi=20)
        progress.initial_current_set()

        height = 1.87
        weight = 95

        old_date_updated = progress.last_updated

        progress.update_current_set(weight, height)

        new_date_updated = progress.last_updated

        self.assertFalse(old_date_updated, new_date_updated)

        user.delete()

    # Testing one to one relationship, i.e. whether a user can have more than one progress
    def test_same_users_invalid(self):
        user = Account.objects.create(username='user4', password='user1234', email='usermail@gmail.com')
        progress = Progress(starting_height=1.85,
                            starting_weight=100,
                            user=user,
                            target_bmi=20)
        progress.initial_current_set()
        progress.save()

        progress2 = Progress(starting_height=1.85, starting_weight=100, user=user, target_bmi=20)
        progress2.initial_current_set()

        # There cannot be two progresses with the same user
        with self.assertRaises(IntegrityError) as context:
            progress2.save()

        user.delete()

class ProgressFormTests(unittest.TestCase):

    def test_blank_inputs(self):
        #form = InitialProgressForm(data={'starting_height': 1.85, 'target_bmi':20})

        form = InitialProgressForm(data={})

        self.assertEqual(
            form.errors['starting_weight'], ['This field is required.']
        )
        self.assertEqual(
            form.errors['starting_height'], ['This field is required.']
        )
        self.assertEqual(
            form.errors['target_bmi'], ['This field is required.']
        )

    def test_too_small_values(self):
        form = InitialProgressForm(data={'starting_weight': -1, 'starting_height': -1, 'target_bmi': 5})

        self.assertEqual(
            form.errors['starting_weight'], ['Ensure this value is greater than or equal to 0.']
        )
        self.assertEqual(
            form.errors['starting_height'], ['Ensure this value is greater than or equal to 0.']
        )

        self.assertEqual(
            form.errors['target_bmi'], ['Ensure this value is greater than or equal to 10.']
        )

    def test_too_high_values(self):
        form = InitialProgressForm(data={'starting_weight': 500, 'starting_height': 5, 'target_bmi': 60})

        self.assertEqual(
            form.errors['starting_weight'], ['Ensure this value is less than or equal to 400.']
        )
        self.assertEqual(
            form.errors['starting_height'], ['Ensure this value is less than or equal to 3.']
        )

        self.assertEqual(
            form.errors['target_bmi'], ['Ensure this value is less than or equal to 50.']
        )


    def test_valid_with_helper_text(self):
        form = InitialProgressForm(data={'starting_weight': 100, 'starting_height': 1.85, 'target_bmi': 20})

        self.assertTrue(form.is_valid())

        self.assertEqual(
            form['starting_weight'].help_text, "(Kg)"
        )
        self.assertEqual(
            form['starting_height'].help_text, "(meters)"
        )


    def test_valid_form_redirect(self):
        client = Client()

        form_data = {
                    'username': 'guest12345',
                    'password1': 'userpassword12345',
                    'password2': 'userpassword12345',
                    'email': 'guest12345@gmail.com',
                }

        response = client.post('/register/', form_data, follow=True)

        form_data = {
            'starting_weight': 100,
            'starting_height': 1.85,
            'target_bmi': 20
        }

        response = client.post('/registration_progress/', form_data, follow=True)

        account = Account.objects.get(username='guest12345')

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/account/dashboard/{}'.format(account.pk))

        self.assertEqual(account.progress.starting_height, 1.85)

        account.delete()


    def test_valid_form_redirect_not_logged_in(self):
        client = Client()

        form_data = {
            'starting_weight': 100,
            'starting_height': 1.85,
            'target_bmi': 20
        }

        response = client.post('/registration_progress/', form_data, follow=True)


        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login/')


    def test_dashboard_progress_edit_form(self):
        client = Client()

        # Making and saving an account
        account = Account(username='username1', email='user1@gmail.com')
        account.set_password('password1')
        account.save()

        progress = Progress(starting_height=1.85, starting_weight=100, user=account, target_bmi=20)
        progress.initial_current_set()
        progress.save()

        # Logging the user through the view
        response = client.post('/login/', {'username': 'username1', 'password': 'password1'}, follow=True)

        # Going to the account dashboard
        request = client.get('/account/dashboard/{}'.format(response.context['user'].pk), follow=True)

        # Checking the progress width variable sent to the template from the view
        self.assertEqual(request.context['progress_width'], 0)
        # Checking the progress percentage variable sent to the template from the view
        self.assertEqual(request.context['progress_percentage'], 100)

        self.assertEqual(request.context['user'].progress.starting_height, 1.85)
        self.assertEqual(request.context['user'].progress.current_height, 1.85)
        self.assertEqual(request.context['user'].progress.starting_weight, 100)
        self.assertEqual(request.context['user'].progress.current_weight, 100)


        data_input = {
            'current_weight': 90,
            'current_height': 1.85,
        }

        request = client.post('/progress/edit/{}'.format(account.pk), data_input, follow=True)

        self.assertEqual(request.redirect_chain[0][0], '/account/dashboard/{}'.format(account.id))
        self.assertEqual(request.redirect_chain[0][1], 302)


        # Checking the progress width variable sent to the template from the view
        self.assertEqual(request.context['progress_width'], 31)
        # Checking the progress percentage variable sent to the template from the view
        self.assertEqual(request.context['progress_percentage'], 68)

        self.assertEqual(request.context['user'].progress.starting_height, 1.85)
        self.assertEqual(request.context['user'].progress.current_height, 1.85)
        self.assertEqual(request.context['user'].progress.starting_weight, 100)
        self.assertEqual(request.context['user'].progress.current_weight, 90)


        account.delete()


    def test_edit_form_invalid(self):
        client = Client()

        # Making and saving an account
        account = Account(username='username1', email='user1@gmail.com')
        account.set_password('password1')
        account.save()

        progress = Progress(starting_height=1.85, starting_weight=100, user=account, target_bmi=20)
        progress.initial_current_set()
        progress.save()

        # Logging the user through the view
        response = client.post('/login/', {'username': 'username1', 'password': 'password1'}, follow=True)

        data_input = {
            'current_weight': -1,
            'current_height': 1.85,
        }

        request = client.post('/progress/edit/{}'.format(account.pk), data_input, follow=True)

        # Checking that there was no redirecting, hence it means that the form was not valid
        self.assertEqual(len(request.redirect_chain), 0)

        account.delete()
