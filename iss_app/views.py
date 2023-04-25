from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
import folium
from folium import plugins
from django.contrib.auth.decorators import login_required

from calculations.iss import iss_params, people_on_board
from .forms import LocationForm
from .models import Location


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

    m = folium.Map(location=[lat, lon], zoom_start=5)

    iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
    folium.Marker((lat, lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(
        m)

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