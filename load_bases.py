import db
from bases import bases

sess = db.get_session()

for key in bases.keys():
	base_info = bases[key]
	db_base = sess.query(db.Bases).filter_by(name = key).first()
	if db_base is None:
		db_base = db.Bases(name = key)
	db_base.LogNet = base_info['from']
	db_base.LogLocal = base_info['to']
	sess.add(db_base)
	sess.commit()

sess.close()