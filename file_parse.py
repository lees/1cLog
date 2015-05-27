 # -*- coding: utf-8 -*-

from glob import glob
import os.path
import datetime
import parser

class LazyReader(object):
	
	def __init__(self, file_name):
		super(LazyReader, self).__init__()
		self.file = open(file_name)
		self.data = ''
		self.data_len = 0
		self.pos = 0
		self.is_end = False
		self.read_chunk()


	def read_chunk(self,size = 1024):
		self.pos = 0
		self.data = self.file.read(size)
		self.data_len = len(self.data)
		if not self.data:
			self.is_end = True

	def get_ch(self):
		if self.is_end:
			return None
		rez = self.data[self.pos]
		self.pos += 1
		if self.pos == self.data_len:
			self.read_chunk()
		return rez

	def look_up(self):
		if self.pos == len(self.data):
			self.is_end = True
			return None
		return self.data[self.pos]

	def drop_to_symbol(self, symbol):
		while not self.is_end:
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
		if reader.is_end:
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
file_list = glob('1/*.lgp')
reader = LazyReader(file_list[2])
a = read_file(reader)
aa = filter(lambda x: x[8]=='E', a)
b = hist(map(len,aa))
'''


'''
file_list = glob('1/*.lgf')
dic = Dictionary(file_list[0])
'''





