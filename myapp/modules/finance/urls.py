from django.urls import path
from . import views  # views.py dosyanın var olduğundan emin ol

app_name = "finance"

urlpatterns = [
    path('', views.index, name='finance'),

]