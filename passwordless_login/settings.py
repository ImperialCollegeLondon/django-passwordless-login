import datetime
from django.conf import settings

# Add sesame backend and middleware to project settings
settings.AUTHENTICATION_BACKENDS = getattr(settings, "AUTHENTICATION_BACKENDS", []) + [
    "sesame.backends.ModelBackend"
]
settings.MIDDLEWARE = getattr(settings, "MIDDLEWARE", []) + [
    "sesame.middleware.AuthenticationMiddleware",
]

# Forward on defaults for sesame config. Can be overriden in project by appending LOGIN_
settings.SESAME_MAX_AGE = getattr(
    settings, "LOGIN_MAX_AGE", datetime.timedelta(minutes=30)
)
settings.SESAME_ONE_TIME = getattr(settings, "LOGIN_ONE_TIME", True)

settings.CONTACT_EMAIL = getattr(settings, "LOGIN_CONTACT_EMAIL", "")
settings.DEFAULT_FROM_EMAIL = getattr(
    settings, "LOGIN_DEFAULT_FROM_EMAIL", ""
)
settings.EMAIL_CONTENT = getattr(
    settings,
    "LOGIN_EMAIL_CONTENT",
    """Hi,

You recently requested access to {app_name}. The following link will
automatically log you in. It is valid for the next {minutes} minutes and can only be
used once:

{link}

If you did not request access or have any difficulty logging in then please contact
{email}.

Best wishes,

The Human-centred, Automation, Robotics and Monitoring in Surgery (HARMS lab) team""",
)
