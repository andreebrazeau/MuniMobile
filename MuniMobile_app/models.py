from django.db import models

class user_form(models.Model):
    # how do we want to define a user_form post?
    phonenumber = models.CharField (max_length = 10)
    timeststamp = models.DateTimeField(auto_now_add=True)
    bus_line = models.CharField (max_length = 256)
    direction = models.CharField (max_length = 256)
    Stop_id = models.CharField (max_length = 256)

    def __unicode__(self):
        return self.phonenumber
        
