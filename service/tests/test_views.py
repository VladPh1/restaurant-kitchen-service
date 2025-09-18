import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import response
from django.test import TestCase, Client
from django.urls import reverse

from service.models import DishType, Dish, Cook

DISH_TYPE_URL = reverse("service:dish-type-list")
DISH_URL = reverse("service:dish-list")


class PublicDishType(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishType(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type(self):
        DishType.objects.create(name="Desserts")
        DishType.objects.create(name="Pizza")
        res = self.client.get(DISH_TYPE_URL)
        self.assertEqual(res.status_code, 200)
        dish_type = DishType.objects.all()
        self.assertEqual(
            list(res.context["dish_type_list"]),
            list(dish_type),
        )
        self.assertTemplateUsed(res, "service/dish_type_list.html")


class PublicDish(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDish(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish(self):
        self.dish_type = DishType.objects.create(
            name="Pizza",
        )
        Dish.objects.create(
            name="Napoleon",
            price=10.2,
            dish_type=self.dish_type,
        )
        Dish.objects.create(
            name="Varenyky",
            price=100,
            dish_type=self.dish_type,
        )
        res = self.client.get(DISH_URL)
        self.assertEqual(res.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(res.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(res, "service/dish_list.html")


class SearchResultsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

        self.name1 = DishType.objects.create(
            name="Pizza",
        )
        self.name2 = DishType.objects.create(
            name="Desserts",
        )

        self.cook1 = get_user_model().objects.create(
            username="user1",
        )
        self.cook2 = get_user_model().objects.create(
            username="user2",
        )

        self.dish1 = Dish.objects.create(
            name="Napoleon",
            dish_type=self.name1,
            description="Classic Ukrainian food",
            price=10.2,
        )
        self.dish2 = Dish.objects.create(
            name="Karbonara",
            dish_type=self.name2,
            description="Classic Italian pasta",
            price=100,
        )
        self.dish1.cooks.add(self.cook1)
        self.dish2.cooks.add(self.cook2)

    def test_search_dish(self):
        res = self.client.get(
            reverse("service:dish-list"), {"name": "Napoleon"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.dish1.name)
        self.assertNotContains(res, self.dish2.name)

    def test_search_dish_type(self):
        res = self.client.get(
            reverse("service:dish-type-list"), {"name": "Pizza"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.name1.name)
        self.assertNotContains(res, self.name2.name)

    def test_search_cooks(self):
        res = self.client.get(
            reverse("service:cook-list"), {"username": "user1"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.cook1.username)
        self.assertNotContains(res, self.cook2.username)


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 3,

        }
        self.client.post(reverse("service:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, "Test first")
        self.assertEqual(new_user.last_name, "Test last")
        self.assertEqual(new_user.years_of_experience, 3)
