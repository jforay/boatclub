from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, ListView
from boats_and_locations.models import Boat, Marina
from .forms import ReservationForm
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib import messages

class ReserveBoatView(LoginRequiredMixin, View):
    template_name = 'reservations/reserve_boat.html'

    def get(self,request, *args, **kwargs):
        boat = get_object_or_404(Boat, id=self.kwargs['boat_id'])
        date = self.kwargs['date']
        time_slot = self.request.GET.get('time_slot')
        user = self.request.user
        form = ReservationForm(
            boat=boat,
            date = date ,
            time_slot = time_slot,
            user = user,
        )
        return render(request, self.template_name, {'form':form, 'date':date, 'time_slot':time_slot})
    
    def post(self,request, *args, **kwargs):
        
        boat = get_object_or_404(Boat, id = self.kwargs['boat_id'])
        date = self.kwargs['date']
        time_slot=self.request.GET.get('time_slot')
        user = self.request.user
        form = ReservationForm(request.POST, boat=boat, date = date, time_slot=time_slot, user = user)
        #check if reserved

        if Reservation.objects.filter(boat=boat, date=date, time_slot=time_slot, confirmed=True).exists():
            messages.error(self.request, "This boat is already reserved for the selected date and time slot")
            return redirect(reverse('reservations_for_day',args=[boat.marina.id,date]))
        if time_slot == 'All Day':
            reservation_cost = 2
        else:
            reservation_cost = 1
        if not user.is_boss():
            current_reservations = Reservation.objects.filter(user=user, date__gte=timezone.now(), confirmed = True)
            reservation_count = sum(2 if res.time_slot == 'All Day' else 1 for res in current_reservations)
            if boat.marina != user.home_marina:
                messages.error(self.request, "If you would like to book a boat at a different marina, please reach out to Dave or Dean to see if this is possible.")
                return redirect(reverse('user_profile', args=[user.id]))
            if reservation_count + reservation_cost > 4:
                messages.error(self.request, "This reservation will put you over the reservation limit. Please review your current reservations.")
                return redirect(reverse('user_profile',args=[user.id]))

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.boat = boat
            reservation.date = date
            reservation.time_slot = time_slot
            reservation.user = user
            reservation.save()
            return redirect(reverse('user_profile', args=[user.id]))
        return render(request,self.template_name, {'form':form})






class AllReservationsView(LoginRequiredMixin, TemplateView):
    template_name = 'reservations/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reservations = Reservation.objects.all().order_by('boat__marina')
        context['reservations'] = reservations
        return context

class DailyReservationsView(LoginRequiredMixin,TemplateView):
    template_name = 'reservations/reservations_for_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_str = self.kwargs['date']
        marina_id = self.kwargs['marina_id']
        marina = Marina.objects.get(id=marina_id)
        date = parse_date(date_str)
        if date is None:
            return context
        
        morning_reservations = Reservation.objects.filter(date=date,time_slot='Morning')
        afternoon_reservations = Reservation.objects.filter(date=date,time_slot='Afternoon')
        all_day_reservations = Reservation.objects.filter(date=date, time_slot='All Day')

        morning_boats = morning_reservations.values_list('boat_id', flat=True)
        afternoon_boats = afternoon_reservations.values_list('boat_id',flat=True)
        all_day_boats = all_day_reservations.values_list('boat_id',flat=True)

        available_morning_boats = Boat.objects.exclude(id__in=morning_boats).exclude(id__in=all_day_boats)
        available_afternoon_boats = Boat.objects.exclude(id__in=afternoon_boats).exclude(id__in=all_day_boats)
        available_all_day_boats = available_morning_boats.intersection(available_afternoon_boats)


        context['available_all_day_boats'] = available_all_day_boats
        context['afternoon_reservations'] = afternoon_reservations
        context['morning_reservations'] = morning_reservations
        context['available_morning_boats'] = available_morning_boats
        context['available_afternoon_boats'] = available_afternoon_boats
        context['all_day_reservations'] = all_day_reservations
        context['date'] = date
        context['marina'] = marina

        return context
class DailyScheduleView(LoginRequiredMixin,TemplateView):
    template_name = 'reservations/schedule_for_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        marina_id = self.kwargs['marina_id']

        date = self.kwargs['date']
        marina = get_object_or_404(Marina,id=marina_id)
        reservations = Reservation.objects.filter(boat__marina=marina,date=date,confirmed=True).order_by('exact_time')
        #make LINK TO reservation, and only shows confirmed reservations

        context['reservations'] = reservations
        context['marina'] = marina
        
        return context
class UserReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/user_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):

        return Reservation.objects.filter(user=self.request.user, date__gte=timezone.now(),confirmed=True).order_by('date')
    

def reservation_detail_view(request,reservation_id):
    reservation = get_object_or_404(Reservation,pk=reservation_id)
    user = request.user
    return render(request,'reservations/reservation_detail.html', {'user':user,'reservation':reservation})

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation,pk=reservation_id)
    reservation.confirmed = False
    #reservation.cancel()
    reservation.save()
    user_id = request.user.id
    return redirect(reverse('user_profile', args=[user_id]))

def reservations_for_day(request,date):
    morning_reservations = Reservation.objects.filter(date=date,time_slot='Morning')
    afternoon_reservations = Reservation.objects.filter(date=date,time_slot='Afternoon')
    all_day_reservations = Reservation.objects.filter(date=date, time_slot='All Day')

    morning_boats = morning_reservations.values_list('boat_id', flat=True)
    afternoon_boats = afternoon_reservations.values_list('boat_id',flat=True)
    all_day_boats = all_day_reservations.values_list('boat_id',flat=True)

    available_morning_boats = Boat.objects.exclude(id__in=morning_boats).exclude(id__in=all_day_boats)
    available_afternoon_boats = Boat.objects.exclude(id__in=afternoon_boats).exclude(id__in=all_day_boats)
    available_all_day_boats = available_morning_boats.intersection(available_afternoon_boats)


    
def marinas_for_schedule_view(request):
    print("marinas view called")
    marinas = Marina.objects.all()
    return render(request,'reservations/marinas_for_schedule.html',{'marinas':marinas})

def marina_schedule_view(request,marina_id):
    marina = get_object_or_404(Marina,id=marina_id)

    return render(request,'reservations/schedule_calendar.html',{'marina':marina})

def reservation_calendar_view(request, marina_id):
    marina = get_object_or_404(Marina, id=marina_id)
    return render(request, 'reservations/reservations_calendar.html', {'marina': marina})

def schedule_or_reservations_view(request, marina_id):
    marina = get_object_or_404(Marina,id=marina_id)
    return render(request,'reservations/schedule_or_reservations.html',{'marina':marina})