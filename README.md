Social plugin for web2py
=============

web2py social plugin

A set of tools for building social apps

Instalation and usage
=============

1) Download or clone and install the plugin (requires db and auth)

2) visit http://..../yourapp/plugin_social/search to search for other users by name and send friend requests

3) visit http://..../yourapp/plugin_social/friends to manage your friends (accept/deny/revoke friend requests)

4) use plugin_social_friend_ids(auth.user.id) to get the user ids of your friends

5) you should create a default/home/id page for each user profile since the plugin will redirect there.

It is based on an improved subset of https://github.com/mdipierro/web2py-appliances/tree/master/FacebookClone


License
=============

BSD
