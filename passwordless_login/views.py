from datetime import timedelta
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

import sesame.utils
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .settings import settings


def login(request):
    if not request.method == "POST":
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(
                request,
                settings.TEMPLATE_PATH,
                {"next": request.GET.get("next", "")},
            )

    email = request.POST["email"]
    try:
        validate_email(email)
    except ValidationError:
        return render(
            request,
            settings.TEMPLATE_PATH,
            {"error": f"'{email}' is not a valid email", "next": request.POST["next"]},
        )
    if settings.CREATE_NEW_USERS:
        user, _ = get_user_model().objects.get_or_create(
            username=email.lower(), email=email.lower()
        )
    else:
        try:
            user = get_user_model().objects.get(email=email.lower())
        except get_user_model().DoesNotExist:
            return render(
                request,
                settings.TEMPLATE_PATH,
                {
                    "error": f"There is no active user associated with {email}",
                    "next": request.POST["next"],
                },
            )
        except get_user_model().MultipleObjectsReturned:
            return render(
                request,
                settings.TEMPLATE_PATH,
                {
                    "error": (
                        f"There are multiple users associated with {email}. Please "
                        "contact {settings.CONTACT_EMAIL} to access your account."
                    ),
                    "next": request.POST["next"],
                },
            )
    if not user.is_active:
        return render(
            request,
            settings.TEMPLATE_PATH,
            {"error": "Account disabled", "next": request.POST["next"]},
        )

    next_url = urlsplit(request.build_absolute_uri(request.POST["next"]))
    query_parameters = parse_qs(next_url.query)
    query_parameters.update(sesame.utils.get_parameters(user))
    link = urlunsplit(next_url._replace(query=urlencode(query_parameters)))

    send_mail(
        f"{settings.APP_NAME} login",
        settings.EMAIL_CONTENT.format(
            link=link,
            minutes=int(settings.SESAME_MAX_AGE / timedelta(minutes=1)),
            app_name=settings.APP_NAME,
            contact_email=settings.CONTACT_EMAIL,
        ),
        None,
        [email],
    )
    message = (
        f"Your login link has been sent to {email}. It may take a few minutes to "
        "arrive. Please check your spam folder."
    )
    return render(request, settings.TEMPLATE_PATH, {"content": message})
