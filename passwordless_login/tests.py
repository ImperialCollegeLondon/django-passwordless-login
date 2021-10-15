import re
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase


@patch("django.conf.settings.CREATE_NEW_USERS", True)
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
        with patch("django.conf.settings.CREATE_NEW_USERS", False):
            response = self.client.post("/login/", {"next": "", "email": self.email})
            with self.assertRaises(get_user_model().DoesNotExist):
                get_user_model().objects.get(username=self.email)
            self.assertIn(
                f"There is no active user associated with {self.email}",
                response.context["error"],
            )

        response = self.client.post("/login/", {"next": "", "email": self.email})
        self.assertIsNotNone(get_user_model().objects.get(username=self.email))
        self.assertIn(
            f"Your login link has been sent to {self.email}",
            response.context["content"],
        )

    def test_post_duplicate_email(self):
        """An email associated with multiple users should not be possible."""
        get_user_model().objects.create_user(self.email, email=self.email)
        get_user_model().objects.create_user("foobar", email=self.email)
        with patch("django.conf.settings.CREATE_NEW_USERS", False):
            response = self.client.post("/login/", {"next": "", "email": self.email})
            self.assertIn(
                f"There are multiple users associated with {self.email}",
                response.context["error"],
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
        user_count = get_user_model().objects.count()
        self.client.post("/login/", {"next": "", "email": self.email})
        self.client.post("/login/", {"next": "", "email": self.email.capitalize()})
        self.assertEqual(get_user_model().objects.count(), user_count + 1)
