 # -*- coding: utf-8 -*-

from glob import glob
import os.path
import datetime
import os
import subprocess as sub
#import parser

def full_path(fl):
	return os.path.abspath(fl)

def get_only_errors(file_name):
	cmd = [full_path('parseone'), full_path(file_name)]
	p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
	output, errors = p.communicate()
	return output


class LazyReader(object):
	
	def __init__(self, file_name):
		self.data = list(get_only_errors(file_name))
		self.data.reverse()

	def get_ch(self):
		if not self.data:
			return None
		return self.data.pop()

	def look_up(self):
		if not self.data:
			return None
		return self.data[-1]

	def is_end(self):
		return bool(not self.data)

	def drop_to_symbol(self, symbol):
		while self.data:
			char = self.get_ch()
			if char == symbol:
				return		


def append_if_not_empty(collection,string):
    if len(string)==0:
    	return
    if not string.strip():
        return
    collection.append(string)


def read_str(reader):
	string_buffer = ''
	while True:
		char = reader.get_ch()
		if char == None:
			raise EOFError("Unexpected end of file")
		elif char=='"':
			if reader.look_up()=='"':
				string_buffer += '""'
				reader.get_ch()
			else:
				return string_buffer
		else:
			string_buffer += char


def read_entry(reader):
	result = []
	string_buffer = ''
	while True:
		char = reader.get_ch()
		if char == None:
			raise EOFError("Unexpected end of file")
			#append_if_not_empty(result,string_buffer)
			#return result
		elif char == ',':
			append_if_not_empty(result,string_buffer)
			string_buffer = ''
		elif char.isspace():
			pass
		elif char == '{':
			append_if_not_empty(result,string_buffer)
			string_buffer = ''
			result.append(read_entry(reader))
		elif char == '}':
			append_if_not_empty(result,string_buffer)
			return result
		elif char == '"':
			append_if_not_empty(result,string_buffer)
			string_buffer = ''
			append_if_not_empty(result,read_str(reader))
		else:
			string_buffer += char


def read_file(file_name):
	reader = LazyReader(file_name)
	#rez = []
	while True:
		reader.drop_to_symbol('{')
		if reader.is_end():
			return
		#rez.append(read_entry(reader))
		yield read_entry(reader)


def hist(list_par):
	rez = {}
	for el in list_par:
		rez[el] = rez.get(el,0)+1
	return rez


class Dictionary(object):
	"""docstring for Dictionary"""
	def __init__(self, file_name):
		super(Dictionary, self).__init__()
		self.users = {}
		self.apps = {}
		self.events = {}
		self.seps = {}

		#for entry in read_file(LazyReader(file_name)):
		for entry in read_file(file_name):
			if entry[0] == '1': #пользователь
				if len(entry) < 4:
					self.users[entry[2]] = ""
				else:	
					self.users[entry[3]] = entry[2].decode('utf')
			elif entry[0] == '3': #приложение
				self.apps[entry[2]] = entry[1].decode('utf')
			elif entry[0] == '4': #событие
				self.events[entry[2]] = entry[1].decode('utf')
			elif entry[0] == '10' and entry[2] == '2': #разделитель
				self.seps[entry[3]] = entry[1][1]
			else:
				pass

'''
import sys
a = list(read_file(sys.argv[1]))
print len(a)
'''


