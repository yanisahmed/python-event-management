from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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

def event_details(request, event_id):
    print(event_id)
    event = Event.objects.select_related('category').prefetch_related('participants').filter(id=event_id).first()
    if not event:
        messages.error(request, 'Event not found.')
        return redirect('event')
    
    context = {
        'event': event
    }
    return render(request, 'frontend/event-details.html', context)



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

# EVENT
def dashboard_event(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    context = {
        'events':events
    }
    return render(request, 'dashboard/dashboard-event.html', context)

def dashboard_event_add(request):
    
    event_form = AddEventForm()

    if request.method == 'POST':
        event_form = AddEventForm(request.POST)
        
        if event_form.is_valid():
            event_form.save()
        
        messages.success(request, 'Event created successfully.')
        return redirect('event')

    context = {
        'action' : 'Add Event',
        'event_form': event_form
    }
    return render(request, 'dashboard/dashboard-event-form.html', context)

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
        'action': 'Edit Event',
        'event_form': event_form
    }
    return render(request, 'dashboard/dashboard-event-form.html', context)

def dashboard_event_delete(request, id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=id)
        event.delete()
        messages.success(request, 'Event has been deleted')
    return redirect('event')

# PARTICIPANT
def dashboard_participant(request):
    participants = Participant.objects.prefetch_related('event').all()
    context = {
        'participants': participants,
    }

    return render(request, 'dashboard/dashboard-participant.html', context)

def dashboard_participant_add(request):
    participant_form = AddParticipantForm()

    if request.method == 'POST':
        participant_form = AddParticipantForm(request.POST)
        
        if participant_form.is_valid():
            participant_form.save()
        
        messages.success(request, 'Participant added successfully.')
        return redirect('participant')
    context = {
        'action': 'Add Participant',
        'participant_form': participant_form
    }

    return render(request, 'dashboard/dashboard-participant-form.html', context)

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
        'action' : 'Edit Participant',
        'participant_form': participant_form
    }

    return render(request, 'dashboard/dashboard-participant-form.html', context)

def dashboard_participant_delete(request, id):
    if request.method == "POST":
        participant = get_object_or_404(Participant, id=id)
        participant.delete()
        messages.success(request, 'Participant has been deleted')
    return redirect('participant')
# CATEGORY
def dashboard_category(request):
    category_query = Category.objects.all()
    context = {
        'categories': category_query
    }
    return render(request, 'dashboard/dashboard-category.html', context)

def dashboard_category_add(request):
    category_form = AddCategoryForm()
    if request.method == 'POST':
        category_form = AddCategoryForm(request.POST)
        
        if category_form.is_valid():
            category_form.save()
        
        messages.success(request, 'Category added successfully.')
        return redirect('category')
    context = {
            'action': 'Add Category',
            'category_form': category_form
        }
    return render(request, 'dashboard/dashboard-category-form.html', context)

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
        'action': 'Edit Category',
        'category_form': category_form
    }
    return render(request, 'dashboard/dashboard-category-form.html', context)

def dashboard_category_delete(request, id):
    if request.method == "POST":
        cat = get_object_or_404(Category, id=id)
        cat.delete()
        messages.success(request, 'Category has been deleted')
    return redirect('category')

def dashboard_settings(request):
    return render(request, 'dashboard/dashboard-settings.html')
