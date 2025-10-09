from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Cook, Dish, DishType, Ingredient


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_ingredients = Ingredient.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits + 1,
    }
    return render(request, "kitchen/index.html", context=context)
