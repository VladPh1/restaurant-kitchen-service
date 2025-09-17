from django.contrib.auth import get_user_model
from django.test import TestCase

from service.models import Dish, DishType, Ingredient


class ModelTest(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test dish type ",
        )

        expected = f"{dish_type.name}"
        self.assertEqual(str(dish_type), expected)

    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="Alex",
            last_name="White",
        )
        expected = (f"{cook.username} "
                    f"({cook.first_name} "
                    f"{cook.last_name})")
        self.assertEqual(str(cook), expected)

    def test_dish_str(self):
        dish_type = DishType.objects.create(
            name="test dish type ",

        )
        dish = Dish.objects.create(
            name="test",
            dish_type=dish_type,
            price=100,
        )
        expected = f"{dish.name} (price: {dish.price} , dish type: {dish.dish_type.name})"
        self.assertEqual(str(dish), expected)

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(
            name="test ingredient ",

        )
        expected = f"{ingredient.name}"
        self.assertEqual(str(ingredient), expected)
