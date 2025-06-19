from django import forms
from .models import Boat,Marina

class AddBoatForm(forms.ModelForm):
    name = forms.CharField(required=True)
    boat_type = forms.CharField()
    description = forms.CharField(required=True)
    marina = forms.ModelChoiceField(queryset=Marina.objects.all(), required=True)
    rules = forms.CharField(required=True)
    issues = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    
    class Meta:
        model = Boat
        fields = ['name','boat_type','marina','description','rules','issues','image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Use Textarea for longer text fields
            'rules': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'image': forms.ClearableFileInput(),  # To handle file uploads
        }


class AddMarinaForm(forms.ModelForm):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    lake = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    state = forms.CharField(required=True)
    class Meta:
        model = Marina
        fields = ['name','address','state','lake','image']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols':40})
        }

class EditMarinaForm(forms.ModelForm):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    lake = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    state = forms.CharField(required=True)
    class Meta:
        model = Marina
        fields = ['name','address','state','lake','image']