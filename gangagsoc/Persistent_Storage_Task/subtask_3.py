import mysql.connector
import json

import ganga.ganga
from ganga import *
import os
import time,re,ast
from gangagsoc.Initial_Task.countWord import check_job_until_completed
from gangagsoc.Persistent_Storage_Task.job_resolver import *

mydb = mysql.connector.connect(
  host="localhost",
  user="ganga",
  passwd='Ganga_2020',
  database="job"
)
mycursor = mydb.cursor()

def recreate_job():

	db_read_start = time.time()
	mycursor.execute("SELECT * from data ORDER BY id DESC LIMIT 1")
	last_inserted_job = mycursor.fetchall()

	for x in last_inserted_job:
		try:
			job_str = x[2].decode('utf-8')
			subattr_mem = json.loads(x[1].decode('utf-8'))
		except:
			job_str = x[2]
			subattr_mem = json.loads(x[1])
		break
	attr_list = subattr_mem['main_attribute_list']
	job_str = job_str.strip()
	
	db_read_finish = time.time()
	# reading the job from database finish

	# recreating the Job from string starts
	job_create_start = time.time()
	j = Job()
	for i in range(0,len(attr_list)):
		if i < len(attr_list)-1:
			start = job_str.find(attr_list[i])
			last = job_str.find(attr_list[i+1])
			#print(job_str[start:last].replace(attr_list[i]+' =',''))
			attr_value = job_str[start:last].replace(attr_list[i]+' =','')
			attr_value = attr_value.strip()
		else:
			start = job_str.find(attr_list[i])
			last = len(job_str)-1
			attr_value = job_str[start:last].replace(attr_list[i]+' =','')
			attr_value = attr_value[0:len(attr_value)-1]
			attr_value = attr_value.strip()

		attrval_len = len(attr_value)
		if attr_value[attrval_len-1]==',':
			attr_value = attr_value.strip()[0:attrval_len-1]
		try:
			if check_type(attr_value)=="Sequence":
				seq = sequence_resolver(attr_value)
				setattr(j, attr_list[i] , seq)
			elif check_type(attr_value)=="Node":
				seq = node_resolver(attr_value,subattr_mem[attr_list[i]])
				setattr(j, attr_list[i] , seq)
			elif check_type(attr_value)=="Dictionary":
				seq = dict_resolver(attr_value)
				setattr(j, attr_list[i] , seq)
			elif check_type(attr_value)=="Bool or None":
				seq = bool_none_resolver(attr_value)
				setattr(j, attr_list[i] , seq)
			elif check_type(attr_value)=="String":
				seq = string_resolver(attr_value)
				setattr(j, attr_list[i] , seq)
			elif check_type(attr_value)=="Number":
				seq = int_resolver(attr_value)
				setattr(j, attr_list[i] , seq)
		except Exception as e:
			#print("error",str(e))
			continue
	job_create_finish = time.time()
	# recreating the Job from string finish
	return (db_read_finish-db_read_start),(job_create_finish-job_create_start)



## reading from database and recreating job starts
experiment_start = time.time()
num_iter = 1000
for test_num in range(0,num_iter):
	# evaluation starts
	read_time,create_time=recreate_job()
experiment_finish = time.time()
		
print("-------Ran ",num_iter,"iterations: took ",experiment_finish-experiment_start,"seconds-----------")
print("-------Performance: ",(experiment_finish-experiment_start)/1000,'seconds-----------\n' )

## experiment for one iteration
read_time,create_time = recreate_job()
print('-------Time for reading a Job string blob from db:',read_time,' seconds------')
print('-------Time for creating a Job object:',create_time,' seconds-------')
