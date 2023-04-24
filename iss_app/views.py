from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import folium
import requests
import geocoder

from calculations.iss import iss_params, people_on_board


def home_view(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return render(request, "iss_app/index.html", {'ip': ip})


@require_GET
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
        'vis': data['vis'],
        'pob': people_on_board.people_iss()['people']
    }

    user_ip = ''

    if 'refresh' in request.GET:

        updating_map = folium.Map(location=[lat, lon], zoom_start=3)

        iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
        folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
            updating_map)
        # folium.CircleMarker(location=(data['lat'], data['lon']), radius=30, fill_color='gray').add_to(updating_map)

        context = {
            'map': updating_map._repr_html_(),
            'data': table_data
        }

        return JsonResponse(context)

    else:

        initial_map = folium.Map(location=[lat, lon], zoom_start=3)

        iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
        folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
            initial_map)
        # folium.CircleMarker(location=(data['lat'], data['lon']), radius=30, fill_color='gray').add_to(initial_map)

        context = {
            'map': initial_map._repr_html_(),
            'data': table_data
        }

        return render(request, 'iss_app/map.html', context)
