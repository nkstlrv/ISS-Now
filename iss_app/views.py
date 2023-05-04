import folium
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from folium import plugins
from geopy.geocoders import Nominatim

from calculations import distance_geocoder
from calculations.iss import iss_params, people_on_board
from .forms import LocationForm, NotifyForm
from .models import Location, Notify


def start_view(request):
    return render(request, "iss_app/index.html")


def data_view(request):
    iss_data = iss_params.iss_data()

    lat = round(iss_data['lat'], 3)
    lon = round(iss_data['lon'], 3)

    if lat < 0:
        lat = f"{lat}° S"
    else:
        lat = f"{lat}° N"

    if lon < 0:
        lon = f"{lon}° W"
    else:
        lon = f"{lon}° E"

    vel_kps = round((iss_data['vel_mps'] / 1000), 2)
    return JsonResponse({'lat': lat,
                         'lon': lon,
                         'alt': round(iss_data['alt'], 1),
                         'vel_kph': iss_data['vel_kph'],
                         'vel_mps': iss_data['vel_mps'],
                         'vel_kps': vel_kps,
                         'pob': people_on_board.people_iss()['people'],
                         'day_night': iss_data['day_night'],
                         })


@login_required(login_url="start/")
def map_view(request):
    iss_data = iss_params.iss_data()

    lat = round(iss_data['lat'], 3)
    lon = round(iss_data['lon'], 3)

    if lat < 0:
        lat = f"{lat}° S"
    else:
        lat = f"{lat}° N"

    if lon < 0:
        lon = f"{lon}° W"
    else:
        lon = f"{lon}° E"

    table_data = {
        'lat': lat,
        'lon': lon,
        'alt': round(iss_data['alt'], 2),
        'vel_kph': iss_data['vel_kph'],
        'vel_mps': iss_data['vel_mps'],
        'pob': people_on_board.people_iss()['people'],
        'day_night': iss_data['day_night'],
        'usr_loc': None,
        'loc_id': None,
        'notify': None
    }

    current_user = request.user.id

    user_lat = None
    user_lon = None
    iss_lat = iss_data['lat']
    iss_lon = iss_data['lon']

    try:

        notification_query = Notify.objects.get(user_id=current_user)
        table_data['notify'] = notification_query

    except Exception as e:
        print(e)

    try:

        location_query = Location.objects.get(user_id=current_user)
        table_data['loc_id'] = location_query.pk
        city = location_query.city
        country = location_query.country

        table_data['user_loc'] = True

        geolocator = Nominatim(user_agent='ISS_Now')
        g_loc = geolocator.geocode(city + ',' + country)

        if g_loc:
            user_lat, user_lon = (g_loc.latitude, g_loc.longitude)

            location_query.lat = user_lat
            location_query.lon = user_lon
            location_query.save()

        else:
            location_query.lat = user_lat
            location_query.lon = user_lon
            location_query.save()

    except Exception as ex:
        print(ex)

    m = folium.Map(location=[iss_lat, iss_lon], zoom_start=4)

    iss_icon = folium.features.CustomIcon('iss_app/static/images/space-station.png', icon_size=(40, 40))
    folium.Marker((iss_lat, iss_lon), tooltip='ISS', popup='International Space Station', icon=iss_icon).add_to(m)

    if user_lat and user_lon:

        dist_km = distance_geocoder.get_distance((iss_lat, iss_lon), (user_lat, user_lon))

        folium.Marker((user_lat, user_lon), tooltip='Your Location').add_to(m)

        folium.PolyLine(locations=[[iss_lat, iss_lon], [user_lat, user_lon]],
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


class SetLocationView(CreateView, LoginRequiredMixin):
    form_class = LocationForm
    model = Location
    template_name = 'iss_app/location_set.html'
    success_url = reverse_lazy('map')


class RemoveMarker(DeleteView, LoginRequiredMixin):
    model = Location
    template_name = 'iss_app/del-location.html'
    success_url = reverse_lazy('map')

    def delete(self, request, *args, **kwargs):
        self.model = self.get_object()

        try:
            notify_obj = Notify.objects.get(user=self.model.user_id)
            print(notify_obj)
        except Notify.DoesNotExist:
            notify_obj = None

        self.object.delete()

        if notify_obj:
            notify_obj.delete()

        return HttpResponseRedirect(self.success_url)


@login_required(login_url="/auth/login/")
def earth_cam_view(request):
    iss_data = iss_params.iss_data()

    lat = round(iss_data['lat'], 3)
    lon = round(iss_data['lon'], 3)

    if lat < 0:
        lat = f"{lat}° S"
    else:
        lat = f"{lat}° N"

    if lon < 0:
        lon = f"{lon}° W"
    else:
        lon = f"{lon}° E"

    vel_kps = round((iss_data['vel_mps'] / 1000), 2)

    return render(request, 'iss_app/earth-cam.html', {'lat': lat,
                                                      'lon': lon,
                                                      'vel_kps': vel_kps,
                                                      'alt': round(iss_data['alt'], 1)
                                                      })


@login_required(login_url="/auth/login/")
def station_cam_view(request):
    iss_data = iss_params.iss_data()

    lat = round(iss_data['lat'], 3)
    lon = round(iss_data['lon'], 3)

    if lat < 0:
        lat = f"{lat}° S"
    else:
        lat = f"{lat}° N"

    if lon < 0:
        lon = f"{lon}° W"
    else:
        lon = f"{lon}° E"

    vel_kps = round((iss_data['vel_mps'] / 1000), 3)

    return render(request, 'iss_app/station-cam.html', {'lat': lat,
                                                        'lon': lon,
                                                        'vel': vel_kps,
                                                        'alt': round(iss_data['alt'], 3)
                                                        })


@login_required(login_url="/auth/login/")
def nasa_tv_view(request):
    iss_data = iss_params.iss_data()

    lat = round(iss_data['lat'], 3)
    lon = round(iss_data['lon'], 3)

    if lat < 0:
        lat = f"{lat}° S"
    else:
        lat = f"{lat}° N"

    if lon < 0:
        lon = f"{lon}° W"
    else:
        lon = f"{lon}° E"

    vel_kps = round((iss_data['vel_mps'] / 1000), 3)

    return render(request, 'iss_app/nasa_tv.html', {'lat': lat,
                                                    'lon': lon,
                                                    'vel': vel_kps,
                                                    'alt': round(iss_data['alt'], 3)
                                                    })


class NotifyView(CreateView, LoginRequiredMixin):
    model = Notify
    form_class = NotifyForm
    template_name = 'iss_app/notify.html'
    success_url = reverse_lazy('map')


class DelNotifyView(DeleteView, LoginRequiredMixin):
    model = Notify
    template_name = 'iss_app/del-notify.html'
    success_url = reverse_lazy('map')
