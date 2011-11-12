from django.db import models
from django.utils.translation import ugettext as _
from apps.categories.managers import CategoryManager

   
   
class Category(models.Model):
    """
        Model for Category of materials.
    """
    label      = models.CharField(_('Label'), max_length=32)
    parent     = models.ForeignKey('self', verbose_name=_('Parent Category'),
                                    null=True, blank=True, related_name='children')
    
    objects     = CategoryManager()
    
    class Meta:
        app_label           = 'categories'
        verbose_name        = _('Category')
        verbose_name_plural = _('Categories')
        
    def __unicode__(self):
        return self.label