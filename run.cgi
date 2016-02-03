#!/usr/bin/env python
from wsgiref.handlers import CGIHandler
from ena_app import app

CGIHandler().run(app)