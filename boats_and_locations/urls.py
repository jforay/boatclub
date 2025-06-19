from django.urls import path
from . import views
urlpatterns = [
    path('', views.fleet_view, name='boats'),
    path('<int:boat_id>/', views.boat_detail_view, name='boat_detail'),
    path('<int:boat_id>/<str:date>',views.BoatAvailabilityView.as_view(), name ='boat_availabilty'),
    path('locations/', views.locations_view, name='locations'),
    path('location/<int:marina_id>/', views.marina_detail_view, name='marina_detail'),
    path('add-boat/', views.AddBoatView.as_view(), name='add_boat'),
    path('edit-boat/<int:pk>/',views.BoatEditView.as_view(),name='edit_boat'),
    path('add-location/',views.AddMarinaView.as_view(),name='add_location'),
    path('edit-location/<int:pk>/', views.MarinaEditView.as_view(), name='edit_location'),
]
