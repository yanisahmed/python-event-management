from django.urls import path
from event.views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/events/', dashboard_event, name='event'),
    path('dashboard/events/create/', dashboard_event_create, name='create_event'),
    path('dashboard/participants/', dashboard_participant, name='event'),
    path('dashboard/tickets/', dashboard_ticket, name='ticket'),
    path('dashboard/settings/', dashboard_settings, name='settings')
]