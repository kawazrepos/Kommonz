from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext

import fields
from types import CreativeCommons

class CreativeCommonsField(models.Field):
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        if 'hidden' in kwargs:
            self.hidden = kwargs.pop('hidden')
        else:
            self.hidden = False
        if 'query_field_id' in kwargs:
            self.query_field_id = kwargs.pop('query_field_id')
        else:
            self.query_field_id = ''
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['help_text']  = kwargs.get('help_text', u"")
        super(CreativeCommonsField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        if isinstance(value, CreativeCommons):
            return value
        elif not value:
            return ''
        return CreativeCommons.parse(value)
    
    def get_db_prep_value(self, value):
        return super(CreativeCommons, self).get_db_prep_value(str(value))
        
    def get_internal_type(self):
        return 'CharField'
    
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.CreativeCommonsField, 'query_field_id': self.query_field_id}
        defaults.update(kwargs)
        return super(CreativeCommonsField, self).formfield(**defaults)
    
    def contribute_to_class(self, cls, name):
        super(CreativeCommonsField, self).contribute_to_class(cls, name)
