from django.urls import path

from service.views import (
    index, DishTypeListView, DishListView, CookListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("cook/", CookListView.as_view(), name="cook-list"),
]

app_name = "service"
