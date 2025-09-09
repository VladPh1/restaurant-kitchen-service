from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", )


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ("years_of_experience", )

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    ingredient = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    def __str__(self):
        return f"{self.name} (price: {self.price} , dish type: {self.dish_type.name})"

    # def get_absolute_url(self):
    #     return reverse("service:dish-detail", args=[str(self.id)])