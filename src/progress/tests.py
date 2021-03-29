from django.test import TestCase
from django.db.utils import IntegrityError
import unittest
from .models import Progress
from account.models import Account
from pages.scripts.bmi_calculate import calculate_BMI


class ProgressTestCase(unittest.TestCase):
    ## Add the progress and user creation in there
    def setUp(self):
        pass

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
