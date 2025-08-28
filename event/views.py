from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from event.forms import AddEventForm, AddParticipantForm, AddCategoryForm
from django.contrib import messages
from event.models import Event, Participant, Category
from django.db.models import Count, Q

# Create your views here.
def frontend_home(request):
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    category_query = Category.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        base_query = base_query.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(category__name__icontains=search_query)
        )

    # Category filter
    category = request.GET.get('category', '')
    if category:
        base_query = base_query.filter(category__name__icontains=category)

    # Date range filter
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    if start_date and end_date:
        base_query = base_query.filter(date__range=[start_date, end_date])
    elif start_date:
        base_query = base_query.filter(date__gte=start_date)
    elif end_date:
        base_query = base_query.filter(date__lte=end_date)

    # Sorting
    sort = request.GET.get('sort', '')
    if sort == 'newest':
        base_query = base_query.order_by('-date')
    elif sort == 'oldest':
        base_query = base_query.order_by('date')
    elif sort == 'name-asc':
        base_query = base_query.order_by('name')
    elif sort == 'name-desc':
        base_query = base_query.order_by('-name')

    context = {
        'events': base_query
        ,'category_query': category_query,
    }
    return render(request, 'frontend/home.html', context)   

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

def dashboard_event_edit(request, event_id):
    event = Event.objects.get(id=event_id)
    event_form = AddEventForm(instance=event)

    if request.method == 'POST':
        event_form = AddEventForm(request.POST, instance=event)
        
        if event_form.is_valid():
            event_form.save()
        
        messages.success(request, 'Event updated successfully.')
        return redirect('event')

    context = {
        'event_form': event_form
    }
    return render(request, 'dashboard/dashboard-event-form.html', context)


def dashboard_event_details(request, event_id):
    print(event_id)
    event = Event.objects.select_related('category').prefetch_related('participants').filter(id=event_id).first()
    if not event:
        messages.error(request, 'Event not found.')
        return redirect('event')
    
    context = {
        'event': event
    }
    return render(request, 'frontend/event-details.html', context)


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

def dashboard_participant_edit(request, id):
    participant = Participant.objects.get(id=id)
    participant_form = AddParticipantForm(instance=participant)

    if request.method == 'POST':
        participant_form = AddParticipantForm(request.POST, instance=participant)
        
        if participant_form.is_valid():
            participant_form.save()
        
        messages.success(request, 'Participant Updated successfully.')
        return redirect('participant')
    context = {
        'participant_form': participant_form
    }

    return render(request, 'dashboard/dashboard-participant-form.html', context)

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

def dashboard_category_edit(request, cat_id):
    cat = Category.objects.get(id = cat_id)
    category_form = AddCategoryForm(instance = cat)

    if not cat:
        messages.error(request, 'Category Not Found')
        return redirect('category')

    if request.method == 'POST':
        category_form = AddCategoryForm(request.POST, instance = cat)
        if category_form.is_valid():
            category_form.save()

        messages.success(request, 'Category upated Successfully')
        return redirect('category')
    
    context = {
        'category_form': category_form
    }
    return render(request, 'dashboard/dashboard-category-form.html', context)

def dashboard_settings(request):
    return render(request, 'dashboard/dashboard-settings.html')
