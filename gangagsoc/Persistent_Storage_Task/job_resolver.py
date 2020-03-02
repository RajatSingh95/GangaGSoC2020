import json

import ganga.ganga
from ganga import *
import os
import time,re,ast

def check_type(attr_value):
	if re.match(r'^[\[]', attr_value):
		#print("Sequence")
		return "Sequence"

	elif re.match(r'^True', attr_value) or re.match(r'^False', attr_value) or re.match(r'^None', attr_value):
		#print("Bool or None")
		return "Bool or None"
	elif re.match(r'^[A-Za-z]+', attr_value) :
	 	#print("Node")
	 	return "Node"
	elif re.match(r'^\'', attr_value) or re.match(r'^\"', attr_value):
		#print("String")
		return "String"
	elif re.match(r'^{', attr_value):
		#print("Dictionary")
		return "Dictionary"
	elif re.match(r'^[0-9]+', attr_value):
		#print("Number")
		return "Number"
	else:
		#print("Some Error")
		return "Some Error"

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
	return attr_value.strip('\'')

def int_resolver(attr_value):
	try:
		return int(attr_value.strip())
	except:
		return attr_value.strip()



def sequence_resolver(attr_value):
	attr_value=attr_value[1:len(attr_value)-1]
	
	attr_value=attr_value.strip()
	
	if re.match(r'^[A-Za-z]', attr_value):
		all_elem = attr_value.split('),')
		final_list = []
		for ele in all_elem:
			try:
				class_name = re.findall(r'[A-z]+ \(',ele)[0].replace(' (','')
				ele = ele.replace(class_name+' (','')
				attribute = [a.strip() for a in ele.split(',' )]
				obj = getattr(sys.modules[__name__], class_name)()
				for key in attribute:
					key = [a.strip() for a in key.split(' = ')]
					
					setattr(obj, key[0], key[1].strip('\''))
				final_list.append(obj)
				

			except:
				#print("#######error######")
				continue
		return final_list

	elif re.match(r'^\'', attr_value):
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
		return final_list

	elif re.match(r'^\[', attr_value):
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
		return final_list
	else:
		return []

def node_resolver(attr_value,subattr_mem=['#']):
	if subattr_mem[0]=='#':
		class_name = re.findall(r'[A-z]+\(',attr_value)[0].replace('(','')
		obj = getattr(sys.modules[__name__], class_name)()
		attr_value = attr_value.strip()
		attr_value = attr_value.replace(class_name+'(','')
		attr_value = attr_value[0:len(attr_value)-1]
		attr_value = attr_value.strip()
		subattr_list = [a.strip() for a in attr_value.split(',')]
		for sub_elem in subattr_list:
			key = [a.strip() for a in sub_elem.split('=')]
			setattr(obj, key[0], key[1].strip('\''))
		return obj	
	
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
	#print(subattr_list)
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
			setattr(obj, subattr_list[k], seq)
		
		elif check_type(atr_str)=="Bool or None":
			seq = bool_none_resolver(atr_str)
			setattr(obj, subattr_list[k], seq)

		elif check_type(atr_str)=="Node":
			seq = node_resolver(atr_str)
			setattr(obj, subattr_list[k], seq)
		elif check_type(atr_str)=="Dictionary":
			seq = dict_resolver(atr_str)
			setattr(obj, subattr_list[k], seq)
		
		elif check_type(atr_str)=="String":
			seq = string_resolver(atr_str)
			setattr(obj, subattr_list[k], seq)
		elif check_type(atr_str)=="Number":
			seq = int_resolver(atr_str)
			setattr(obj, subattr_list[k], seq)
	return obj

