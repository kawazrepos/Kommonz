# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/28
# Modifier:      giginet
#
import mimetypes
from ..models import Material

IMAGE = (
    'image/bmp',
    'image/x-ms-bmp',
    'image/jpeg',
    'image/png',
    'image/gif',
)
AUDIO = (
    'audio/midi',
    'audio/mpeg',
    'audio/x-wav',
    'application/x-ogg',
)
MOVIE = (
    'video/mp4',
    'video/mpeg',
    'video/x-ms-wmv',
    'video/x-msvideo',
    'video/x-flv',
)
PACKAGE = (
    'application/x-bzip2',
    'application/x-gtar',
    'application/x-gzip',
    'application/x-lzh',
    'application/x-tar',
    'application/zip',
)
TEXT = (
    'application/atom+xml',
    'application/msword',
    'application/pdf',
    'application/rdf+xml',
    'application/rss+xml',
    'application/x-latex',
    'application/x-tex',    
)
CODE = (
    'application/xhtml+xml',
    'text/css',
    'text/html',
    'text/plain',
    'text/richtext',
    'text/rtf',
    'text/x-scalar',
    'text/x-cpp',
    'text/x-csharp',
    'text/css',
    'text/x-ruby',
    'text/x-perl',
    'text/x-python',
    'application/x-wais-source'
)
APPLICATION = (
    'application/octet-stream',
    'application/x-csh',
    'application/x-httpd-cgi',
    'application/x-javascript',
    'application/x-sh',
)
TYPES = (
    ('image',       IMAGE),
    ('audio',       AUDIO),
    ('movie',       MOVIE),
    ('text',        TEXT),
    ('package',     PACKAGE),
    ('application', APPLICATION),
    ('code',        CODE)
)
def guess(filename):
    mimetypes.init()
    try:
        type = mimetypes.guess_type(filename)[0]
    except:
        # Fail silently
        type = None
    if type is None:
        return 'unknown'
    for label, types in TYPES:
        if type in types:
            return label
    return 'unknown'

def get_file_model(filename):
    """
    Return suitable class for file
    """
    import os
    type = guess(filename)
    if not type or type == 'unknown':
        return Material
    cls_name = type[0].upper() + type[1:] #convert from 'type' to 'Type'
    try:
        module = __import__('.'.join(('Kommonz', 'apps', 'materials', '%ss' % type, 'models')), globals(), locals(), [cls_name])
        return getattr(module, cls_name)
    except:
        return Material

