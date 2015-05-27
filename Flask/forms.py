# -*- coding: utf8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class AppSearch(Form):
    app = TextField('app')    