from django.urls import path

from service.views import (
    index,
    DishTypeListView,
    DishListView,
    CookListView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    DishDetailView,
)


urlpatterns = [
    path("", index, name="index"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("cook/", CookListView.as_view(), name="cook-list"),
]

app_name = "service"
