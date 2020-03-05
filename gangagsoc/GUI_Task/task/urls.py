from django.conf.urls import url, include
from . import views
app_name = 'task'
urlpatterns = [
	url(r'^subtask1/', views.Subtask1, name='Subtask1'),
    url(r'^subtask2/', views.Subtask2, name='Subtask2'),   
    url(r'^population-chart/', views.population_chart, name='population-chart'),
	url(r'^status-monitor/', views.status_monitor, name='status-monitor'),
	url(r'^job-submit/', views.job_submit, name='job-submit'),	 
]
