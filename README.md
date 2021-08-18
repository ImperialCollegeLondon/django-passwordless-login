# django-passwordless-login
Login to your Django app with a link sent by email.

### Adding it to your django project

1. Install django-passwordless-login:
```
$ pip install https://github.com/ImperialCollegeLondon/django-passwordless-login
```
1. Add `"passwordless_login.apps.PasswordlessLoginConfig"` to `INSTALLED_APPS`:
```
INSTALLED_APPS += ["passwordless_login.apps.PasswordlessLoginConfig"]
```
1. Include `"passwordless_login/login.html"` in the template where users will login:
```
{% include "passwordless_login/login.html" %}
```

Customisable Settings include:
 - `LOGIN_MAX_AGE` - A `datetime.timedelta` of the duration the login link will last (default 30 minutes)
 - `LOGIN_ONE_TIME` - If the login link can be used one time only (default `True`)
 - `LOGIN_CONTACT_EMAIL`
 - `DEFAULT_FROM_EMAIL`
 - `LOGIN_EMAIL_CONTENT`

For development servers, change the `EMAIL_BACKEND` setting to allow emails to be printed to the console:
```
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```
