from django.urls import path
from . import views
urlpatterns = [
    path('', views.fleet_view, name='boats'),

    path('boats/<slug:slug>/', views.boat_detail_view, name='boat_detail'),
    path('locations/', views.locations_view, name='locations'),

    path('locations/<slug:slug>/', views.marina_detail_view, name='marina_detail'),
    path('locations/<slug:slug>/flyer',views.marina_flyer_view,name='marina_flyer'),

    path('reservations/', views.reservations_view, name='reservations'),

    # admin urls
    path('manage/add-boat/', views.AddBoatView.as_view(), name='add_boat'),
    path('manage/edit-boat/<slug:slug>/',views.BoatEditView.as_view(),name='edit_boat'),
    path('manage/add-location/',views.AddMarinaView.as_view(),name='add_location'),
    path('manage/edit-location/<slug:slug>/', views.MarinaEditView.as_view(), name='edit_location'),

]
