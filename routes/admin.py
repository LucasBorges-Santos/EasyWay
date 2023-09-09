from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(PointLocation)
admin.site.register(RouteLocation)
admin.site.register(SpaceRoute)
