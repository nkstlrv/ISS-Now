from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import folium

from calculations.iss import iss_params, people_on_board


def home_view(request):
    return render(request, "iss_app/index.html", {})


@require_GET
def map_view(request):
    if 'refresh' in request.GET:

        data = iss_params.iss_data()
        lat = float(data['lat'])
        lon = float(data['lon'])

        updating_map = folium.Map(location=[lat, lon], zoom_start=3)

        iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
        folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
            updating_map)
        # folium.CircleMarker(location=(data['lat'], data['lon']), radius=30, fill_color='gray').add_to(updating_map)

        context = {
            'map': updating_map._repr_html_(),
        }

        return JsonResponse(context)

    else:

        data = iss_params.iss_data()
        lat = float(data['lat'])
        lon = float(data['lon'])

        initial_map = folium.Map(location=[lat, lon], zoom_start=3)

        iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
        folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
            initial_map)
        # folium.CircleMarker(location=(data['lat'], data['lon']), radius=30, fill_color='gray').add_to(initial_map)

        context = {
            'map': initial_map._repr_html_()
        }

        return render(request, 'iss_app/map.html', context)
