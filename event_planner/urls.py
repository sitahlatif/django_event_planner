from django.urls import path
from events.views import Login, Logout, profile, Signup, home,EventsList,EventsDetail,CreateEvent,UpdateEvent,DeleteEvent,dashboard,update_profile
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    EventListView,

)
urlpatterns = [
	path('', home, name='home'),
	path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
	path('EventList/',EventsList, name='event-list'),
	path('<int:event_id>/',EventsDetail, name='event-detail'),
	path('events/create', CreateEvent, name='create-event'),
    path('<int:event_id>/update/', UpdateEvent, name='update-event'),
    path('updateprofile/', update_profile, name='update-profile'),
    path('<int:event_id>/delete/', DeleteEvent, name='delete-event'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('api/list/', EventListView.as_view(), name='api-list')
]

if settings.DEBUG:
    '''Uncomment the next line to include your static files'''
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)