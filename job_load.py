import ganga.ganga
from ganga import *
from GangaCore.GPIDev.Base.Proxy import *
import json
import re,ast
def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)  
    return d

def full_print(obj, out=None, interactive=False):
    """Print the full contents of a GPI object without abbreviation."""
    
    from io import StringIO
    import sys
    if out is None:
        out = sys.stdout

    from GangaCore.GPIDev.Lib.GangaList.GangaList import GangaList

    _obj = stripProxy(obj)

    if isType(_obj, GangaList):
        obj_len = len(_obj)
        if obj_len == 0:
            print('[]', end=' ', file=out)
        else:
            outString = '['
            outStringList = []
            for x in _obj:
                if isType(x, GangaObject):
                    sio = StringIO()
                    stripProxy(x).printTree(sio, interactive)
                    result = sio.getvalue()
                    # remove trailing whitespace and newlines
                    outStringList.append(result.rstrip())
                else:
                    # remove trailing whitespace and newlines
                    outStringList.append(str(x).rstrip())
            outString += ', '.join(outStringList)
            outString += ']'
            print(outString, end=' ', file=out)
        return

    if isProxy(obj) and isinstance(_obj, GangaObject):
        sio = StringIO()
        runProxyMethod(obj, 'printTree', sio, interactive)
        print("##########",type(sio.getvalue()))
        return sio.getvalue()
        #from ast import literal_eval
        #l = literal_eval(sio.getvalue())
        
        l = sio.getvalue()
        print(l.count('\n'))
        #print(sio.getvalue(), end=' ', file=out)
    else:
        print(str(_obj), end=' ', file=out)



def sequence_resolver(attr_value):
	#attr_value= attr_value[:len(attr_value)-1] + attr_value[len(attr_value)-1 + 1:]
	print("!!!!!",attr_value[0],attr_value[len(attr_value)-1])
	attr_value=attr_value[1:len(attr_value)-1]
	print("&&&&",attr_value)
	attr_value=attr_value.strip()
	
	if re.match(r'^[A-Za-z]', attr_value):
		print("Node")
		all_elem = attr_value.split('),')
		print(all_elem)
		final_list = []
		for ele in all_elem:
			try:
				class_name = re.findall(r'[A-z]+ \(',ele)[0].replace(' (','')
				ele = ele.replace(class_name+' (','')
				attribute = [a.strip() for a in ele.split(',' )]
				obj = getattr(sys.modules[__name__], class_name)()
				print(class_name,obj,attribute)
				for key in attribute:
					key = [a.strip() for a in key.split(' = ')]
					print(key[0])
					setattr(obj, key[0], key[1].strip('\''))
				final_list.append(obj)
				print(class_name,obj.namePattern)

			except:
				#print("#######error######")
				continue
		return final_list

	elif re.match(r'^\'', attr_value):
		print("String seq")
		all_elem = attr_value.split(',')
		#print(all_elem)
		final_list = []
		for ele in all_elem:
			try:
				if ele:
					final_list.append(ele.strip())
			except:
				#print("#######error######")
				continue
		print(final_list)
		return final_list

	elif re.match(r'^\[', attr_value):
		print("Sequence of seq",attr_value)
		all_elem = attr_value.split(',')
		final_list = []
		for ele in all_elem:
			ele = ele.strip()
			try:
				ele = [a.strip('\'') for a in ele.strip('][').split(', ')]
				if ele:
					final_list.append(ele)
			except:
				#print("#######error######")
				continue
		print(final_list)
		return final_list
	else:
		return []

