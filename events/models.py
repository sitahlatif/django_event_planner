from django.db import models
#from location_field.models.plain import PlainLocationField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User
from django.urls import reverse
#from datetime import datetime
#Change to Event
class Events(models.Model):
     owner= models.ForeignKey(User,on_delete=models.CASCADE, related_name='events')
     title= models.CharField( max_length=20)
     description=models.TextField()
     location=models.CharField(max_length=40)
     datetime=models.DateTimeField()
     seats= models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2000)])
     pretty_picture = models.ImageField(null=True, blank=True)
     def __str__(self):
         return self.title

     def get_absolute_url(self):
         return reverse('event-detail', kwargs={'event_id':self.id})

     def seats_left(self):
         return self.seats - sum(self.bookings.all().values_list('seats', flat=True))


class BookedEvent(models.Model):
     user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="bookings")
     event= models.ForeignKey(Events, on_delete=models.CASCADE,related_name="bookings")
     seats=models.PositiveIntegerField()
      