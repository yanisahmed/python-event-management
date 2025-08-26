from django.urls import path
from event.views import *

urlpatterns = [
    path('', frontend_home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/events/', dashboard_event, name='event'),
    path('dashboard/participants/', dashboard_participant, name='participant'),
    path('dashboard/tickets/', dashboard_ticket, name='ticket'),
    path('dashboard/settings/', dashboard_settings, name='settings')
]