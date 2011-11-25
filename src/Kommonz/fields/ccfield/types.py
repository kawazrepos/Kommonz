# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

class CreativeCommons(object):
    @classmethod
    def perse(cls, value):
        """
            generate CreativeCommons from 'Noncommerical,No Derivative,Share Alike' format.
            ex '1,0,0' => 'CC BY-NC' 
        """
        nc, nd, sa = [i is '1' for i in value.split(',')]
        return cls(nc, nd, sa)
    
    def __init__(self, nc=0, nd=0, sa=0):
        self.noncomerical  = nc
        self.no_derivative = nd
        self.share_alike   = sa
        
    def __str__(self):
        return self.__unicode__().encode('utf-8')
    
    def __unicode__(self):
        return self._get_commons_description()
    
    def _get_commons_description(self):
        nc, nd, sa = self.noncommerical, self.no_derivative, self.share_alike
        if not nd:
            return 'CC BY' if not nc else 'CC BY-NC'
        elif not nd and sa:
            return 'CC BY-SA' if not nc else 'CC-BY-NC-SA'
        elif nd:
            return 'CC BY-ND' if not nc else 'CC BY-NC-ND'