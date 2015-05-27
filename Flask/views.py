# -*- coding: utf8 -*-

from flask import render_template, flash, redirect, request
from app import app
import db
from forms import AppSearch

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    
    form = AppSearch()
    if form.validate_on_submit():
        return redirect('/application/'+form.app.data)
    
    return render_template("index.html",
        title = 'Home',
        form = form)




@app.route('/application/<app>', methods = ['GET', 'POST'])
def spamer(app):
    
    form = AppSearch()
    if form.validate_on_submit():
        return redirect('/application/'+form.app.data)

    sess = db.get_session()
    events = []
    for event in sess.query(db.Events).filter_by(applicationId = app).order_by(db.Events.time.desc()).all()[:50]:
        rez = event.__dict__
        events.append(rez)

    db_app = sess.query(db.Applications).filter_by(id = app).first()
    if not db_app is None:
        app_view = {'id':db_app.id, 'base':db_app.base.name}
    else:
        app_view = None
    sess.close()

    return render_template("events.html",
        title = 'Unsorted',
        form = form,
        app_view = app_view,
        is_partial = True,
        events = events)

