from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField()
    estimated_prep_minutes = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
