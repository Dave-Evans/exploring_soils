from django.test import TestCase
from django.urls import reverse

from wisccc.models import SurveyFarm
from django.contrib.auth.models import User


class SurveyHomeViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(
            username="testuser1", email="testuser1@email.com", password="1X<ISRUkw+tuK"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", email="testuser2@email.com", password="2HJ1vRV0Z&3iD"
        )
        test_user1.save()
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("wisc_cc_survey"))
        self.assertRedirects(response, "/login/?next=/wisc-cc-survey")

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("wisc_cc_survey"))

        # Check our user is logged in
        self.assertEqual(str(response.context["user"]), "testuser1")
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, "wisccc/wisc_cc_survey.html")
