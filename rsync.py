import sys
from glob import glob
from os.path import basename
from shutil import copy

import db

sess = db.get_session()

def rsync(from_path, to_path):

	if from_path is None or len(from_path)==0:
		print "Empty from path"
		return
	
	if to_path is None or len(to_path)==0:
		print "Empty to path"
		return
	
	exist = glob(to_path+r'\*.lgp')
	exist.sort()

	if len(exist) < 1:
		print "Wrong to path: ", to_path
		return
	
	new = glob(from_path+r'\*.lgp')
	new.sort()
	
	if len(new) < 1:
		print "Wrong from path: ", from_path
		return

	filter_function = lambda x : basename(x) >= basename(exist[-1])
	to_copy = filter(filter_function,new)
	to_copy.append(from_path+'\\1Cv8.lgf')

	for filename in to_copy:
		print "copying %s" % (basename(filename))
		copy(filename,to_path)

def find_and_rsync(base_name):		
	base = sess.query(db.Bases).filter_by(name = base_name).first() 
	if base is None:
		print "Invalid base name ", base_name
		return
	rsync(base.LogNet,base.LogLocal)

param = sys.argv[1]

if param == 'all':
	for base in sess.query(db.Bases).all():
		print "Started ", base.name
		find_and_rsync(base.name)
		print ""
else:
	find_and_rsync(param)
