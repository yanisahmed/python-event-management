from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard-home.html')

def dashboard_event(request):
    return render(request, 'dashboard/dashboard-event.html')

def dashboard_participant(request):
    return render(request, 'dashboard/dashboard-participant.html')

def dashboard_ticket(request):
    return render(request, 'dashboard/dashboard-ticket.html')

def dashboard_settings(request):
    return render(request, 'dashboard/dashboard-settings.html')