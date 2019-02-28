from django.contrib import admin
from .models import Events ,BookedEvent


admin.site.register(Events)
admin.site.register(BookedEvent)