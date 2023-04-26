import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
import folium
from folium import plugins
from django.contrib.auth.decorators import login_required

from calculations.iss import iss_params, people_on_board
from .forms import LocationForm
from .models import Location
from geopy.geocoders import Nominatim
from geopy import distance


def home_view(request):
    return render(request, "iss_app/index.html")


@login_required(login_url="/auth/login/")
def map_view(request):
    data = iss_params.iss_data()
    lat = float(data['lat'])
    lon = float(data['lon'])
    print(lat, lon)

    table_data = {
        'lat': round(data['lat'], 2),
        'lon': round(data['lon'], 2),
        'alt': round(data['alt'], 2),
        'vel_kph': data['vel_kph'],
        'vel_mps': data['vel_mps'],
        'pob': people_on_board.people_iss()['people'],
        'day_night': data['day_night'],
    }

    current_user = request.user.id
    user_lat = None
    user_lon = None

    try:
        location_query = Location.objects.get(user_id=current_user)
        city = location_query.city
        country = location_query.country

        geolocator = Nominatim(user_agent='ISS_Now')
        g_loc = geolocator.geocode(city + ',' + country)
        user_lat, user_lon = (g_loc.latitude, g_loc.longitude)

    except Exception as ex:
        print(ex)

    m = folium.Map(location=[lat, lon], zoom_start=4)

    iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
    folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(m)

    if user_lat and user_lon:

        dist_km = round((distance.great_circle((lat, lon), (user_lat, user_lon)).km), 2)
        print(dist_km)

        folium.Marker((user_lat, user_lon), tooltip='Your Location').add_to(m)

        folium.PolyLine(locations=[[lat, lon], [user_lat, user_lon]],
                        color='gray',
                        dash_array='5, 10',
                        weight=3,
                        tooltip=f"{dist_km} km").add_to(m)

        table_data['dist'] = dist_km

    else:
        print('No Marker')

    plugins.Terminator().add_to(m)

    context = {
        'map': m._repr_html_(),
        'data': table_data
    }

    return render(request, 'iss_app/map.html', context)


class SetLocationView(CreateView):
    form_class = LocationForm
    model = Location
    template_name = 'iss_app/location_set.html'
    success_url = reverse_lazy('map')


class ChangeLocationView(UpdateView):
    model = Location
    fields = ('city', 'country')
    template_name = 'iss_app/change_location.html'
    success_url = reverse_lazy('map')

