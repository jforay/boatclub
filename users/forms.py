from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from boats_and_locations.models import Marina
from django.contrib.auth.forms import AuthenticationForm


class AddUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.NumberInput()
    trained_drivers = forms.CharField()
    home_marina = forms.ModelChoiceField(queryset=Marina.objects.all(), required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email','phone_number','home_marina','password', 'role', 'trained_drivers']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        
        return email
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'