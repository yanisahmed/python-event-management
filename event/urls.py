from django.urls import path
from event.views import *

urlpatterns = [
    path('', frontend_home, name='home'),
    path('admin/dashboard/', dashboard, name='dashboard'),
    path('admin/dashboard/events/', dashboard_event, name='event'),
    path('admin/dashboard/events/<int:event_id>/', dashboard_event_details, name='event-details'),
    path('admin/dashboard/events/edit/<int:event_id>/', dashboard_event_edit, name="event-edit"),

    path('admin/dashboard/participants/', dashboard_participant, name='participant'),
    path('admin/dashboard/participants/<int:id>', dashboard_participant_edit, name='participant-edit'),

    path('admin/dashboard/categories/', dashboard_category, name='category'),
    path('admin/dashboard/categories/<int:cat_id>/', dashboard_category_edit, name="category-edit" ),

    path('admin/dashboard/settings/', dashboard_settings, name='settings')
]