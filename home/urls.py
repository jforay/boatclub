from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('amenities/', views.amenities, name='amenities'),
    path('equipment/',views.equipment, name='equipment'),
    path('first-responders/',views.first_responders,name='first-responders'),
    path('FAQs/',views.FAQs, name='FAQs'),
    path('perks/', views.perks, name='perks'),
    path('reasons-to-join/',views.reasons_to_join,name='reasons_to_join'),
    path('accessibilities/',views.accessibilities, name='accessibilities'),
    path('contact-us/',views.contact_us,name='contact-us'),
    path('training/',views.training,name="training"),
    path('qr/<slug:location>/', views.qr_redirect, name='qr_redirect')
]

