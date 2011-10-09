# ref : http://www.essentialcode.com/2009/01/26/splitting-django-models-into-separate-files/
import os
import re
import types
 
PACKAGE = 'materials.models'
MODEL_RE = r"^.*.py$"

def get_models(package_dir):
    model_names = []
    for filename in os.listdir(package_dir):
      if not re.match(MODEL_RE, filename) or filename == "__init__.py":
        continue
      model_module = __import__('%s.%s' % (PACKAGE, filename[:-3]),
                               {}, {},
                               filename[:-3])
      for name in dir(model_module):
        item = getattr(model_module, name)
        if isinstance(item, (type, types.ClassType)):
            exec "%s = item" % name
            model_names.append(name)
 
# Hide everything other than the classes from other modules.
__all__ = get_models(os.path.dirname( __file__))