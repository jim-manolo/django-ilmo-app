import sys
import json
from django.db import models
from django.utils import timezone
from djangocms_text_ckeditor.fields import HTMLField

# DB MODELS
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50,blank=True)
    zip_code = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(blank=True,null=True)
    method = models.CharField(choices=[(i,i) for i in ["Tilisiirto","Käteinen","Ilmainen","Muu"]],max_length=100)
    receiver = models.CharField(max_length=50,blank=True)
    reference_number = models.PositiveIntegerField(blank=True, null=True)
    due_to = models.DateField(blank=True,null=True)
    account = models.CharField(blank=True,null=True,max_length=100)
    special_price_offsets = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    form_name = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    place = models.ForeignKey(Place)
    close_date = models.DateTimeField()
    fb_url = models.URLField(blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    payment = models.ForeignKey(Payment,blank=True)
    image_url = models.CharField(max_length=1000,blank=True)
    description = HTMLField()
    thank_you_text = HTMLField()
    backup = models.BooleanField(verbose_name="Accept backup seats?",default=True)

    def __str__(self):
        return self.name

    def is_past(self):
        if timezone.now() > self.close_date:
            return True
        return False

    def is_full(self):
        count = EventAttendee.objects.filter(event__id=self.id).count()
        capacity = self.capacity if self.capacity is not None else sys.maxsize
        if capacity <= count:
            return True
        return False

class EventAttendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_name = models.CharField(max_length=50)
    attendee_email = models.CharField(max_length=50,blank=True)
    attendee_phone = models.CharField(max_length=50,blank=True)
    attendee_gender = models.CharField(max_length=50,blank=True)
    attendee_details = models.CharField(max_length=500,blank=True)
    isbackup = models.BooleanField(verbose_name="Is a backup?", default=False)
    registration_date = models.DateTimeField()

    def __str__(self):
        return self.attendee_name

    def get_price(self):
        price = self.event.payment.price
        ep = Payment.objects.get(event=self.event)
        try:
            special_prices_map = json.loads(ep.special_price_offsets)
        except ValueError:
            return price
        else:
            attendee_details_map = json.loads(self.attendee_details)
            for name,offsets in special_prices_map.items():
                price += offsets.get(attendee_details_map.get(name),0)
            return price

    def __get_check_number(self):
        base = self.event.payment.reference_number + self.id
        sum = 0
        a = [7,3,1]
        i = 0
        while base > 0:
            sum += (base % 10) * a[i]
            base /= 10
            i = (i + 1) % 3
        ret = sum % 10
        return 0 if ret == 0 else int(10 - ret)

    def get_reference_number(self):
        r = self.event.payment.reference_number
        if r is None:
            return r
        return r * 10 + self.__get_check_number()
