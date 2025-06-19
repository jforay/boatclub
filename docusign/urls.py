from django.urls import path
from .views import send_float_plan

urlpatterns = [
    path("send-float-plan/", send_float_plan, name="send_float_plan"),
]