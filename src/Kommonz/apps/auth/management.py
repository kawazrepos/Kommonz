# -*- coding: utf-8 -*- #
# src/Kommonz/apps/auth/management.py
# created by giginet on 2011/11/16
#
from django.db.models.signals import post_syncdb
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth import models as User
from models import USER_ICON_PATH

@receiver(post_syncdb)
def clean_up_storage(sender, app, created_models, verbosity, interactive, **kwargs):
    if not settings.DEBUG or not interactive or not User == sender: return
    try:
        import os
        import shutil
        shutil.rmtree(os.path.join(settings.STATICFILES_DIRS[0], USER_ICON_PATH))
    except:
        pass
