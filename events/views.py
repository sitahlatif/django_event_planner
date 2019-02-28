from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventsForm, BookForm, UpdateProfile
from django.contrib import messages
from .models import Events,BookedEvent
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render_to_response
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    now = timezone.now()
    context = {
        "event":Events.objects.filter(datetime__gte=now).order_by('datetime')[:3]
          }
    return render(request, 'home.html' , context)

def dashboard(request):
    event = request.user.events.all()
    book= request.user.bookings.all()
    context = {
        "event": event,
         "book":book,
          }
    return render(request, 'Dashboard.html' ,context)

def profile(request):
    event = request.user.events.all()
    context = {
        "event": event,
          }
   
    return render(request, 'profile.html', context)

def EventsList(request):
    now = timezone.now()
    event = Events.objects.filter(datetime__gte=now).order_by('datetime')
    query = request.GET.get('q')
    if query:
        event = event.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(location__icontains=query)|
            Q(owner__username__icontains=query)
            ).distinct()
    context = {
        "events":event,
    }
    return render(request, 'Events_list.html', context)

def EventsDetail(request, event_id):
    event = Events.objects.get(id=event_id)
    book= BookedEvent.objects.filter(event=event)
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST)
        if request.user.is_anonymous:
            messages.info(request, "You have to signin first!");
            return redirect('login')
        if form.is_valid():
            book = form.save(commit=False)
            if event.seats_left() == 0:
                 messages.info(request, "This event is full!")
                 return redirect(event)

            elif book.seats > event.seats_left():
                 messages.info(request, "Not allow to book more than avaliable!")
                 return redirect(event)

            else:
                 book = form.save(commit=False)
                 book.event = event
                 book.user= request.user
                 subject='Successfully Booking For Event'
                 message='Email to confirm the booking'
                 email_from=settings.EMAIL_HOST_USER
                 recipient_list=[request.user.email]
                 send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list
                    )
                 book.save()
                 messages.success(request, "Successfully Booked! You will receive Book information email")
                 return redirect('dashboard')
    context = {
        "event": event,
        "book":book,
        "form":form,
    }
    return render(request, 'Events_Detail.html', context)
def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')
def CreateEvent(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventsForm()
    if request.method == "POST":
        form = EventsForm(request.POST, request.FILES or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            messages.success(request, "Successfully Created!")
            return redirect('dashboard')
        messages.warning(request, form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create_events.html', context)

def UpdateEvent(request,event_id):
    event = Events.objects.get(id=event_id)
    if not(request.user.is_staff or request.user == event.owner):
        return redirect('signin')
    form = EventsForm(instance=event)

    if request.method == "POST":
        form = EventsForm(request.POST, request.FILES or None, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('dashboard')
        print (form.errors)
    context = {
    "form": form,
    "event": event,
    }
    return render(request, 'update_events.html', context)

def DeleteEvent(request,event_id):
    Events.objects.get(id=event_id).delete()
    if not (request.user.is_staff):
        return redirect('signin')
    messages.success(request, "Successfully Deleted!")
    return redirect('dashboard')

def update_profile(request):
    form= UpdateProfile()
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfile()

    context = {
    'form' : form,}
    return render(request, 'update_profile.html', context)

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                if Events.objects.filter(owner=auth_user):
                    messages.success(request, "Welcome Back!")
                    return redirect('dashboard')
                else:
                    return redirect('home')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        #messages.success(request, "You have successfully logged out.")
        return redirect("login")

