from rest_framework.generics import (
	ListAPIView, 
)
from events.models import Events
from django.utils import timezone
from .serializers import( 
	EventListSerializer, 
)
class EventListView(ListAPIView):
	now = timezone.now()
	queryset = Events.objects.filter(datetime__gte=now).order_by('datetime')
	serializer_class = EventListSerializer
