from sso.models import Account
from django.contrib.auth.models import User


def get_user_account(user: User) -> Account:
    return user.userprofile.account
