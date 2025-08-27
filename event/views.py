from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from event.forms import AddEventForm, AddParticipantForm, AddCategoryForm
from django.contrib import messages
from event.models import Event, Participant, Category
from django.db.models import Count, Q

# Create your views here.
def frontend_home(request):
    return render(request, 'frontend/home.html')    

def dashboard(request):
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    
    counts = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events=Count('id', filter=Q(date__gt=datetime.now())),
        past_events=Count('id', filter=Q(date__lt=datetime.now())),
        participants=Count('participants', distinct=True)
    )

    type = request.GET.get('type', 'All')
    if type == 'upcoming-events':
        events = base_query.filter(date__gt=datetime.now())
        events.title = "Upcoming Events"
    elif type == 'past-events':
        events = base_query.filter(date__lt=datetime.now())
        events.title = "Past Events"
    elif type == 'participants':
        events = base_query.filter(participants__isnull=False).distinct()
        events.title = "Events with Participants"
    elif type == 'All':
        events = base_query.all()
        events.title = "All Events"

    context = {
        'events': events,
        'counts': counts
    }
    return render(request, 'dashboard/dashboard-home.html', context)

def dashboard_event(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    event_form = AddEventForm()

    if request.method == 'POST':
        event_form = AddEventForm(request.POST)
        
        if event_form.is_valid():
            event_form.save()
            event_form = AddEventForm()
        
        messages.success(request, 'Event created successfully.')
        return redirect('event')

    context = {
        'events':events,
        'event_from': event_form
    }
    return render(request, 'dashboard/dashboard-event.html', context)


def dashboard_participant(request):
    participants = Participant.objects.prefetch_related('event').all()
    participant_form = AddParticipantForm()

    if request.method == 'POST':
        participant_form = AddParticipantForm(request.POST)
        
        if participant_form.is_valid():
            participant_form.save()
            participant_form = AddParticipantForm()
        
        messages.success(request, 'Participant added successfully.')
        return redirect('participant')
    context = {
        'participants': participants,
        'participant_form': participant_form
    }

    return render(request, 'dashboard/dashboard-participant.html', context)

def dashboard_category(request):
    category_query = Category.objects.all()
    category_form = AddCategoryForm()
    if request.method == 'POST':
        category_form = AddCategoryForm(request.POST)
        
        if category_form.is_valid():
            category_form.save()
            category_form = AddCategoryForm()
        
        messages.success(request, 'Category added successfully.')
        return redirect('category')
    context = {
            'categories': category_query,
            'category_form': category_form
        }
    return render(request, 'dashboard/dashboard-category.html', context)

def dashboard_settings(request):
    return render(request, 'dashboard/dashboard-settings.html')