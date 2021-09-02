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
1. Write a login template and specify the path in settings, ie:
```
LOGIN_TEMPLATE_PATH = "app_name/login.html"
```
1. Include `"passwordless_login/login.html"` in the template where users will login:
```
{% include "passwordless_login/login.html" %}
```
1. Include functionality of the login view directly `from passwordless_login.views import login`, or include the urls from this app into your app's `urlpatterns`:
```
include("passwordless_login.urls")
```


Customisable Settings include:
 - `LOGIN_MAX_AGE` - A `datetime.timedelta` of the duration the login link will last (default 30 minutes)
 - `LOGIN_ONE_TIME` - If the login link can be used one time only (default `True`)
 - `LOGIN_CREATE_NEW_USERS` - Boolean for whether or not this login form should create new users or just log in existing ones.
 - `LOGIN_EMAIL_CONTENT` - The content of the email, should include dynamic/format references to `link` (required), `minutes` (equivalent to `LOGIN_MAX_AGE`), `app_name`, and `contact_email`.
 - `APP_NAME` - used in the default email content
 - `LOGIN_CONTACT_EMAIL` - used in the default email content
 - `DEFAULT_FROM_EMAIL` - used in the default email content

For development servers, change the `EMAIL_BACKEND` setting to allow emails to be printed to the console:
```
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```
