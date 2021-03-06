import random
import json

def index():
    return dict(message=T('Welcome to our Crowd Sourcing Platform!'))

#@auth.requires_login()
def get_sentence():
    return "bla"

#@auth.requires_login()
def tutorial():
    return dict()


def getAnnotation(data):
    session.data = data
    ret = "<p>"
    words = data['sentence']
    separators = data['conjunction']
    high = data['highlighted']
    j = 0
    k = 0
    for i in xrange(len(words)):
        if j <> len(separators) and i == separators[j]:
            j += 1
            ret += "<span class='word red' id='" + str(i) + "'>" + words[i] + "&nbsp;</span>"
        elif k <> len(high) and i == high[k]:
            k += 1
            ret += "<span class='word high' id='" + str(i) + "'>" + words[i] + "&nbsp;</span>"
        else:
            ret += "<span class='word' id='" + str(i) + "'>" + words[i] + "&nbsp;</span>"
    ret += "</p>"
    return XML(ret)


@auth.requires_login()
def contribute():
    x = db(db.once).select()
    y = db(db.approved).select()
    instr = XML("<h4> Yay! We are done.")
    btn = XML("")
    sn = XML("")
    if len(x) > 0:
        instr = XML("<h4> Annotate the following sentence for list elements </h4>")
        btn = XML("<button type='submit' class='btn btn-primary' id='submit'>Submit</button>")
        session.index = random.randint(0, len(x)-1)
        print "rand index", session.index
        sn = getAnnotation(x[session.index])
    return dict(sentence=sn, once=len(x), approved=len(y), instruction=instr, buttons=btn)


def recordAnnotation():
    lis = map(int, filter(None, request.vars.lis.split(',')))
    data = session.data
    id = data['id']
    if data['highlighted'] == lis:
        db.approved.insert(sentence=data['sentence'], conjunction=data['conjunction'], highlighted=data['highlighted'], person1=data['person'], person2=auth.user)
    else:
        db.once.insert(sentence=data['sentence'], conjunction=data['conjunction'], highlighted=lis, person=auth.user)        
    db(db.once.id == id).delete()
    ret = contribute()
    ret['sentence'] = str(ret['sentence'])
    ret['instruction'] = str(ret['instruction'])
    ret['buttons'] = str(ret['buttons'])
    return json.dumps(ret)

def reset():
    db(db.once).delete()
    db(db.approved).delete()
    db.once.insert(sentence=["this", "is", "shit", "and", "smack1"], conjunction=[3], highlighted=[2, 4])
    db.once.insert(sentence=["this", "is", "shit", "and", "smack2"], conjunction=[3], highlighted=[2, 4])
    db.once.insert(sentence=["this", "is", "shit", "and", "smack3"], conjunction=[3], highlighted=[2, 4])
    db.once.insert(sentence=["this", "is", "shit", "and", "smack4"], conjunction=[3], highlighted=[2, 4])
    return dict()

def lis():
    x = db(db.approved).select()

    print "=================================================================="
    print x
    print "=================================================================="

    return dict()
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
