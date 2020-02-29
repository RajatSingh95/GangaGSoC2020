# Author : Rajat Singh
# Script to create Hello World Ganga Job


job = Job()
job.backend = "Local"
job.submit()

status = job.status
while status!='completed':
	status = job.status
job.peek('stdout','more')
exit()
