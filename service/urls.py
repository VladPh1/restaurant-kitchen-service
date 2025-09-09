from django.urls import path

from service.views import (
    index,
    DishTypeListView,
    DishTypeCreateView,
    DishListView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    DishDetailView,
    CookListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path(
        "dish_type/create/",
        DishTypeCreateView.as_view(),
        name="dish-type-create",
    ),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("cook/", CookListView.as_view(), name="cook-list"),
]

app_name = "service"
