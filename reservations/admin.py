from django.contrib import admin
from .models import Reservation, FloatPlan
# Register your models here.
admin.site.register(Reservation)
admin.site.register(FloatPlan)