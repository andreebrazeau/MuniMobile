from django.db import models

class user_form(models.Model):
    # how do we want to define a blog post?
    phonenumber = models.CharField (max_length = 10)
    timeststamp = models.CharField (max_length = 256)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)