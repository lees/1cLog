import db
import sys
from glob import glob

bases = {}
sess = db.get_session()

def findBase(base_name):

	base_id = bases.get(base_name, None)
	if not base_id is None:
		return base_id

	base = sess.query(db.Bases).filter_by(name = base_name).first()
	if not base is None:
		bases[base_name] = base.id
		#sess.close()
		return base.id

	base = db.Bases(name = base_name)
	sess.add(base)
	sess.commit()
	base_id = base.id
	return base_id


def load_chunk(chunk):
	loaded = 0

	if len(chunk) == 0:
		return 0

	apps = sess.query(db.Applications).filter(db.Applications.id.in_(chunk.keys())).all()

	for app in apps:
		if chunk[app.id] == app.baseId:
			del chunk[app.id]
		else:
			app.baseId == chunk[app.id]
			sess.add(app)
			del chunk[app.id]
			loaded += 1

	for key in chunk:
		app = db.Applications(id = key, baseId = chunk[key])
		sess.add(app)
		loaded += 1

	sess.commit()
	return loaded


def load(filename):
	count = 1
	loaded = 0
	lines = file(filename).readlines()
	lines_len = len(lines)
	chunk = {}
	for line in lines:
		vals = line.split('\t')
		if len(vals) != 2:
			print 'Bad line ',count,': ', line
			count += 1
			continue

		app_id = int(vals[0])
		base_id = findBase(vals[1].strip())

		count += 1
		chunk[app_id] = base_id

		if count % 300 == 0:
			print count,'/',lines_len
			loaded += load_chunk(chunk)
			chunk = {}

	loaded += load_chunk(chunk)


	print 'Loaded ',loaded,'apps from ', count



def main():
	if len(sys.argv[1]) < 2:
		print 'Usage: load_apps.py <apps_file>'
	else:
		load(sys.argv[1])

if __name__ == '__main__':
	main()