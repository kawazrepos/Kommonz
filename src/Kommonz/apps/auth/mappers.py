from bpmappers import NonKeyField
from bpmappers.djangomodel import ModelMapper
from models import UserProfile
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'


class UserProfileMapper(ModelMapper):
    url = NonKeyField()
    
    def filter_url(self):
        return self.data.get_absolute_url()
    
    class Meta:
        model  = UserProfile
        fields = ('pk', 'user', 'nickname', 'icon',)