from django.urls import path
from .views import upload_filled_plan

urlpatterns = [
    path("upload/", upload_filled_plan, name="upload_filled_plan"),
]
