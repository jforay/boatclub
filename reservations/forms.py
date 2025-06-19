from django import forms
from .models import Reservation, FloatPlan

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['exact_time','notes']

    MORNING_TIMES = [
        ('08:00', '8:00 AM'),
        ('08:30', '8:30 AM'),
        ('09:00', '9:00 AM'),
    ]

    AFTERNOON_TIMES = [
        ('13:50', '1:30 PM'),
        ('14:00', '2:00 PM'),
    ]

    def __init__(self, *args, **kwargs):
        self.boat = kwargs.pop('boat')
        self.date = kwargs.pop('date')
        self.time_slot = kwargs.pop('time_slot')
        self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)

        print(f"time slot recieved: {self.time_slot}")

        self.fields['exact_time'] = forms.ChoiceField(choices=[])  # Initialize as empty choices
  

        if self.time_slot == 'Morning':
            self.fields['exact_time'].choices = self.MORNING_TIMES
        elif self.time_slot == 'Afternoon':
            self.fields['exact_time'].choices = self.AFTERNOON_TIMES
        else:
            self.fields['exact_time'].choices = self.MORNING_TIMES + self.AFTERNOON_TIMES
        
        print(f"Exact time choices: {self.fields['exact_time'].choices}")

        

    def save(self, commit=True):
        reservation = super().save(commit = False)
        reservation.boat = self.boat 
        reservation.time_slot = self.time_slot
        reservation.date = self.date
        reservation.user = self.user
        print(f"saving reservation with time slot: {self.time_slot}")
        reservation.save()
        return reservation
    

class FloatPlanForm(forms.ModelForm):
    return_time = forms.CharField(label='Estimated Return Time', required=True)
    class Meta:
        model = FloatPlan
        fields = ['return_time', 'emergency_contact_name', 'emergency_contact_phone', 'guests']