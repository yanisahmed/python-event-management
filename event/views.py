from django.http import HttpResponse
from django.shortcuts import render, redirect
from event.forms import AddEventForm
from django.contrib import messages

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard-home.html')

def dashboard_event(request):
    event_form = AddEventForm()

    if request.method == 'POST':
        event_form = AddEventForm(request.POST)
        
        if event_form.is_valid():
            event_form.save()
            event_form = AddEventForm()
        
        messages.success(request, 'Event created successfully.')
        return redirect('event')

    context = {
        'event_from': event_form
    }
    return render(request, 'dashboard/dashboard-event.html', context)


def dashboard_participant(request):
    return render(request, 'dashboard/dashboard-participant.html')

def dashboard_ticket(request):
    return render(request, 'dashboard/dashboard-ticket.html')

def dashboard_settings(request):
    return render(request, 'dashboard/dashboard-settings.html')