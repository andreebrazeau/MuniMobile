from django.db import models

class user_form(models.Model):
    # how do we want to define a user_form post?
    phone_number = models.CharField (max_length = 10)
    timestamp = models.DateTimeField(auto_now_add=True)
    route_tag = models.CharField (max_length = 256)
    direction_tag = models.CharField (max_length = 256)
    stop_id = models.CharField (max_length = 256)
    start_time = models.CharField (max_length = 10, default = "0")
    finish_time = models.CharField (max_length = 10, default = "0")
    days = models.CharField (max_length = 10)
    minutes_away = models.CharField (max_length = 5, default = "0")
    bus_tag = models.CharField (max_length = 10, default='None')
    activated = models.BooleanField(default = True)

    def __unicode__(self):
        return self.phone_number

'''
from MuniMobile_app.models import user_form
from django.utils import timezone
p = user_form(phone_number = '+16504552830', timestamp=timezone.now(), route_tag = '1', direction_tag = 'inbound', stop_id = "13885")
p.save()
p = user_form(phone_number = '+16504552830', timestamp=timezone.now(), route_tag = '24', direction_tag = 'inbound', stop_id = "17213")
p.save()
user_form.objects.all()
'''
