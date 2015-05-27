import tornado.web
import tornado.httpserver
import db
import simplejson as json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class EventsHandler(tornado.web.RequestHandler):
    def get(self,app_id):
    	sess = db.get_session()
    	events = []
    	for event in sess.query(db.Events).filter_by(applicationId = app_id).order_by(db.Events.time.desc()).all()[:50]:
            rez = event.__dict__
            del rez['_sa_instance_state']
            rez['time'] = rez['time'].isoformat()
            #rez['comment'] = rez['comment'].decode('utf-8')
            #rez = str(rez)
            #rez['comment'] = rez['comment'].replace('\n','</p><p>')
            rez['commentlines'] = rez['comment'].splitlines()
            events.append(rez)
        self.write(json.dumps(events))


class ApplicationsHandler(tornado.web.RequestHandler):
    def get(self,app_id):
    	sess = db.get_session()
    	db_app = sess.query(db.Applications).filter_by(id = app_id).first()
    	if not db_app is None:
        	app_view = {'id':str(db_app.id), 'base':str(db_app.base.name)}
    	else:
        	app_view = None
        self.write(json.dumps(app_view))



application = tornado.web.Application([
        (r"/json/", MainHandler),
        (r"/json/Applications/([0-9]+)", ApplicationsHandler),
        (r"/json/Events/([0-9]+)", EventsHandler)
    ])
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen("5001")
tornado.ioloop.IOLoop.current().start()