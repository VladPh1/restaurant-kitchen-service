from django.test import TestCase

from service.forms import CookCreationForm


class FormTests(TestCase):
    def test_driver_creation_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": "3",

        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
