# -*- coding: utf-8 -*-
#
# src/Kommonz/utils/decorators.py
# created by giginet on 2011/11/29
#
from django.utils.decorators import method_decorator
def view_class_decorator(decorator):
    """
    Converts a function decorator into a Generic View Class decorator
    Usage
        @view_class_decorator(login_required)
        class SomeModelCreateView(CreateView):
            model = SomeModel
    """
    def _decorator(cls):
        dispatch = getattr(cls, 'dispatch')
        func = method_decorator(decorator)
        dispatch = func(dispatch)
        setattr(cls, 'dispatch', dispatch)
        return cls
    return _decorator
