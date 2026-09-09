from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    WAITER = "waiter", "Waiter"
    CHEF = "chef", "Chef"

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    def __str__(self):
        return self.username
