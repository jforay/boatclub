from django.shortcuts import render,get_object_or_404
from .models import Boat,Marina
from .forms import AddBoatForm, AddMarinaForm
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,TemplateView
from reservations.models import Reservation
from django.utils import timezone
from django.http import JsonResponse
import json
from collections import defaultdict
# Create your views here.

def reservations(request):
    marinas = Marina.objects.all()
    marinas_by_state = Marina.objects.order_by('state','name')
    grouped_marinas = defaultdict(list)
    for marina in marinas:
        grouped_marinas[marina.state].append(marina)
    print(grouped_marinas)
    return render(request, 'boats_and_locations/locations.html', {'marinas':marinas, 'user':request.user,'grouped_marinas':dict(grouped_marinas)})

def fleet_view(request):
    boats = Boat.objects.all()
    boat_types = boats.values_list('boat_type', flat=True).distinct()

    return render(request, 'boats_and_locations/fleet.html', {'boats': boats, 'boat_types':boat_types})

def boat_detail_view(request, boat_id):
    boat = get_object_or_404(Boat, pk = boat_id)
    reservations = Reservation.objects.filter(date__gte=timezone.now(), boat=boat)
    
    
    availability = {}
    for reservation in reservations:
        if reservation.date not in availability:
            availability[reservation.date] = {'Morning': False, 'Afternoon': False, 'All Day': False}
        
        # Mark the time slot as booked
        if reservation.time_slot == 'Morning':
            availability[reservation.date]['Morning'] = True
        elif reservation.time_slot == 'Afternoon':
            availability[reservation.date]['Afternoon'] = True
        elif reservation.time_slot == 'All Day':
            availability[reservation.date]['All Day'] = True
    # Debug print to check the availability dictionary
    print("Availability Dictionary:", availability)

    # Build the calendar events
    calendar_events = []
    for date, slots in availability.items():
        # Debug print to check slot values before conditions
        print(f"Date: {date}, Slots: {slots}")
        
        if slots['All Day'] or (slots['Morning'] and slots['Afternoon']):
            text = 'Fully Booked'
            print(f"{date} - Condition: Fully Booked")
        elif slots['Morning'] and not slots['Afternoon']:
            text = 'AM Booked'
            print(f"{date} - Condition: Available in Afternoon")
        elif slots['Afternoon'] and not slots['Morning']:
            text = 'PM Booked'
            print(f"{date} - Condition: Available in Morning")
        else:
            text = 'All Day'
            print(f"{date} - Condition: Available All Day")

        # Append each date as an event with its text
        calendar_events.append({
            'date': str(date),  # Convert date to string for JSON compatibility
            'text': text
        }) 


    return render(request, 'boats_and_locations/boat_detail.html', {
        'boat':boat,
        'calendar_events_json':json.dumps(calendar_events)
        })

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
    marinas = Marina.objects.all()
    marinas_by_state = Marina.objects.order_by('state','name')
    grouped_marinas = defaultdict(list)
    for marina in marinas:
        grouped_marinas[marina.state].append(marina)
    print(grouped_marinas)
    return render(request, 'boats_and_locations/locations.html', {'marinas':marinas, 'user':request.user,'grouped_marinas':dict(grouped_marinas)})

def marina_detail_view(request, marina_id):
    marina = get_object_or_404(Marina, pk = marina_id)
    return render(request, 'boats_and_locations/location_detail.html',{'marina':marina})


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