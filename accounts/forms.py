import os
import requests
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import html_safe
from django.conf import settings


@html_safe
class ScriptTag:
    def __str__(self):
        return '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'


class TurnstileField(forms.CharField):

    def __init__(self, *args, **kwargs):
        self.client_ip = kwargs.pop("client_ip")
        super().__init__(*args, **kwargs)

    def clean(self, value):
        # get the secret Turnstile key from the environment
        try:
            secret_key = settings.CLOUDFLARE_TURNSTILE_SECRET_KEY
        except KeyError:
            raise ValueError(
                "CLOUDFLARE_TURNSTILE_SECRET_KEY environment variable not set"
            )

        if value is None or value == "":

            msg = "Please check the box to complete your signup."
            raise ValidationError((msg), code="check_box")

        # send the widget response token value, secret key, and request IP to the Turnstile API
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": secret_key,
                "response": value,
                "remoteip": self.client_ip,
            },
        ).json()
        print("Response from Cloudflare:")
        print(response)
        if not response["success"]:
            raise ValidationError(
                ("Please check the box to complete the signup."),
                code=",".join(response["error-codes"]),
            )
        return value


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
