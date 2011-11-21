from django.template.base import add_to_builtins
#
# Add some useful extra templatetags in builtin templatetags
#----------------------------------------------------------------------------------------------------
add_to_builtins('reversetag.templatetags.reversetag')
add_to_builtins('object_permission.templatetags.object_permission_tags')
add_to_builtins('templatetags.templatetags.sizify')
add_to_builtins('uni_form.templatetags.uni_form_tags')
add_to_builtins('apps.notifications.templatetags.notifications')
add_to_builtins('apps.materials.templatetags.mtimg')
