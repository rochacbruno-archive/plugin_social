"""
To use this plugin you need a database called db, you need auth
"""


db.define_table('plugin_social_link',
    Field('source_user','reference auth_user'),
    Field('target_user','reference auth_user'),
    Field('accepted','boolean',default=False))

def plugin_social_friend_button(
    user_id,name=T('Friend'),action='request',replace=T('pending')):
    return TAG.button(name,_onclick="var x=this;jQuery.post('%s',function(d,t,r){jQuery(x).parent().html('%s');})" % (URL('plugin_social','callback',args=(action,user_id)),replace))

def plugin_social_accept_button(user_id):
    return plugin_social_friend_button(
        user_id,T('Accept'),'accept',T('Accepted'))

def plugin_social_deny_button(user_id):
    return plugin_social_friend_button(
        user_id,T('Deny'),'deny',T('Denied'))

def plugin_social_revoke_button(user_id):
    return plugin_social_friend_button(
        user_id,T('Revoke'),'revoke',T('revoked'))

def plugin_social_search():
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.name.split()
        query = reduce(lambda a,b:a&b,[
                db.auth_user.first_name.contains(k)|
                db.auth_user.last_name.contains(k)
                for k in tokens])
        people = db(query).select(orderby=db.auth_user.first_name|db.auth_user.last_name)
    else:
        people = []
    return dict(form=form, people=people)

def plugin_social_friends():
    u, l, me = db.auth_user, db.plugin_social_link, auth.user.id
    friends = db(u.id==l.source_user)(l.target_user==me).select(orderby=u.first_name|u.last_name)
    requests = db(u.id==l.target_user)(l.source_user==me).select(orderby=u.first_name|u.last_name)
    return locals()

def plugin_social_callback():
    """AJAX callback!"""
    link, me = db.plugin_social_link, auth.user.id
    a0,a1 = request.args(0),request.args(1, cast=int)
    if request.env.request_method!='POST': raise HTTP(400)
    if a0 == 'request' and not link(source_user=a1, target_user=me):
        # insert a new friendship request
        link.insert(source_user=me,target_user=a1)
    elif a0 == 'accept':
        # accept an existing friendship request
        db(link.target_user==me)(link.source_user==a1).update(accepted=True)
        if not db(link.source_user==me)(link.target_user==a1).count():
            link.insert(source_user=me,target_user=a1)
    elif a0=='deny':
        # deny an existing friendship request
        db(link.target_user==me)(link.source_user==a1).delete()
    elif a0=='revoke':
        # delete a previous friendship request
        db(link.source_user==me)(link.target_user==a1).delete()
    return 'ok'

def plugin_social_friend_ids(user_id=auth.user_id):
    return [row.id for row in db(db.plugin_social_link.source_user==user_id)\
                (db.plugin_social_link.approved==True).select()]

plugin_social_menu = [
    (T('Search Friends'),None,URL('plugin_social','search')),
    (T('Manage Friends'),None,URL('plugin_social','manage'))
    ]
