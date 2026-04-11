from django.shortcuts import render,get_object_or_404
from .models import Boat,Marina
from .forms import AddBoatForm, AddMarinaForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.http import JsonResponse
import json
import os
from collections import defaultdict
from django.conf import settings
# Create your views here.

def marina_flyer_view(request,slug):
    marina = get_object_or_404(Marina,slug=slug)
    boats = marina.boats.all()[:6]

    return render(request , 'boats_and_locations/marina_flyer2.html', {'marina':marina,'boats':boats})

def reservations_view(request):
    marinas = Marina.objects.all()
    reservations = Marina.objects.filter(checkfront_url__isnull=False).exclude(checkfront_url__exact='None').order_by('state','lake','name')
    grouped_marinas = defaultdict(lambda: defaultdict(list))
    for marina in reservations:
        states = [marina.state]
        if marina.display_states:
            states += [s.strip() for s in marina.display_states.split(',')]
        for state in states:
            grouped_marinas[state][marina.lake].append(marina)

   
    grouped_marinas = {
        state: dict(sorted(lakes.items(), key=lambda x: len(x[1]), reverse=True))
        for state, lakes in sorted(grouped_marinas.items())
    }
    
    grouped_marinas = dict(
        sorted(
            grouped_marinas.items(),
            key=lambda item: sum(len(m) for m in item[1].values()),
            reverse=True
        )
    )

    nc = dict(sorted(grouped_marinas.pop("North Carolina", {}).items(), key=lambda x: len(x[1]), reverse=True))
    sc = dict(sorted(grouped_marinas.pop("South Carolina", {}).items(), key=lambda x: len(x[1]), reverse=True))

    return render(request, 'boats_and_locations/reservations.html', {
        'marinas': marinas,
        'user': request.user,
        'grouped_marinas': grouped_marinas,
        'nc': nc,
        'sc': sc,
    })

def fleet_view(request):
    from itertools import chain
    top = Boat.objects.filter(position='top').order_by('name')
    middle = Boat.objects.filter(position='middle').order_by('name')
    bottom = Boat.objects.filter(position='bottom').order_by('name')
    boats = list(chain(top, middle, bottom))
    boat_types = Boat.objects.all().values_list('boat_type', flat=True).distinct()
    marinas = Marina.objects.filter(boats__isnull=False).distinct().order_by("name")
    
    return render(request, 'boats_and_locations/fleet.html', {'boats': boats, 'boat_types':boat_types,'marinas':marinas})

def boat_detail_view(request, slug):
    boat = get_object_or_404(Boat, slug = slug)
    folder_name = boat.name.replace(" ", "-")
    
    # static path (as used in templates)
    static_folder = f"boats_and_locations/images/{folder_name}/"
    
    # Get all image URLs relative to static/
    image_urls = []
    static_dir = os.path.join(settings.BASE_DIR, "boats_and_locations", "static", static_folder)
    if os.path.exists(static_dir):
        for filename in sorted(os.listdir(static_dir)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_urls.append(f"/static/{static_folder}{filename}")

    return render(request, "boats_and_locations/boat_detail.html", {"boat": boat, "image_urls": image_urls})


def locations_view(request):
    COMING_SOON_STATE = "Coming Soon!"
    active_marinas = Marina.objects.exclude(state=COMING_SOON_STATE)
    coming_soon = Marina.objects.filter(state=COMING_SOON_STATE)
    grouped_marinas = defaultdict(lambda: defaultdict(list))
    for marina in active_marinas:
        states = [marina.state]
        if marina.display_states:
            states += [s.strip() for s in marina.display_states.split(',')]
        for state in states:
            grouped_marinas[state][marina.lake].append(marina)
    
    grouped_marinas = {
        state: dict(sorted(lakes.items()))
        for state, lakes in sorted(grouped_marinas.items())
    }
    grouped_marinas = dict(
        sorted(
            grouped_marinas.items(),
            key=lambda item: sum(len(m) for m in item[1].values()),
            reverse=True
        )
    )

    nc = grouped_marinas.pop("North Carolina", {})
    sc = grouped_marinas.pop("South Carolina", {})

    return render(request, 'boats_and_locations/locations.html', {
        'marinas': active_marinas,
        'coming_soon': coming_soon,
        'user': request.user,
        'grouped_marinas': grouped_marinas,  # everything except NC and SC
        'nc': nc,
        'sc': sc,
    })

def marina_detail_view(request, slug):
    marina = get_object_or_404(Marina, slug = slug)
    return render(request, 'boats_and_locations/marina_flyer2.html',{'marina':marina})


class AddBoatView(CreateView):
    model = Boat
    form_class = AddBoatForm
    template_name = 'boats_and_locations/add_boat.html'
    success_url = reverse_lazy('boats')

    def form_valid(self, form):
        return super().form_valid(form)
    
class BoatEditView(UpdateView):
    model = Boat
    fields = ['name', 'description', 'issues', 'marina','boat_type','image']  # Add any fields you want to allow for editing
    template_name = 'boats_and_locations/edit_boat.html'
    success_url = reverse_lazy('boats')  # Redirect to users list after editing


class AddMarinaView(CreateView):
    model = Marina
    form_class = AddMarinaForm
    template_name = 'boats_and_locations/add_marina.html'
    success_url = reverse_lazy('locations')

    def form_valid(self, form):
        return super().form_valid(form)
    
class MarinaEditView(UpdateView):
    model = Marina
    fields = ['name', 'address','state', 'lake','image']
    template_name = 'boats_and_locations/edit_marina.html'
    success_url = reverse_lazy('locations')
        
    def form_valid(self, form):
        return super().form_valid(form)
    


def filter_boats(request):
    boat_type = request.GET.get('boat_type')
    marina_id = request.GET.get('marina_id')

    boats = Boat.objects.all()
    if marina_id:
        # Boat has a ManyToMany relationship to Marina (`Boat.marinas`).
        boats = boats.filter(marinas__id=marina_id).distinct()

    if boat_type:
        boats = boats.filter(boat_type=boat_type)
    
    boats_data = []
    for boat in boats:
        boats_data.append({
            'id': boat.id,
            'slug': boat.slug,
            'name': boat.name,
            'boat_type': boat.boat_type,
            'image': request.build_absolute_uri(boat.image.url) if boat.image else None,
        })

    return JsonResponse({'boats':boats_data})

