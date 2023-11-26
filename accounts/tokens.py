from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import *
from django.contrib.auth.models import User

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.emailconfirm.email_confirmed)
        )

account_activation_token = TokenGenerator()
