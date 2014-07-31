from random import randrange

def index():
    return dict(message=T('Welcome to our Crowd Sourcing Platform!'))

#@auth.requires_login()
def get_sentence():
    # x=None
    # y=None
    # x = db.data_list.select(db.data_list.ALL,db.data_list.submissions==0)[0]
    # for y in db.data_list.select(db.data_list.ALL,db.data_list.submissions>0):
    #     if y.users.contains(auth.user_id)==False: break
    # r = randrange(3)
    # if r==0: return y or -1
    # return x or -1

    return "bla"

#@auth.requires_login()
def tutorial():
    return dict()

#@auth.requires_login()
def contribute():
    x = db(db.clear).select()
    y = db(db.once).select()
    z = db(db.approved).select()

    return dict(sentence="test", clear=len(x), once=len(y), approved=len(z))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
