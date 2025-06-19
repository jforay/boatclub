from typing import Any
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reservation, FloatPlan
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import CreateView,TemplateView,View,ListView
from boats_and_locations.models import Boat
from .forms import ReservationForm, FloatPlanForm
from django.utils import timezone
from users.models import CustomUser
from boats_and_locations.models import Marina
from django.http import HttpResponseBadRequest
from django.utils.dateparse import parse_date
from django.contrib import messages
from .utils import send_reservation_email, send_float_plan_email
from django.core.files.storage import FileSystemStorage
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs
from django.http import JsonResponse

# from .forms import ReservationForm

# # Create your views here.

# @login_required
# def make_reservation(request):
#     if meth

def send_document(request):
    # Add this function in your app's views.py
    try:
        api_client = ApiClient()
        api_client.host = "https://demo.docusign.net/restapi"
        api_client.set_default_header("Authorization", f"Bearer fc263be6-5a01-46c5-b9d3-4312a0719612")

        # Load the PDF from static/pdf
        with open("static/pdf/Float_plan_fillable.pdf", "rb") as file:
            document_base64 = file.read().encode("base64").decode("utf-8")

        document = Document(
            document_base64=document_base64,
            name="Float Plan",
            file_extension="pdf",
            document_id="1",
        )

        signer = Signer(
            email="user@example.com",
            name="User Name",
            recipient_id="1",
            routing_order="1",
            client_user_id="123",
        )

        sign_here = SignHere(
            anchor_string="/signature/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0",
        )

        signer.tabs = Tabs(sign_here_tabs=[sign_here])

        envelope = EnvelopeDefinition(
            email_subject="Please sign the Float Plan",
            documents=[document],
            recipients={"signers": [signer]},
            status="sent",
        )

        envelopes_api = EnvelopesApi(api_client)
        envelope_summary = envelopes_api.create_envelope(account_id="4ce66269-9bec-4729-8aff-96d38de6c5a4", envelope_definition=envelope)

        return JsonResponse({"envelope_id": envelope_summary.envelope_id})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    


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
            request.session['reservation_id'] = reservation.id
            # send_reservation_email(
            #     user = request.user,
            #     boat=reservation.boat, 
            #     reservation_date=reservation.date,
            #     reservation_time=reservation.exact_time,
            # )
            try:
                from docusign.utils import send_docusign_envelope, generate_signing_url
                
                envelope_id = send_docusign_envelope(
                    recipient_email=user.email,
                    recipient_name=f"{user.first_name} {user.last_name}",
                )

                signing_url = generate_signing_url(envelope_id,user)

                return redirect(signing_url)
            
            except Exception as e:
                messages.error(self.request, f"Error sending the float plan for signing: {str(e)}")
                return redirect(reverse('user_profile', args=[user.id]))
        return render(request,self.template_name, {'form':form})

        
# class FloatPlanView(View):
#     template_name = 'reservations/float_plan.html'

#     def get(self, request, *args, **kwargs):
#         reservation_id = request.session.get('reservation_id')
#         reservation = get_object_or_404(Reservation, id = reservation_id)
#         date = reservation.date
#         boat = reservation.boat.name
#         if not reservation_id:
#             marina_id = self.kwargs.get('marina_id')
#             return redirect(reverse('reservations_for_day', args=[marina_id,date]))
#         form = FloatPlanForm()
#         return render(request, self.template_name, {'form':form, 'date':date, 'boat':boat})
    
#     def post(self,request, *args, **kwargs):
#         reservation_id = request.session.get('reservation_id')
#         if not reservation_id:
#             date = self.kwargs.get('date')
#             marina_id = self.kwargs.get('marina_id')
#             return redirect(reverse('reservations_for_day', args=[marina_id,date]))
        
#         reservation = get_object_or_404(Reservation, id=reservation_id)
#         form = FloatPlanForm(request.POST)

#         if form.is_valid():
#             float_plan = form.save(commit=False)
#             float_plan.reservation = reservation
#             float_plan.user = request.user
#             float_plan.boat = reservation.boat
#             float_plan.departure_time = reservation.exact_time
#             float_plan.save()
#             #send email to float plan
#             #send_float_plan_email(request.user, float_plan)
#             return redirect('user_profile', request.user.id)
        
#         return render(request, self.template_name, {'form':form})
    
    
def float_plan_view(request,reservation_id):
    pdf_path = "reservations/static/pdf/Float_plan_fillable.pdf"
    submit_url = reverse("submit_float_plan_pdf", args=[reservation_id])
    return render(request, "reservations/float_plan_pdf.html",{"pdf_url":pdf_path, "submit_url":submit_url})

def submit_float_plan_pdf(request, reservation_id):
    if request.method == "POST":
        completed_pdf = request.FILES.get("completed_pdf")
        if completed_pdf:
            fs = FileSystemStorage()
            file_name = f"reservation_{reservation_id}_float_plan.pdf"
            file_path = fs.save(file_name, completed_pdf)
            
            # Optionally link the file to the reservation (if you have a Reservation model)
            # reservation = Reservation.objects.get(id=reservation_id)
            # reservation.float_plan = file_path
            # reservation.save()
        
        # Redirect to the user profile page after submission
        return redirect("user_profile")
    return redirect("float_plan_pdf", reservation_id=reservation_id)


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