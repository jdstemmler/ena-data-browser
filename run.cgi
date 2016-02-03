#!/home/disk/eos1/jstemm/nobackup/mini/envs/ena/bin/python
from wsgiref.handlers import CGIHandler
from ena_app import app

CGIHandler().run(app)