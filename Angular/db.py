from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from datetime import datetime

engine = create_engine('sqlite:///Logs.dat', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Bases(Base):
	__tablename__ = 'bases'
	id = Column(Integer, primary_key=True)
	name = Column(String(256))
	LogNet = Column(String(500))
	LogLocal = Column(String(500))
	apps = relationship("Applications", backref='base', lazy = 'dynamic')

	def __repr__(self):
		return str(self.name)
 
 	def last_event(self):
 		sess = get_session()
 		apps_id = map(lambda x: x.id,self.apps.all())
 		curr_date = datetime(2015,03,16)
 		chunk_size = 800
 		while len(apps_id) > 0:
 			chunk, apps_id = apps_id[:chunk_size], apps_id[chunk_size:]
 			event = sess.query(Events).filter(Events.time>curr_date).\
										filter(Events.applicationId.in_(chunk)).\
										order_by(Events.time.desc()).first()
	 		if not event is None:
	 			curr_date = max(curr_date, event.time)
	 	return curr_date

	def last_event1(self):
		sess = get_session()

		curr_date = datetime(2015,03,16)
		event = sess.query(Events,Applications,Bases).\
				filter(Applications.baseId == id).\
				filter(Applications.id==Events.applicationId).\
				order_by(Events.time.desc()).first()
		if not event is None:
			curr_date = max(curr_date, event.time)
		return curr_date


class Applications(Base):
	__tablename__ = 'applications'
	id = Column(Integer, primary_key=True)
	baseId = Column(Integer, ForeignKey('bases.id'))

	def __repr__(self):
		return str((self.id, self.base))

class Events(Base):
	__tablename__ = 'events'
	id = Column(Integer, primary_key=True)
	time = Column(DateTime)
	user = Column(String(50))
	connection_kind = Column(String(20))
	connectionId = Column(Integer)
	event = Column(String(256))
	kind = Column(String(1))
	comment = Column(Text)
	sessionId = Column(Integer)
	applicationId = Column(Integer, ForeignKey('applications.id'), index = True)

def update_scheme():
	Base.metadata.create_all(engine)

def get_session():
	return Session()	

if __name__ == '__main__':
	update_scheme()
	
