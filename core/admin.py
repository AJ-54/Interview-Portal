from django.contrib import admin
from core.models import *

admin.site.register(Participant)
admin.site.register(Interview)
admin.site.register(ParticipantToInterview)