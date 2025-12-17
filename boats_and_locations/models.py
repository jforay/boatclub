from django.db import models
# Create your models here.
class Marina(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    lake = models.TextField(default='Unkown',null=True,blank=True)
    image = models.ImageField(default= '..static/images/dbc-logo-small.png',null=True,blank=True)
    state = models.TextField(max_length=100, default='Unknown',null=True,blank=True)
    video_url = models.URLField(blank=True,null=True)
    checkfront_url = models.URLField(blank=True,null=True)
    
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
    max_hp = models.CharField(max_length=10)
    description = models.TextField()
    image = models.ImageField(default='..static/images/dbc-logo-small.png')

    def __str__(self):
        return f"{self.name}"