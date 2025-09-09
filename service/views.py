from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from service.models import DishType, Cook, Dish


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_dishes = Dish.objects.count()
    num_cookers = Cook.objects.count()
    num_dish_types = DishType.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_dishes": num_dishes,
        "num_cookers": num_cookers,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1
    }
    return render(request, "service/index.html", context=context)
