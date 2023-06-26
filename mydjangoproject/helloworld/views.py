from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import CityForm
from django.contrib import messages
import structlog
import traceback

logger = structlog.get_logger(__name__)

# https://docs.djangoproject.com/en/4.2/topics/db/queries/


# def index(request: HttpRequest) -> HttpResponse:
#     return HttpResponse("Hello, world. You're at the polls index.")

def hello(request):
    logger.info("Hit hello world")
    return HttpResponse("Hello, World!")

def index(request):
    all_cities = City.objects.all()
    context = {
        "all_cities": all_cities
    }
    logger.info("At the index")
    return render(request, "index.html", context)

def add_city(request):
    if request.method == "POST":
        city_form = CityForm(request.POST)
        if city_form.is_valid():
            city_form.save()
            messages.success(request, ('Your city was successfully added!'))
            logger.info("Your city was successfully added!")
            return redirect('index')
        else:
            messages.error(request, 'Error saving form')
            logger.error('An error occurred', error=str(messages.error), traceback=traceback.format_exc())
    else:
        city_form = CityForm()

    return render(request, 'add_city.html', {'city_form': city_form})


def hello_city(request, city_name):
    city = get_object_or_404(City, city=city_name)
    logger.info("'Hello from a city!")
    return render(request, 'hello_city.html', {'city': city})

def delete_city(request, city_name=None):
    if request.method == 'POST':
        try:
            city_name = request.POST['city_name']
            city = City.objects.get(city=city_name)
            city.delete()
            return redirect('index')
        except City.DoesNotExist:
            logging.warning("text")
            logger.error('City does not exist', error=str(City.DoesNotExist), traceback=traceback.format_exc())
            return redirect('index')  # Or show an error message
        
    else:
        return render(request, 'delete_city.html')

