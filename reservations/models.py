from django.db import models
from users.models import CustomUser
from boats_and_locations.models import Boat,Marina
from datetime import time
# Create your models here.

class Reservation(models.Model):
    TIME_SLOT_CHOICES = [
        ('Morning','Morning'),
        ('Afternoon','Afternoon'),
        ('All Day','All Day')
    ]
    MORNING_TIMES = [
        (time(8, 0), '8:00 AM'),
        (time(8, 30), '8:30 AM'),
        (time(9, 0), '9:00 AM'),
        (time(9, 30), '9:30 AM'),
    ]

    AFTERNOON_TIMES = [
        (time(13, 30), '1:30 PM'),
        (time(14, 0), '2:00 PM'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE,related_name='reservations')
    date = models.DateField()
    time_slot = models.CharField(max_length=200, choices=TIME_SLOT_CHOICES)
    exact_time = models.TimeField(null=True, blank=True)
    confirmed = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)
    float_plan_pdf = models.FileField(upload_to='float_plans/', null=True, blank=True)

    def cancel(self):
        self.confirmed == False
        self.save()

    def __str__(self):
        return f"{self.boat.name} Reserved by {self.user.first_name} {self.user.last_name} on {self.date} at {self.exact_time}"
        
class FloatPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='float_plan')
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)

    departure_time = models.TimeField()
    return_time = models.TimeField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    guests = models.TextField()

    def __str__(self):
        return f"Float Plan for {self.reservation.user} for {self.reservation.boat.name} on {self.reservation.date}"
    

