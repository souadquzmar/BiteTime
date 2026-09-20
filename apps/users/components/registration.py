from apps.users.models import User, Role


def register_customer(*, username, email, password):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=Role.CUSTOMER,
    )

    return user
