# -*- coding: utf-8 -*-
#
# src/Kommonz/utils/encoding.py
# created by giginet on 2011/11/26
#

ENCODES = (
    'UNKNOWN',
    'ASCII',
    'SJIS', 
    'EUC',
    'JIS', 
    'UTF8', 
    'UTF16_LE', 
    'UTF16_BE', 
    'ERROR'
)

def to_utf8(text):
    import pykf
    encoding = pykf.guess(text)
    for enc_name in ENCODES:
        enc = getattr(pykf, enc_name)
        if enc == encoding:
            return unicode(text, enc_name.lower()).encode('utf8')
