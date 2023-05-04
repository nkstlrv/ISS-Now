from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import start_view, map_view, SetLocationView, ChangeLocationView, earth_cam_view, data_view, \
    station_cam_view, nasa_tv_view, NotifyView, DelNotifyView

urlpatterns = [

    path("", map_view, name='map'),
    path("start/", start_view, name='start'),
    path("set-location/", SetLocationView.as_view(), name='set-location'),
    path("change-location/<int:pk>/", ChangeLocationView.as_view(), name='change-location'),
    path("earth-cam/", earth_cam_view, name='earth-view'),
    path("station-cam/", station_cam_view, name='station-view'),
    path("nasa-tv/", nasa_tv_view, name='nasa-tv'),
    path("data-view/", data_view, name='data-view'),
    path("notify/", NotifyView.as_view(), name='notify'),
    path("notify/turn-off/<int:pk>", DelNotifyView.as_view(), name='del-notify'),
]
