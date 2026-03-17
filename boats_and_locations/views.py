from django.shortcuts import render,get_object_or_404
from .models import Boat,Marina
from .forms import AddBoatForm, AddMarinaForm
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,TemplateView
from reservations.models import Reservation
from django.utils import timezone
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
        grouped_marinas[marina.state][marina.lake].append(marina)
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

    return render(request, 'boats_and_locations/reservations.html', {
        'marinas': marinas,
        'user': request.user,
        'grouped_marinas': grouped_marinas,
        'nc': nc,
        'sc': sc,
    })

def fleet_view(request):
    boats = Boat.objects.order_by('?')
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

class BoatAvailabilityView(TemplateView):
    template_name = 'boats_and_locations/boat_availability.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        boat_id = self.kwargs['boat_id']
        date = self.kwargs['date']
        user = self.request.user

        # Query for availability based on the boat and selected date
        boat = Boat.objects.get(id=boat_id)
        marina = boat.marina
        morning_reserved = Reservation.objects.filter(boat=boat, date=date, time_slot="Morning",confirmed = True).exists()
        afternoon_reserved = Reservation.objects.filter(boat=boat, date=date, time_slot="Afternoon",confirmed = True).exists()
        all_day_reserved = Reservation.objects.filter(boat=boat, date = date, time_slot="All Day",confirmed = True).exists()
        if (morning_reserved and afternoon_reserved) or all_day_reserved:
            all_day_available = False
        else:
            all_day_available = True

        cancelled_morning = Reservation.objects.filter(
            boat=boat, date=date, time_slot="Morning", confirmed=False
        ).exists()
        cancelled_afternoon = Reservation.objects.filter(
            boat=boat, date=date, time_slot="Afternoon", confirmed=False
        ).exists()
        cancelled_all_day = Reservation.objects.filter(
            boat=boat, date=date, time_slot="All Day", confirmed=False
        ).exists()

        boss_morning_available = not morning_reserved or cancelled_morning
        boss_afternoon_available = not afternoon_reserved or cancelled_afternoon
        boss_all_day_available = (
            not morning_reserved
            and not afternoon_reserved
            and not all_day_reserved
            and cancelled_all_day
)

        # Pass the boat availability details to the context
        context['boss_all_day_available'] = boss_all_day_available
        context['boss_morning_available'] = boss_morning_available
        context['boss_afternoon_available'] = boss_afternoon_available
        context['boat'] = boat
        context['date'] = date
        context['marina'] = marina
        context['morning_available'] = not morning_reserved
        context['afternoon_available'] = not afternoon_reserved
        context['all_day_available'] = all_day_available

        return context

def locations_view(request):
    COMING_SOON_STATE = "Coming Soon!"
    active_marinas = Marina.objects.exclude(state=COMING_SOON_STATE)
    coming_soon = Marina.objects.filter(state=COMING_SOON_STATE)
    grouped_marinas = defaultdict(lambda: defaultdict(list))
    for marina in active_marinas:
        grouped_marinas[marina.state][marina.lake].append(marina)
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
            'name': boat.name,
            'boat_type': boat.boat_type,
            'image': request.build_absolute_uri(boat.image.url) if boat.image else None,
        })

    return JsonResponse({'boats':boats_data})

