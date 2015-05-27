import db
import file_parse
import file_parse_go
from glob import glob
from datetime import datetime
from os.path import basename
import sys

sess = db.get_session()

def hour_start(dt):
	return datetime(dt.year,dt.month,dt.day,dt.hour)

def load_dir(base):
	
	dir_path = base.LogLocal
	if dir_path is None:
		return
	if len(dir_path)==0:
		return

	start_date = base.last_event()
	
	print datetime.now(),'| Loading from time : %s' % start_date

	dic_file = glob(dir_path+'/*.lgf')[0]
	print datetime.now(),'| Loading dictionary from: %s ...' % dic_file
	dic = file_parse.Dictionary(dic_file)
	print datetime.now(),'| Done'

	for event_file in sorted(glob(dir_path+'/*.lgp')):
		# TODO os.path.basename(event_file) need to be bigger than last loaded
		#events = file_parse.read_file(file_parse.LazyReader(event_file))
		event_file_time = datetime.strptime(basename(event_file)[:14], '%Y%m%d%H%M%S')

		if start_date and event_file_time < hour_start(start_date):
			continue

		applications = {}

		print datetime.now(),'| Loading log from: %s ...' % event_file
		events = file_parse_go.read_file(event_file)
		#events = file_parse.read_file(event_file)
		errors = filter(lambda x: x[8]=='E', events)
		for error in errors:
			dic_event = {}
			
			event_time = datetime.strptime(error[0],'%Y%m%d%H%M%S')
			if start_date and event_time < start_date:
				continue
			dic_event['time'] = datetime.strptime(error[0],'%Y%m%d%H%M%S')
			
			dic_event['user'] = dic.users.get(error[3],'')
			dic_event['connection_kind'] = dic.apps.get(error[5],'')
			dic_event['connectionId'] = error[6]
			dic_event['event'] = dic.events.get(error[7],'')
			dic_event['kind'] = error[8]
			dic_event['comment'] = error[9].decode('utf')
			dic_event['sessionId'] = error[-3]
			dic_event['applicationId'] = dic.seps.get(error[-1][-1],'') 

			sess.add(db.Events(**dic_event))

		sess.commit()
		print datetime.now(),'| Done'
		print ' '


def find_and_load(base_name):		
	base = sess.query(db.Bases).filter_by(name = base_name).first()
	if base is None:
		print "Invalid base name ", base_name
		return
	load_dir(base)

if __name__ == '__main__':
	param = sys.argv[1]
	print datetime.now(),'| Start'

	if param == 'all':
		for base in sess.query(db.Bases).all():
			print "Started ", base.name
			find_and_load(base.name)
			print ""
	else:
		find_and_load(param)

	print datetime.now(),'| End'


