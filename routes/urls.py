from django.urls import path
from . import views

urlpatterns = [
    path('map_view/', views.map_view, name='map_view'),
    path('map_creation/', views.map_creation, name='map_creation'),
    path('get_route/<str:latitude_user>/<str:longitude_user>/<str:destino>', views.get_route, name='get_route')
]