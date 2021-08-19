import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


class PasswordlessTestCase(TestCase):
    def setUp(self):
        email = "j.smith@hotmail.com"
        self.device_id = "20146435807d3a4a81dd"
        self.user = User.objects.create_user(email, email=email)

    def test_paswordless(self):
        response = self.client.post(reverse("login"), {"email": self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_email(self):
        response = self.client.post(reverse("login"), {"email": "j.smith"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_user(self):
        response = self.client.post(reverse("login"), {"email": "unknown@mail.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        email = "j.smith2@hotmail.com"
        user = User.objects.create_user(email, email=email, is_active=False)
        response = self.client.post(reverse("login"), {"email": user.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        User.objects.create_user("jsmith", email=self.user.email)
        response = self.client.post(reverse("login"), {"email": self.user.email})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class TestLoginView(TestCase):
    email = "foo@imperial.ac.uk"

    def test_get(self):
        """Get request should have status code 200"""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_email(self):
        """Only allow valid emails"""
        email = "foo"
        response = self.client.post("/login/", {"next": "", "email": email})
        self.assertEqual(response.context["error"], f"'{email}' is not a valid email")

    def test_post(self):
        """An email associated with a user in the database should be sent when email is
        submitted"""
        response = self.client.post("/login/", {"next": "", "email": self.email})
        self.assertIsNotNone(get_user_model().objects.get(username=self.email))
        self.assertIn(
            f"Your login link has been sent to {self.email}",
            response.context["content"],
        )

    def test_post_inactive_user(self):
        """An email associated with an inactive user returns a message that the account
        is disabled"""
        get_user_model().objects.create_user(
            self.email, email=self.email, is_active=False
        )
        response = self.client.post("/login/", {"next": "", "email": self.email})
        self.assertEqual(response.context["error"], "Account disabled")

    def test_post_existing_user(self):
        """An email associated with an existing user should be allowed and work fine"""
        get_user_model().objects.create_user(self.email, email=self.email)
        response = self.client.post("/login/", {"next": "", "email": self.email})
        self.assertIsNotNone(get_user_model().objects.get(username=self.email))
        self.assertIn(
            f"Your login link has been sent to {self.email}",
            response.context["content"],
        )

    def test_post_twice(self):
        """Confirm that requesting a login token is possible for a second email"""
        response = self.client.post("/login/", {"next": "", "email": self.email})
        self.assertIn(
            f"Your login link has been sent to {self.email}",
            response.context["content"],
        )
        email2 = "bar@imperial.ac.uk"
        response = self.client.post("/login/", {"next": "", "email": email2})
        self.assertIn(
            f"Your login link has been sent to {email2}",
            response.context["content"],
        )

    def test_invalid_token_in_next(self):
        """Invalid sesame tokens passed in next parameter do not persist in login url.
        This is a regression test for a bug that led to malformed login urls
        being sent to users when they attempted to use an expired url.
        """
        self.client.post(
            "/login/",
            {"next": "/?sesame=badtoken", "email": self.email},
        )

        sesame_url = re.search(r"http\S+", mail.outbox[0].body).group(0)
        self.assertFalse("badtoken" in sesame_url)

    def test_upper_lower_case(self):
        """Same email differently capitalised should map to the same user"""
        self.client.post("/login/", {"next": "", "email": self.email})
        self.client.post("/login/", {"next": "", "email": self.email.capitalize()})
        self.assertEqual(get_user_model().objects.count(), 1)
