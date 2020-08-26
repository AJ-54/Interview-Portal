from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
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
   

@login_required(login_url='/')
def home_view(request):
    return render(request, "home.html")

@login_required(login_url='/')
def upcoming_interview(request):
    current_time = datetime.now()
    upcoming_interviews = Interview.objects.exclude(
        start_time__lt = current_time
    )
    return upcoming_interviews

@login_required(login_url='/')
def all_interviews_view(request):
    upcoming_interviews = upcoming_interview(request)
    context = {
        'interviews' : upcoming_interviews,
    }
    return render(request, 'All_Interviews.html', context)

@login_required(login_url='/')
def convert_to_datetime(request, date_obj):

    try:
        mod_obj = date_obj + ":00"
        mod_obj = datetime.strptime(mod_obj, '%d/%m/%Y %H:%M:%S')
        return mod_obj
    except:
        return "old"

@login_required(login_url='/')
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

@login_required(login_url='/')
def interview_object_create(request, title,  start, end, participants):
    interview_obj = Interview.objects.create(
        name = title, 
        start_time = start,
        end_time = end
    )
    for participant in participants:
        part_id = int(participant)
        part_user = Participant.objects.get(id = part_id)
        ParticipantToInterview.objects.create(
            participant = part_user,
            interview = interview_obj
        )

@login_required(login_url='/')
def send_creation_mail(request, participants, start, end):
    recipient_list = []
    subject = "Your Interview with InterviewBit is Scheduled"
    message = "Hello, your interview with InterviewBit is scheduled from " + str(start) + " to " + str(end) +  ". We expect your presence!"
    from_id = 'ayush.jain@pro-coder.tech'

    for part in participants:
        part = int(part)
        pat_obj = Participant.objects.get(id = part)
        recipient_list.append(pat_obj.email)
    
    send_mail(
        subject,
        message,
        from_id,
        recipient_list,
        fail_silently=False,
    )

@login_required(login_url='/')
def create_view(request):
    if request.method == 'POST':
        int_form = InterviewForm(request.POST)
        if int_form.is_valid:

            participant_pk = request.POST.getlist("participant")        
            if (len(participant_pk) < 2):
                form = InterviewForm()
                context = {
                    'form' : form,
                    'lessthantwo' : True,
                }
                return render(request,'create_interviews.html', context)
            
            start_time = request.POST.get('start')
            end_time = request.POST.get('end')
            title = request.POST.get('Title')

            start_time = convert_to_datetime(request, start_time)
            end_time = convert_to_datetime(request, end_time)

            invalid_ids = check_conflicts(request,participant_pk, start_time, end_time)

            if (len(invalid_ids) == 0):
                interview_object_create(request, title, start_time, end_time, participant_pk)
                send_creation_mail(request, participant_pk,  start_time, end_time)
                return HttpResponseRedirect(reverse('create'))
            else:
                names = []
                form = InterviewForm()
                for participant in invalid_ids:
                    part_id = participant
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

@login_required(login_url='/')
def update_interview_view(request):
    upcoming_interviews = upcoming_interview(request)
    context = {
        'interviews' : upcoming_interviews,
    }
    return render(request,'edit_interviews.html',context)

@login_required(login_url='/')
def check_updates_conflicts(request, participants, start, end, id):

    invalid_ids = []
    for part in participants:
        all_interviews = Interview.objects.filter(
            participant = int(part)
        ).exclude(id = id)
        search_query = all_interviews.filter(
            start_time__lt = end
        ).exclude(
            end_time__lt = start
        )
        if search_query:
            invalid_ids.append(int(part))

    return invalid_ids

@login_required(login_url='/')
def update_one_interview_view(request, pk):

    interview_obj = Interview.objects.get(pk = pk)
    participants = Participant.objects.all()
    if request.method == 'POST':
        participant_pk = request.POST.getlist("participant")

        if (len(participant_pk) < 2):
                context = {
                    'obj' : interview_obj,
                    'participants' : participants,
                    'lessthantwo' : True,
                }
                return render(request,'edit_one_interview.html', context)

        start_time = request.POST.get('start')
        end_time = request.POST.get('end')
        title = request.POST.get('Title')
        start_time = convert_to_datetime(request,start_time)
        end_time = convert_to_datetime(request,end_time)
        if (start_time == "old"):
            start_time = interview_obj.start_time
        if (end_time == "old"):
            end_time = interview_obj.end_time
        
        invalid_ids = check_updates_conflicts(request, participant_pk, start_time, end_time, pk)

        if (len(invalid_ids) == 0):
            interview_obj.delete()
            interview_object_create(request, title, start_time, end_time, participant_pk)
            send_creation_mail(request, participant_pk,  start_time, end_time)
            return render(request,'edit_interviews.html')
        else:
            names = []
            for participant in invalid_ids:
                part_id = participant
                part_user = Participant.objects.get(id = part_id)
                names.append(part_user.name)
            context = {
                'obj' : interview_obj,
                'participants' : participants,
                'names' : names,
            }
            return render(request,'edit_one_interview.html', context)

    else:
        context = {
            'obj' : interview_obj,
            'participants' : participants,
        }
        return render(request,'edit_one_interview.html', context)

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
