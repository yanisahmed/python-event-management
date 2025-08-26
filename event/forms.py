from django import forms
from event.models import Event

class CreateUpdateMixin:
    default_class = 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none'
    date_class = 'border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none'
    def apply_mixin(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.SelectDateWidget):
                field.widget.attrs.update({'class': self.date_class, 'type': 'date'})
            elif isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs.update({'class': self.default_class, 'rows': 4})
            else:
                field.widget.attrs.update({'class': self.default_class})

# Add Event Form fields
class AddEventForm(CreateUpdateMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'description']
        widgets = {
            'date': forms.SelectDateWidget
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_mixin()