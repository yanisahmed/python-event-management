from django.db import models

# Create your models here.

def get_default_category():
    category, created = Category.objects.get_or_create(name="Uncategorized")
    return category.id   # must return the PK

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name   

class Event(models.Model):
    choices = [
        ('Scheduled', 'Scheduled'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET(get_default_category), default=get_default_category, related_name='events')
    staus = models.CharField(max_length=50, default='Scheduled', choices=choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Participant(models.Model):
    event = models.ManyToManyField(Event, related_name='participants')
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

 