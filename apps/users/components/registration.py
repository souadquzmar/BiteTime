from apps.users.models import User, Role
from apps.users.models.profile import Profile


def register_customer(*, username, email, password, bio="", avatar=None):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=Role.CUSTOMER,
    )

    Profile.objects.create(
        user=user,
        bio=bio,
        avatar=avatar,
    )

    return user