def node_resolver(attr_value,subattr_mem):
	att_index = {}
	for subatr in subattr_mem:
		index = job_str.find(subatr+' ')
		if index>=0:
			att_index[subatr]=index
	final_atr = {k: v for k, v in sorted(att_index.items(), key=lambda item: item[1])}
	subattr_list = []
	for key_order in final_atr:
		subattr_list.append(key_order)
	class_name = re.findall(r'[A-z]+ \(',attr_value)[0].replace(' (','')
	obj = getattr(sys.modules[__name__], class_name)()
	print(subattr_list)
	for k in range(0,len(subattr_list)):
		attr_value = attr_value.strip()
		if k < len(subattr_list)-1:
			start = attr_value.find(subattr_list[k])
			last = attr_value.find(subattr_list[k+1])
			atr_str = attr_value[start:last].replace(subattr_list[k]+' =','')
			atr_str = atr_str.strip()
			atr_str = atr_str[0:len(atr_str)-1]
			atr_str = atr_str.strip()
		else:
			start = attr_value.find(subattr_list[k])
			last = len(attr_value)
			atr_str = attr_value[start:last].replace(subattr_list[k]+' =','')
			atr_str = atr_str.strip()
			atr_str = atr_str[0:len(atr_str)-1]
			atr_str = atr_str.strip()

		if check_type(atr_str) == "Sequence":			
			seq = sequence_resolver(atr_str)
			print("Node Sequence ## ",atr_str)
			setattr(obj, subattr_list[k], seq)
		elif check_type(attr_value)=="Dictionary":
			seq = dict_resolver(attr_value)
			setattr(obj, subattr_list[k], seq)
		elif check_type(attr_value)=="Bool or None":
			seq = bool_none_resolver(attr_value)
			setattr(obj, subattr_list[k], seq)
		elif check_type(attr_value)=="String":
			seq = string_resolver(attr_value)
			setattr(obj, subattr_list[k], seq)
		elif check_type(attr_value)=="Number":
			seq = int_resolver(attr_value)
			setattr(obj, subattr_list[k], seq)
	
	return obj
def dict_resolver(attr_value):
	return ast.literal_eval(attr_value)

def bool_none_resolver(attr_value):
	if attr_value.strip() == "True":
		return True
	elif attr_value.strip() == "False":
		return False
	else:
		return None

def string_resolver(attr_value):
	return attr_value.strip()

def int_resolver(attr_value):
	try:
		return int(attr_value.strip())
	except:
		return attr_value.strip()

def check_type(attr_value):
	if re.match(r'^[\[]', attr_value):
		print("Sequence")
		return "Sequence"

	elif re.match(r'^True', attr_value) or re.match(r'^False', attr_value) or re.match(r'^None', attr_value):
		print("Bool or None")
		return "Bool or None"
	elif re.match(r'^[A-Za-z]+', attr_value):
	 	print("Node")
	 	return "Node"
	elif re.match(r'^\'', attr_value) or re.match(r'^\"', attr_value):
		print("String")
		return "String"
	elif re.match(r'^{', attr_value):
		print("Dictionary")
		return "Dictionary"
	elif re.match(r'^[0-9]+', attr_value):
		print("Number")
		return "Number"
	else:
		print("Some Error")
		return "Some Error"




j1 = Job()
j1.inputfiles = ['1','2','3','1','2']
j1.splitter = ArgSplitter(args=[['1'],['2']])
j1.postprocessors.append(CustomMerger(module='setup.py',files=['output.txt']))
import inspect,sys
attr = inspect.getmembers(j1)

attr = [a for a in attr if not(a[0].startswith('__') and a[0].endswith('__')) and not(a[0].startswith('_'))]

subattr_mem = {}
for subattr in attr:
		
		temp = inspect.getmembers(subattr[1])
		#print(temp)
		temp = [a[0] for a in temp if not(a[0].startswith('__') and a[0].endswith('__')) and not(a[0].startswith('_'))]
		subattr_mem[subattr[0]] = temp
		

attr_list = [a[0] for a in attr if not(a[0].startswith('__') and a[0].endswith('__')) and not(a[0].startswith('_'))]






#print(str(j1))
job_str  = full_print(j1)

print(job_str)
att_index = {}
for atr in attr_list:
	index = job_str.find(atr+' ')
	if index>=0:
		att_index[atr]=index

final_atr = {k: v for k, v in sorted(att_index.items(), key=lambda item: item[1])}
attr_list = []
for key_order in final_atr:
	attr_list.append(key_order) 

#print(job_str)
job_str = job_str.strip()

j = Job()
for i in range(0,len(attr_list)):
	
	if i < len(attr_list)-1:
		start = job_str.find(attr_list[i])
		last = job_str.find(attr_list[i+1])
		#print(job_str[start:last].replace(attr_list[i]+' =',''))
		attr_value = job_str[start:last].replace(attr_list[i]+' =','')
		attr_value = attr_value.strip()
	#print(attr_value)
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
			if attr_list[i]=="inputfiles":
				print("sssssssss")

			seq = sequence_resolver(attr_value)
			
			setattr(j, attr_list[i] , seq)
		elif check_type(attr_value)=="Node":
			if attr_list[i]=="postprocessors":
				print(attr_value)
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
	except:
		continue

# loc = getattr(sys.modules[__name__], 'LocalFile')()
# setattr(loc,'namePattern','1.txt')
# #loc = ['1.txt','2.txt']
# setattr(j,'inputfiles',[loc])
print(j)