from django.urls import path
from .views import AllReservationsView, DailyReservationsView, ReserveBoatView, UserReservationsView, reservation_detail_view, float_plan_view ,submit_float_plan_pdf
from .views import cancel_reservation, DailyScheduleView, reservation_calendar_view, marinas_for_schedule_view, marina_schedule_view, schedule_or_reservations_view, send_document

urlpatterns = [
    path('schedule/', marinas_for_schedule_view, name='marinas_for_schedule'),
    path('schedule/<int:marina_id>/', schedule_or_reservations_view, name='schedule_or_reservations'),
    path('schedule/<int:marina_id>/calendar/', marina_schedule_view, name='schedule_calendar'),
    path('reservations/<int:marina_id>/calendar/',reservation_calendar_view, name='reservation_calendar'),
    path('schedule/<int:marina_id>/<str:date>/', DailyScheduleView.as_view(), name='daily_schedule_view'),

    
    path('', AllReservationsView.as_view(), name='all_reservations'),
    path('<int:marina_id>/<str:date>/', DailyReservationsView.as_view(), name='reservations_for_day'),
    path('reserve/<int:boat_id>/<str:date>', ReserveBoatView.as_view(), name='reserve_boat'),
    path('<int:reservation_id>', reservation_detail_view, name='reservation_detail'),
    path('cancel/<int:reservation_id>', cancel_reservation, name='cancel_reservation'),
    path('floatplan/<int:reservation_id>/',float_plan_view, name='float_plan'),
    path("submit-float-plan/<int:reservation_id>/", submit_float_plan_pdf, name="submit_float_plan_pdf"),
    path('send-float-plan/', send_document, name='send_float_plan'),


    
    

]
