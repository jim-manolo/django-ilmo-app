from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone

from .models import Event,EventAttendee,Place
from .forms import get_form
from .utils import save_event_attendee,merge_dicts

import datetime

def get_all_events(request):
    events = Event.objects.all()
    return render(request,'list.html',{'event_list' : events})

def get_coming_events(request):
    events = Event.objects.filter(event_date__gte=timezone.now())
    return render(request,'list.html',{'event_list' : events, 'coming' : True})

def index(request):
    return render(request,'index.html',{'content' : "This is Ilmo App"})

def thanks(request):
    return render(request,'index.html',{'content' : "Thank you for registration"})

def parse_event_form(request,event_id):
    event_details = get_event_details(event_id)
    form_name = event_details['event'].form_name
    if request.method == 'POST':
        form = get_form(form_name)(request.POST)
        if form.is_valid():
            attendee = save_event_attendee(event_details['event'],form.cleaned_data)
            return render(request,'thanks.html',{'attendee' : attendee, 'event' : event_details['event']})
    else:
        form = get_form(form_name)
    data = merge_dicts(event_details,{'form' : form})
    return render(request, 'registration_form.html',data)

def get_event_details(event_id):
    event = Event.objects.get(id=event_id)
    attendees = EventAttendee.objects.filter(event=event_id)
    place = Place.objects.get(id=event.place_id)
    event
    return {'event' : event, 'attendees' : attendees, 'place' : place}