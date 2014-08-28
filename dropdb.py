#!/usr/bin/env python

"""Drop all databases."""

from models import db

db.drop_all()
