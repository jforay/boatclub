from django.db import models
from django.db.models import Count
from django.utils.text import slugify

# Create your models here.
class Marina(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    lake = models.TextField(default='Unkown',null=True,blank=True)
    image = models.ImageField(
        upload_to='marinas/',
        blank=True,
        null=True
    )
    state = models.TextField(max_length=100, default='Unknown',null=True,blank=True)
    video_url = models.URLField(blank=True,null=True)
    checkfront_url = models.URLField(blank=True,null=True)
    slug = models.SlugField(unique=True,blank=True,null=True)

    def boats_by_type(self):
            """Returns [{'boat_type': 'Pontoon', 'count': 3}, ...] for this marina."""
            return (self.boats
                    .values('boat_type')
                    .annotate(count=Count('id'))
                    .order_by('boat_type'))

    def total_boats(self):
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
    marinas = models.ManyToManyField(
        Marina,
        related_name="boats",
        blank=True,
    )

    slug = models.SlugField(unique=True,blank=True,null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 2
            # ensure uniqueness in case two boats have same/similar names
            while Boat.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"