from django.template.base import add_to_builtins

#
# Add some useful extra templatetags in builtin templatetags
#----------------------------------------------------------------------------------------------------
add_to_builtins('notifications.templatetags.notifications')
add_to_builtins('reversetag.templatetags.reversetag')
add_to_builtins('object_permission.templatetags.object_permission_tags')
