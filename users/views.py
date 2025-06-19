from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from boats_and_locations.models import Boat,Marina
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden,HttpResponseRedirect
from .forms import AddUserForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,TemplateView,DeleteView,DetailView,UpdateView
from reservations.models import Reservation
from django.utils import timezone
from .models import CustomUser
from docusign.utils import save_completed_pdf
from reservations.utils import send_float_plan_email_with_pdf
# Create your views here.
def is_member(user):
    return user.group.filter(name='Member').exists()

def is_employee(user):
    return user.groups.filter(name__in=['Employee','Manager','Boss']).exists()

def is_manager(user):
    return user.groups.filter(name__in=['Manager','Boss']).exists()

def is_boss(user):
    return user.groups.filter(name='Boss').exists()

class AddUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AddUserForm
    template_name = 'users/add_user.html'
    success_url = reverse_lazy('marinas')

    def test_func(self):
        return self.request.user.groups.filter(name='Boss').exists()
    
    def form_valid(self, form):
        User = get_user_model()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        group = form.cleaned_data['role']
        first_name = form.cleaned_data['first_name']  # Make sure these fields are saved
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        home_marina = form.cleaned_data['home_marina']
        new_user = User.objects.create_user(
            email=email,
            password=password,
            group_name=group.name,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            home_marina=home_marina
            )
        return HttpResponseRedirect(reverse('marinas'))
    
class MarinaView(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    template_name = 'users/marinas.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Boss').exists()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        marinas = Marina.objects.all()
        boss_group = Group.objects.get(name='Boss')
        boss_users = User.objects.filter(groups=boss_group)

        context['marinas'] = marinas
        context['boss_users'] = boss_users
        return context

class UsersInMarinaView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/marina_users.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Boss')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        marina = get_object_or_404(Marina, pk=self.kwargs['marina_id'])
        User = get_user_model()
        
        groups = Group.objects.exclude(name='Boss')
        users_in_groups = {}
        for group in groups:
            users_in_groups[group.name] = User.objects.filter(home_marina = marina, groups= group)

        context['request'] = self.request
        context['users_in_groups'] = users_in_groups
        context['marina'] = marina
        return context

    

class UsersListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Boss').exists()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        marinas = Marina.objects.all()
        groups = Group.objects.exclude(name='Boss')

        boss_group = Group.objects.get(name='Boss')
        boss_users = User.objects.filter(groups=boss_group)

        context['request']=self.request
        context['marina']= marinas
        context['boss_users'] = boss_users
        return context

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('marinas')

    def test_func(self):
        return self.request.user.groups.filter(name='Boss').exists()
    
    def get_object(self, queryset = None):
        return get_object_or_404(get_user_model(), id = self.kwargs['pk'])

# @login_required
# @user_passes_test(is_employee)
# def view_schedule(request):
    
    
class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'users/user_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(pk = user_id)
        # Add reservations to the context
        context['reservations'] = Reservation.objects.filter(
            user=user, 
            date__gte=timezone.now(), 
            confirmed=True
        ).order_by('date')
        context['request'] = self.request
        envelope_id = self.request.GET.get("envelope_id")  # Get envelope ID from return_url query params
        print(f"Envelope ID: {envelope_id}")
        if envelope_id:
            try:
                reservation = Reservation.objects.filter(user=user).last()
                save_completed_pdf(envelope_id=envelope_id, reservation=reservation)
                # Email PDF to the user or another recipient
                print(reservation.float_plan_pdf.path)
                send_float_plan_email_with_pdf(user, reservation.float_plan_pdf.path)

            except Exception as e:
                print(f"Error processing signed PDF: {str(e)}")

        return context


# class UserProfileView(LoginRequiredMixin, DetailView):
#     model = get_user_model()
#     template_name = 'users/user_profile.html'
#     context_object_name = 'user'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_id = self.kwargs['pk']
#         user = CustomUser.objects.get(pk = user_id)
#         # Add reservations to the context
#         context['reservations'] = Reservation.objects.filter(
#             user=user, 
#             date__gte=timezone.now(), 
#             confirmed=True
#         ).order_by('date')
#         context['request'] = self.request
#         envelope_id = self.request.GET.get("envelope_id")  # Get envelope ID from return_url query params
#         print(f"Envelope ID: {envelope_id}")
#         if envelope_id:
#             try:
#                 reservation = Reservation.objects.filter(user=user).last()
#                 save_completed_pdf(envelope_id=envelope_id, reservation=reservation)
#                 # Email PDF to the user or another recipient
#                 print(reservation.float_plan_pdf.path)
#                 #send_float_plan_email_with_pdf(user, reservation.float_plan_pdf.path)

#             except Exception as e:
#                 print(f"Error processing signed PDF: {str(e)}")

        return context

class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'home_marina','groups']  # Add any fields you want to allow for editing
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('marinas')  # Redirect to users list after editing

    def test_func(self):
        return self.request.user.groups.filter(name='Boss').exists()  # Only allow Boss to edit

