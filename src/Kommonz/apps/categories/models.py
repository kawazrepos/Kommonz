from django.db import models
from django.utils.translation import ugettext as _
from managers import CategoryManager
   
   
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
        unique_together = (('label', 'parent'),)
        
    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('categories_category_detail', (), { 'pk' : self.pk })