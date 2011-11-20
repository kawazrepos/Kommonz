from django.db import models
from django.utils import simplejson
from django.utils.translation import ugettext as _
from managers import CategoryManager
from utils.views import JSONResponse

   
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
    
    def get_children_tree(self):
        def _get_dict(category):
            child_categories = {}
            for child in category.children.iterator():
                child_categories.update({child.label : _get_dict(child)})
            return child_categories
        result = _get_dict(self)
        return result
        
    def get_children_json(self):
        tree_dict = self.get_children_tree()
        return simplejson.dumps(tree_dict)
    
    def get_root_category(self):
        def _get_root(category):
            if category.parent:
                self.get_root_category(category.parent)
            else:
                return category
        return _get_root(self)
