from django.urls import path
from event.views import *

urlpatterns = [
    path('', frontend_home, name='home'),
    path('events/<int:event_id>/', event_details, name='event-details'),
    
    path('admin/dashboard/', dashboard, name='dashboard'),

    path('admin/dashboard/events/', dashboard_event, name='event'),
    path('admin/dashboard/events/add-new-event/', dashboard_event_add, name="event-add"),
    path('admin/dashboard/events/edit/<int:event_id>/', dashboard_event_edit, name="event-edit"),
    path('admin/dashboard/events/delete/<int:id>/', dashboard_event_delete, name="event-delete"),
    

    path('admin/dashboard/participants/', dashboard_participant, name='participant'),
    path('admin/dashboard/participants/add-new-participant/', dashboard_participant_add, name='participant-add'),
    path('admin/dashboard/participants/<int:id>/', dashboard_participant_edit, name='participant-edit'),
    path('admin/dashboard/participants/delete/<int:id>/', dashboard_participant_delete, name='participant-delete'),

    path('admin/dashboard/categories/', dashboard_category, name='category'),
    path('admin/dashboard/categories/add-new-category/', dashboard_category_add, name="category-add" ),
    path('admin/dashboard/categories/<int:cat_id>/', dashboard_category_edit, name="category-edit" ),
    path('admin/dashboard/categories/delete/<int:id>/', dashboard_category_delete, name="category-delete" ),

    path('admin/dashboard/settings/', dashboard_settings, name='settings')
]