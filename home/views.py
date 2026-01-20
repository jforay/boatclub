from django.shortcuts import render,get_object_or_404
from boats_and_locations.models import Boat,Marina
from .forms import ContactUs, JoinUs
from django.http import JsonResponse
# Create your views here.
def home(request):
    boats = Boat.objects.order_by('?')[:12]
    marinas = Marina.objects.exclude(image="").exclude(image__isnull=True)
    unique_lakes = []
    seen_lakes = []
    for marina in marinas:
        if marina.lake in seen_lakes:
            continue
        else:
            unique_lakes.append(marina)
    is_boss = request.user.groups.filter(name='Boss').exists()
    is_manager = request.user.groups.filter(name='Manager').exists()
    return render(request, 'home/home.html', {'boats':boats, 'unique_lakes':unique_lakes})
    

def maintenance(request):
    return render(request, 'home/maintenance.html')

def amenities(request):
    return render(request,'home/amenities.html')

def equipment(request):
    return render(request, 'home/equipment.html')

def first_responders(request):
    return render(request,'home/first-responders.html')

def FAQs(request):
    return render(request, 'home/FAQs.html')

def perks(request):
    return render(request, 'home/perks.html')

def reasons_to_join(request):
    return render(request, 'home/reasons-to-join.html')

def join(request):
    form = JoinUs()
    return render(request, 'home/join.html', {'form':form})

def accessibilities(request):
    return render(request, 'home/accessibilities.html')

def contact_us(request):
    form = ContactUs()
    return render(request,'home/contact-us.html',{'form':form})
