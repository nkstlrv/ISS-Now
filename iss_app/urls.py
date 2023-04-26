from django.urls import path
from .views import home_view, map_view, SetLocationView, ChangeLocationView, live_cam_view
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path("", home_view, name='home'),
    path("map/", map_view, name='map'),
    path("set-location/", login_required(SetLocationView.as_view()), name='set-location'),
    path("change-location/<int:pk>/", login_required(ChangeLocationView.as_view()), name='change-location'),
    path("live-cam/", login_required(live_cam_view), name='cam'),
]