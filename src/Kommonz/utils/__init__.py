from django.utils.functional import lazy
from django.core.urlresolvers import reverse
lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

