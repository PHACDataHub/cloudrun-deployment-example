from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, World!")


# https://docs.djangoproject.com/en/4.2/topics/db/queries/
from django.shortcuts import render

from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import CityForm
from django.contrib import messages


def index(request):
    all_cities = City.objects.all()
    context = {
        "all_cities": all_cities
    }
    return render(request, "index.html", context)


def add_city(request):
    if request.method == "POST":
        city_form = CityForm(request.POST)
        if city_form.is_valid():
            city_form.save()
            messages.success(request, ('Your city was successfully added!'))
            return redirect('index')
        else:
            messages.error(request, 'Error saving form')
    else:
        city_form = CityForm()

    return render(request, 'add_city.html', {'city_form': city_form})


def hello_city(request, city_name):
    city = get_object_or_404(City, city=city_name)
    return render(request, 'hello_city.html', {'city': city})

def delete_city(request, city_name=None):
    if request.method == 'POST':
        try:
            city_name = request.POST['city_name']
            city = City.objects.get(city=city_name)
            city.delete()
            return redirect('index')
        except City.DoesNotExist:
            return redirect('index')  # Or show an error message
    else:
        return render(request, 'delete_city.html')
