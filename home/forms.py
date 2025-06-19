from django import forms
from .models import Contact,Join

class ContactUs(forms.ModelForm):
    desired_location = forms.CharField(label='Desired Location',required=True)
    email = forms.CharField(required=True)
    first_name = forms.CharField(label='First Name',required=True)
    last_name = forms.CharField(label='Last Name',required=True)
    phone_number = forms.CharField(label='Phone Number',required=True)
    question = forms.CharField(label='Questions/Concerns', required=False, widget=forms.Textarea())

    class Meta:
        model = Contact
        fields = ['desired_location','email','first_name','last_name','phone_number','question']


class JoinUs(forms.ModelForm):
    desired_location = forms.CharField(label='Desired Location',required=True)
    email = forms.CharField(required=True)
    first_name = forms.CharField(label='First Name',required=True)
    last_name = forms.CharField(label='Last Name',required=True)
    phone_number = forms.CharField(label='Phone Number',required=True)

    class Meta:
        model = Join
        fields = ['desired_location','email','first_name','last_name','phone_number']


