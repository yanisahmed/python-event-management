from django.urls import path
from event.views import *

urlpatterns = [
    path('', frontend_home, name='home'),
    path('admin/dashboard/', dashboard, name='dashboard'),
    path('admin/dashboard/events/', dashboard_event, name='event'),
    path('admin/dashboard/participants/', dashboard_participant, name='participant'),
    path('admin/dashboard/tickets/', dashboard_ticket, name='ticket'),
    path('admin/dashboard/settings/', dashboard_settings, name='settings')
]