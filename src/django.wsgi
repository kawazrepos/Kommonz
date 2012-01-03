# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/30
#
import os, sys

# Activate virtualenv
virtualenv = os.path.join(os.path.dirname(__file__), '../env')
if os.path.exists(virtualenv):
    activate_this = os.path.join(virtualenv, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

# Append Kawaz to the PYTHONPATH
path_list = [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'Kommonz'),
]
for path in path_list:
    if path not in sys.path:
        sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Kommonz.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
