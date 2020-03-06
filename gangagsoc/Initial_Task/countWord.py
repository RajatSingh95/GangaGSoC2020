from PyPDF2 import PdfFileWriter, PdfFileReader
import ganga.ganga
from ganga import *
import os
import time

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

def check_job_until_completed(j):
	from GangaCore.GPIDev.Base.Proxy import stripProxy
	j = stripProxy(j)
	if j.master is not None:
		j = j.master
	    
	from time import sleep
	from GangaCore.Core import monitoring_component
	from GangaCore.Core.GangaRepository import getRegistryProxy

	jobs = getRegistryProxy('jobs')

	timeout = 60
	sleep_period = 1
	current_status = None
	state = 'completed'
	break_states = None
	verbose = True
	while j.status != state and timeout > 0:
		if not monitoring_component.isEnabled():
			monitoring_component.runMonitoring(jobs=jobs.select(j.id,j.id))
		else:
			monitoring_component.alive = True
			monitoring_component.enabled = True
			monitoring_component.steps = -1
			monitoring_component.__updateTimeStamp = 0
			monitoring_component.__sleepCounter = -0.5
		if verbose and j.status != current_status:
			print("Job %s: status = %s" % (str(j.id), str(j.status)))
		if current_status is None:
			current_status = j.status
		if type(break_states) == type([]) and j.status in break_states:
			print("Job finished with status: %s" % j.status )
			break
		sleep(sleep_period)
		timeout -= sleep_period
	return True