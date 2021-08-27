import sys

import django
from django.test.runner import DiscoverRunner
from django.conf import settings


def run_tests(*test_args):
    if not test_args:
        test_args = ["passwordless_login.tests"]

    runner = DiscoverRunner(verbosity=1)
    failures = runner.run_tests(test_args)
    if failures:
        sys.exit(failures)


def setup_django():
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="passwordless_login.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "passwordless_login",
        ],
        SECRET_KEY="123",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ]
                },
            }
        ],
    )
    django.setup()


if __name__ == "__main__":
    setup_django()
    run_tests(*sys.argv[1:])
