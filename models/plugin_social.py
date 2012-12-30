# CONFIGS

# Plugin can be called by an arbitrary name instead of /plugin_social (which is a bit ugly)
# example: http://..../social/friends or http://..../contacts/search
plugin_social_shortcut = response.plugin_social_shortcut or "social"

# The plugin_social models are conditional and tables are defined only for specific controller
# users can set response.plugin_social_controllers_to_run = ['default'] 
# to fire the definition of plugin_social functions and tables
plugin_social_controllers_to_run = response.plugin_social_controllers_to_run or []

# Set the models to run
if request.controller in plugin_social_controllers_to_run + [plugin_social_shortcut]:    
    response.models_to_run.append("^plugin_social/\w+\.py$")

# Test if called by shortcut
if request.controller == plugin_social_shortcut:
    request.controller = 'plugin_social'
    response.view = response.view.replace(plugin_social_shortcut, 'plugin_social')
    
