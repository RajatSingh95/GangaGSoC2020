# Author : Rajat Singh
# Script to count 'the' word in a pdf by creating subjobs


from PyPDF2 import PdfFileWriter, PdfFileReader
# import ganga.ganga
# from ganga import *
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
	job.submit()
	status = job.status
	while status!='completed':
		status = job.status

	for i in range(len(page_list)):
		filename = page_list[i][0] + '.pdf'
		os.remove(filename)



count_word_from_pdf("CERN.pdf")
#print(count_job)
exit()