from django.shortcuts import render

# Create your views here.
from django.db.models import Sum
from django.http import JsonResponse

from task.models import City
import ganga.ganga
from gangagsoc.Initial_Task.countWord import * 
import threading
from ganga import *


def Subtask1(request):
    labels = []
    data = []
    queryset = City.objects.values('country__name').annotate(country_population=Sum('population')).order_by('-country_population')
    for entry in queryset:
        labels.append(entry['country__name'])
        data.append(entry['country_population'])   
    return render(request, 'subtask1.html', {
        'labels': labels,
        'data': data,
    })



def population_chart(request):
    country = request.GET['country'];
    labels = []
    data = []
    queryset = City.objects.filter(country__name=country).order_by('-population')[:5]
    for city in queryset:
        labels.append(city.name)
        data.append(city.population)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def Subtask2(request):
    return render(request, 'subtask2.html')

def job_submit(request):
    j = Job()
    j_id = j.id
    j.submit()
    x = threading.Thread(target=check_job_until_completed, args=(j,))
    x.start()
    return JsonResponse(data={
        'job_id': j_id
    })

def status_monitor(request):
    job_id = request.GET['j_id'];
    status = jobs(int(job_id)).status
    if status=='completed':
        output = jobs(int(job_id)).peek('stdout','more')
        print("Got it: ",output)
        return JsonResponse(data={
        'job_status': jobs(int(job_id)).status,
        'job_output': output
        })
    return JsonResponse(data={
        'job_status': jobs(int(job_id)).status
    })

