from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.conf import settings
from core.forms import *
from core.models import *
from datetime import datetime

# Create your views here.


def index_view(request):

    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.info(request, 'User is flagged Inactive')
                return HttpResponseRedirect(reverse('home'))
        else:
            messages.info(request, 'Invalid login details given')
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "index.html")
   

@login_required
def home_view(request):
    return render(request, "home.html")


@login_required
def all_interviews_view(request):
    current_time = datetime.now()
    upcoming_interviews = Interview.objects.exclude(
        start_time__lt = current_time
    )
    context = {
        'interviews' : upcoming_interviews,
    }
    return render(request, 'All_Interviews.html', context)

@login_required
def convert_to_datetime(request, date_obj):

    date_obj += ":00"
    date_obj = datetime.strptime(date_obj, '%d/%m/%Y %H:%M:%S')
    return date_obj

@login_required
def check_conflicts(request, participants, start, end):

    invalid_ids = []
    for part in participants:
        all_interviews = Interview.objects.filter(
            participant = int(part)
        )
        search_query = all_interviews.filter(
            start_time__lt = end
        ).exclude(
            end_time__lt = start
        )
        if search_query:
            invalid_ids.append(int(part))

    return invalid_ids


@login_required
def create_view(request):
    if request.method == 'POST':
        int_form = InterviewForm(request.POST)
        if int_form.is_valid:

            participant_pk = request.POST.getlist("participant")
            start_time = request.POST.get('start')
            end_time = request.POST.get('end')
            title = request.POST.get('Title')

            start_time = convert_to_datetime(request, start_time)
            end_time = convert_to_datetime(request, end_time)

            invalid_ids = check_conflicts(request,participant_pk, start_time, end_time)

            if (len(invalid_ids) == 0):
                interview_obj = Interview.objects.create(
                    name = title, 
                    start_time = start_time,
                    end_time = end_time
                )
                for participant in participant_pk:
                    part_id = int(participant)
                    part_user = Participant.objects.get(id = part_id)
                    ParticipantToInterview.objects.create(
                        participant = part_user,
                        interview = interview_obj
                    )
                return HttpResponseRedirect(reverse('create'))
            else:
                names = []
                form = InterviewForm()
                for participant in participant_pk:
                    part_id = int(participant)
                    part_user = Participant.objects.get(id = part_id)
                    names.append(part_user.name)
                context = {
                    'form' : form,
                    'names' : names,
                }
                return render(request,'create_interviews.html', context)
    else:
        form = InterviewForm()
        context = {
            'form' : form,
        }
        return render(request,'create_interviews.html', context)

