from django.db import models
from django.db.models import Count
from django.utils.text import slugify

POSITION_CHOICES = [
    ('top', 'Top'),
    ('middle', 'Middle'),
    ('bottom', 'Bottom'),
]

class Marina(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    lake = models.TextField(default='Unknown', null=True, blank=True)
    hero_image = models.ImageField(
        upload_to='marinas/',
        blank=True,
        null=True
    )
    carousel_image = models.ImageField(
        upload_to='marina_carousel/',
        blank=True,
        null=True
    )
    state = models.TextField(max_length=100, default='Unknown', null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)
    checkfront_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    display_states = models.CharField(max_length=200, blank=True, default='')
    # Lake / location write-up
    description = models.TextField(blank=True, null=True)

    # Optional restaurant section
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)
    restaurant_description = models.TextField(blank=True, null=True)
    restaurant_image = models.ImageField(
        upload_to='marina_restaurants/',
        blank=True,
        null=True
    )
    # Optional feature section (e.g. Vol Navy)
    feature_title = models.CharField(max_length=255, blank=True, null=True)
    feature_description = models.TextField(blank=True, null=True)
    feature_image = models.ImageField(
        upload_to='marina_features/',
        blank=True,
        null=True
    )


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


class MarinaPhoto(models.Model):
    marina = models.ForeignKey(
        Marina,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(upload_to='marina_photos/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.marina.name} — photo {self.order}"


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
    slug = models.SlugField(unique=True, blank=True, null=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='middle')
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 2
            while Boat.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"