
import mysql.connector
import json

from PyPDF2 import PdfFileWriter, PdfFileReader
import ganga.ganga
from ganga import *
import os
import time
import inspect,sys
from job_load import full_print

# function to return job for counting 'the' word in a pdf file
def count_word_from_pdf(pdf_file,exe_file="count_word.sh",merge_file="merge_result.py"):
	os.system('chmod +x '+exe_file)
	os.system('chmod +x '+merge_file)
	
	#starts new job
	job = Job()

	#specifies executable to run on Grid
	job.application = Executable()
	job.application.exe = File(exe_file)

	#specifies the job backend
	job.backend = "Local"

	# splitting the whole pdf into pages
	inputpdf = PdfFileReader(open(pdf_file, "rb"))
	page_list = list()
	for i in range(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		with open("page%s.pdf" % i, "wb") as outputStream:
			output.write(outputStream)
		page_list.append(["page%s" % i])

	#Split job by changing the args attribute of the application.
	splitter = ArgSplitter(args=page_list)

	#creates list of file names
	filelist = []
	for i in range(len(page_list)):
		filename = page_list[i][0]
		filelist.append(LocalFile(filename+'.pdf'))


	# assigns input and ouput files 
	job.outputfiles = [LocalFile("job_output.txt")]
	job.inputfiles = filelist

	#assigns splitter to job application
	job.splitter = splitter

	# merges the result of all job-splits
	job.postprocessors.append(CustomMerger(module=merge_file,files=['job_output.txt'],overwrite=True))

	
	return job

# mysql-db instance
mydb = mysql.connector.connect(
  host="localhost",
  user="ganga",
  passwd='Ganga_2020',
  database="job"
)
mycursor = mydb.cursor()

#job instance
job = count_word_from_pdf("CERN.pdf")

# get attributes from the Job class
attr = inspect.getmembers(job)
attr = [a for a in attr if not(a[0].startswith('__') and a[0].endswith('__')) and not(a[0].startswith('_'))]

# storing the attribute values
subattr_mem = {}
for subattr in attr:		
		temp = inspect.getmembers(subattr[1])
		#print(temp)
		temp = [a[0] for a in temp if not(a[0].startswith('__') and a[0].endswith('__')) and not(a[0].startswith('_'))]
		subattr_mem[subattr[0]] = temp

attr_list = [a[0] for a in attr if not(a[0].startswith('__') and a[0].endswith('__')) and not(a[0].startswith('_'))]
job_str = full_print(job)
att_index = {}
for atr in attr_list:
	index = job_str.find(atr+' ')
	if index>=0:
		att_index[atr]=index

final_atr = {k: v for k, v in sorted(att_index.items(), key=lambda item: item[1])}
attr_list = []
for key_order in final_atr:
	attr_list.append(key_order) 

#main attribute list
subattr_mem['main_attribute_list']= attr_list

print("###### Write Job Blob to database #######")
attribute_blob = json.dumps(subattr_mem).encode('utf-8')
job_blob = job_str.encode('utf-8')

# writing the blob into table
sql = "INSERT INTO data (attributes, job_string_blob) VALUES (%s, %s)"
val = (attribute_blob, job_blob)

mycursor.execute(sql, val)

mydb.commit()
print("###### Writing Done #######")


print("\n###### Reading Job Blob from database #######")
# reading the blob from from table
mycursor.execute("SELECT * from data ORDER BY id DESC LIMIT 1")
last_inserted_job = mycursor.fetchall()

for x in last_inserted_job:
	try:
		print(x[2].decode('utf-8'))
	except:
		print(x[2])
print("###### Reading Done #######")