from django.db import models
# Create your models here.
class Marina(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    lake = models.TextField(default='Unkown')
    image = models.ImageField(default= '..static/images/dbc-logo-small.png')
    state = models.TextField(max_length=100, default='Unknown')

    def available_boats_count(self):
        return self.boats.filter(available_to_customers=True).count()

    def marina_boats_count(self):
        return self.boats.count()
    
    def __str__(self):
        return self.name
    

class Boat(models.Model):
    name = models.CharField(max_length=100)
    boat_type = models.CharField(max_length=50)
    description = models.TextField()
    marina = models.ForeignKey(Marina, on_delete=models.CASCADE, related_name='boats')
    open = models.BooleanField(default=True)
    available_to_customers = models.BooleanField(default=True)
    issues = models.TextField() # ex. depth finder not working
    rules = models.TextField()  #ex. no pets allowed
    image = models.ImageField(default='..static/images/dbc-logo-small.png')

    def __str__(self):
        return f"{self.name} ({self.marina.name})"
    
    def is_open(self):
        
        return self.open
    
    def booked(self,date,time_slot):
        self.open = False
        self.available_to_customers = False
        self.save()

    def reset_availability(self):
        self.open = True
        self.available_to_customers = True
        self.save()
