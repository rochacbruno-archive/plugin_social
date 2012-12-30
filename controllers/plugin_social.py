# a page for searching friends and requesting friendship
@auth.requires_login()
def search(): 
    return plugin_social_search()

# a page for accepting and denying friendship requests
@auth.requires_login()
def friends():
    return plugin_social_friends()

# service callback for accepting, denaing and revoking friendship
@auth.requires_login()
def callback():
    return plugin_social_callback()
