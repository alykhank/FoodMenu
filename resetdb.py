#!/usr/bin/env python

"""Reset database."""

from models import db

db.drop_all()
db.create_all()
