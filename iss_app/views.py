from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import folium
from folium import plugins
import requests
import geocoder
from django.contrib.auth.decorators import login_required

from calculations.iss import iss_params, people_on_board


def home_view(request):
    return render(request, "iss_app/index.html")


@login_required(login_url="/auth/login/")
def map_view(request):
    data = iss_params.iss_data()
    lat = float(data['lat'])
    lon = float(data['lon'])

    table_data = {
        'lat': round(data['lat'], 2),
        'lon': round(data['lon'], 2),
        'alt': round(data['alt'], 2),
        'vel_kph': data['vel_kph'],
        'vel_mps': data['vel_mps'],
        'pob': people_on_board.people_iss()['people']
    }

    if 'refresh' in request.GET:

        updating_map = folium.Map(location=[lat, lon], zoom_start=5)

        iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
        folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
            updating_map)

        plugins.Terminator().add_to(updating_map)

        context = {
            'map': updating_map._repr_html_(),
            'data': table_data
        }

        return JsonResponse(context)

    else:

        initial_map = folium.Map(location=[lat, lon], zoom_start=5)

        iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
        folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
            initial_map)

        plugins.Terminator().add_to(initial_map)

        context = {
            'map': initial_map._repr_html_(),
            'data': table_data
        }

        return render(request, 'iss_app/map.html', context)


def map_google(request):
    return render(request, 'iss_app/map_google.html')
