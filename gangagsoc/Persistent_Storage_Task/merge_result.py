import os

#custom merge function, reads input files, sums up numbers, prints to another file
def mergefiles(file_list,output_file):    	
    #f_out = open(output_file,'w')
    f_out = open("job_output.txt",'w')
    sum = 0
    for f in file_list:
        f_in = open(f,'r')
        num = int(f_in.read())
        sum += num
        f_in.close()
    f_out.write(str(sum))
    f_out.close()
    return True