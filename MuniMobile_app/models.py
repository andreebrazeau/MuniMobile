from django.db import models
from datetime import datetime

class Notification(models.Model):
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

    @staticmethod
    def index():
        active_notif = Notification.objects.filter(activated = True)
        return active_notif

    @staticmethod
    def create(params):
        notif = Notification()
        notif.set_params(params)
        try:
            notif.save()
            message = { 'message': 'Success!' }
        except: 
            message = {'message': "We coun't save you datas"}
        return message

    @staticmethod
    def update(params):
        notif = Job.objects.get(phone_number = params['phone_number'])
        notif.set_params(params)
        notif.save()
        return notif

    @staticmethod
    def notification_in_periode(now):
        start_str = datetime.strptime(str(now.year) + ":" +str(now.month) + ":" +str(now.day) + ":" + start_time, "%Y:%m:%d:%H:%M")
        finish_str = datetime.strptime(str(now.year) + ":" +str(now.month) + ":" +str(now.day) + ":" + finish_time, "%Y:%m:%d:%H:%M")
        week_day = str(now.isoweekday())
        active_notif = Notification.objects.filter(activated = True, start_time__gte = start_time, finish_time__gte = finish_time, days__contains = week_day)
        return active_notif

    def set_params(self, params):
        
        for key in ['phone_number', 'timestamp', 'route_tag', 'direction_tag', 'stop_id', 'start_time', 'finish_time', 'days', 'minutes_away']: # set all params
            if params.has_key(key):
                setattr(self, key, params[key])
                print key, getattr(self,key)

        