from sso.models import Account, UserProfile
from django.contrib.auth.models import User


def get_user_account(user: User) -> Account:
    return user.userprofile.account


def create_user_profile(user: User, account: Account) -> UserProfile:
    return UserProfile.objects.create(user=user, account=account)
