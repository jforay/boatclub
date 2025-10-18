from django.db import models
# Create your models here.
class Marina(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    lake = models.TextField(default='Unkown')
    image = models.ImageField(default= '..static/images/dbc-logo-small.png')
    state = models.TextField(max_length=100, default='Unknown')
    video_url = models.URLField(blank=True,null=True)
    
    def available_boats_count(self):
        return self.boats.filter(available_to_customers=True).count()

    def marina_boats_count(self):
        return self.boats.count()
    
    def __str__(self):
        return self.name
    

class Boat(models.Model):
    name = models.CharField(max_length=100)
    boat_type = models.CharField(max_length=50)
    length = models.CharField(max_length=2)
    passengers = models.CharField(max_length=2)
    max_hp = models.CharField(max_length=4)
    description = models.TextField()
    main_image = models.ImageField(default='..static/images/dbc-logo-small.png')
    images = models.ImageField(default='..static/images/')

    def __str__(self):
        return f"{self.name}"