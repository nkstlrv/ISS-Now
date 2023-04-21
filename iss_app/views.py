from django.shortcuts import render
from django.views.generic import TemplateView
import folium

from calculations.iss import iss_params, people_on_board


def home_view(request):
    return render(request, "iss_app/index.html", {})


def map_view(request):
    data = iss_params.iss_data()

    coordinates = (data['lat'], data['lon'])

    m = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=3)

    # folium.TileLayer(
    #     'https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/{z}/{x}/{y}?access_token={access_token}',
    #     name='Satellite',
    #     attr='Mapbox',
    #     overlay=True,
    #     control=True,
    #     min_zoom=0,
    #     max_zoom=22).add_to(m)


    iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
    folium.Marker(coordinates, tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(m)

    folium.CircleMarker(location=(data['lat'], data['lon']), radius=30, fill_color='blue').add_to(m)

    context = {'map': m._repr_html_()}

    return render(request, 'iss_app/map.html', context)
