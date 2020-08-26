from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator
import datetime

class Participant(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)

    def __str__(self):
        return self.name

class Interview(models.Model):
    name = models.CharField(max_length=50)
    participant = models.ManyToManyField("Participant", related_name = "interviews", through = 'ParticipantToInterview')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class ParticipantToInterview(models.Model):
    participant = models.ForeignKey("Participant", on_delete=models.CASCADE)
    interview = models.ForeignKey("Interview", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.interview.name + " - " + self.participant.name

