from django.shortcuts import render
from django.views.generic import TemplateView
import folium

from calculations.iss.iss_params import ISS
from calculations.iss.people_on_board import PeopleISS


def home_view(request):
    return render(request, "iss_app/index.html", {})


def map_view(request):
    iss = ISS()
    data = iss.iss_data()

    coordinates = (data['lat'], data['lon'])

    m = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=3)

    iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
    folium.Marker(coordinates, tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(m)

    folium.CircleMarker(location=(data['lat'], data['lon']), radius=30, fill_color='blue').add_to(m)

    context = {'map': m._repr_html_()}

    return render(request, 'iss_app/map.html', context)
