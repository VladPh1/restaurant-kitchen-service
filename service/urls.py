from django.urls import path

from service.views import (
    index,
)


urlpatterns = [
    path("", index, name="index"),
    path("dish_type/", LiteraryFormatListView.as_view(), name="dish-type-list"),
]

app_name = "service"
