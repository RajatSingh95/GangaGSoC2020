from django.test import TestCase
from task.models import *
from django.db.models import Sum
import json
import ganga.ganga
from ganga import *
from gangagsoc.Initial_Task.countWord import * 
import threading

class GUITestCase(TestCase):
    def setUp(self):
        country1 = Country.objects.create(name="China")
        country2 = Country.objects.create(name="Singapore")

        city1 = City.objects.create(name="Shanghai",population=34000000,country=country1)
        city2 = City.objects.create(name="Guangzhou",population=25000000,country=country1)
        city3 = City.objects.create(name="Beijing",population=24900000,country=country1)
        city4 = City.objects.create(name="Shenzhen",population=23300000,country=country1)
        city5 = City.objects.create(name="Singapore",population=5535000,country=country2)


    def test_subtask1(self):
        country_population = City.objects.values('country__name').annotate(country_population=Sum('population')).order_by('-country_population')
        
        self.assertEqual(len(country_population), 2)
        self.assertEqual(country_population[0]['country__name'],'China')
        
        country = 'China'
        city = list(City.objects.filter(country__name=country).order_by('-population').values()[:5])

        self.assertEqual(len(city), 4)
        self.assertEqual(city[0]['name'],'Shanghai')

    def test_subtask2(self):
        j = Job()
        j.submit()
        self.assertTrue(j.id >= 0)

        x = threading.Thread(target=check_job_until_completed, args=(j,))
        x.start()
        
        self.assertIn(j.status, ['submitted','running','completed'])
        while(jobs(j.id).status!='completed'):
        	continue
        self.assertEqual(j.status,'completed')


