from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from service.forms import DishForm, DishSearchForm, DishTypesSearchForm, CookSearchForm, CookCreationForm, \
    CookYearOfExperienceUpdateForm
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

class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 5
    template_name = "service/dish_type_list.html"
    context_object_name = "dish_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypesSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("service:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("service:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("service:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    name = Dish
    paginate_by = 5
    template_name = "service/dish_list.html"
    context_object_name = "dish_list"
    queryset = Dish.objects.select_related("dish_type").order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DishSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            model_name = form.cleaned_data.get("name")
            if model_name:
                queryset = queryset.filter(name__icontains=model_name)

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("service:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("service:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("service:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5
    template_name = "service/cook_list.html"
    context_object_name = "cook_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["username"]
            if name:
                queryset = queryset.filter(username__icontains=name)
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookYearOfExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookYearOfExperienceUpdateForm
    success_url = reverse_lazy("service:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("")

@login_required
def toggle_assign_to_dish(request, pk):
    cook = get_object_or_404(Cook, id=request.user.id)
    dish = get_object_or_404(Dish, id=pk)

    if cook.dishes.filter(id=dish.id).exists():
        cook.dishes.remove(dish)
    else:
        cook.dishes.add(dish)
    return redirect(reverse_lazy("service:dish-detail", kwargs={"pk": pk}))