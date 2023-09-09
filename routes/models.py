from django.db import models
import random
import string


class PointLocation(models.Model):
    latitude  = models.FloatField(
        name="latitude", 
        max_length=100
    )
    longitude = models.FloatField(
        name="longitude", 
        max_length=100,
    )
    type = models.CharField(
        choices=[
            ('route', 'Route'),
            ('area', 'Area'),
            ('point', 'Point')
        ],
        default='point',
        max_length=20
    )
    cartesian_latitude = models.FloatField(
        name="cartesian_latitude", 
        max_length=100,
        default=-1.0,
        blank=True
    )
    cartesian_longitude = models.FloatField(
        name="cartesian_longitude", 
        max_length=100,
        default=-1.0,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        # Convert geolocation to Cartesians locations TODO
        self.cartesian_latitude = -1.0 
        self.cartesian_longitude = -1.0
        
        super(PointLocation, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"({self.latitude}, {self.longitude})"


    
class RouteLocation(models.Model):
    initial_point = models.ForeignKey(
        PointLocation, 
        related_name='route_locations_as_initial_point',
        on_delete=models.CASCADE
    )
    final_point = models.ForeignKey(
        PointLocation, 
        related_name='route_locations_as_final_point',
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"<{self.initial_point}, {self.final_point}>"
    
class SpaceRoute(models.Model):
    name = models.CharField(
        name="name",
        max_length=25,
        default=None
    )
    space_area = models.ManyToManyField(
        PointLocation
    )
    routes = models.ManyToManyField(
        RouteLocation,
        related_name='space_routes_as_route_locations',
    )
    def __str__(self):
        return self.name

