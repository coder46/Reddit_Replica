# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    redirect(URL(r=request,f='list_news'))
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


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
@auth.requires_login()
def list_news():
		
		cats=db(db.category.id>0).select()
		return dict(cats=cats,news=db().select(db.news.ALL,orderby=~db.news.rating))
		
@auth.requires_login()
def post_news():
	return dict(form=crud.create(db.news))
	
@auth.requires_login()
def view_news():
	news_id=request.args(0) or redirect(URL(r=request,f='index'))
	db.comments.news_id.default=news_id
	db.comments.news_id.writable=db.comments.news_id.readable=False
	return dict(news_id=news_id,form1=crud.read(db.news,news_id),comments=db(db.comments.news_id==news_id).select(orderby=db.comments.posted_on),form2=crud.create(db.comments))


def delete_news():
		news_id=request.args(0) or redirect(URL(r=request,f='index'))
		news=db.news[news_id]
		#db(int(news.id)==int(news_id) & int(news.posted_by)==int(auth.user.id)).delete()
		db((db.news.id==news_id) & (db.news.posted_by==auth.user.id)).delete()
		redirect(URL(r=request,f='index'))
		return dict(news_id=news_id)		
		
def update_news():
                                                  record=db.news(request.args(0)) or redirect(URL('index'))
                                                  form=SQLFORM(db.news,record,deletable=True)
                                                  if form.process().accepted:
                                                      response.flash='form accepted'
                                                  elif form.errors:
                                                      respose.flash='form has errors'
                                                  return dict(form=form)
                                                      
                                                  
                                                                                                     
                                                  
								
'''					
def upvote():
    item=db.news[request.vars.id]
    items=db().select(db.upvotes.ALL)
    #item=db.item[request.vars.id]
    flag=0
    new_votes=db.news[request.vars.id].uvotes
    count=0
    for i in items:
        if i.news_id==1:
                    count=count+1
        if int(i.news_id)==int(item.id) and int(i.upvoted_by)==int(auth.user.id):
             flag=1
             break
        
  
    if flag==0:
        new_votes=item.uvotes+1;
        item.update_record(uvotes=new_votes)
        db.upvotes.insert(news_id=item.id)
    elif flag==1:
        new_votes=item.uvotes-1
        item.update_record(uvotes=new_votes)
        #db.upvotes.delete(item_id=item.id && upvoted_by=auth.user.id)
        db( (db.upvotes.news_id==item.id) & (db.upvotes.upvoted_by==auth.user.id)).delete()
    return str(new_votes)



def downvote():
    item=db.news[request.vars.id]
    items=db().select(db.downvotes.ALL)
    #item=db.item[request.vars.id]
    flag=0
    new_votes=item.dvotes
    count=0
    for i in items:
        """if i.item_id==1:
                    count=count+1"""
        if int(i.news_id)==int(item.id) and int(i.downvoted_by)==int(auth.user.id):
             flag=1
             break
        
  
    if flag==0:
        new_votes=item.dvotes-1;
        item.update_record(dvotes=new_votes)
        db.downvotes.insert(news_id=item.id)
    elif flag==1:
        new_votes=item.dvotes+1
        item.update_record(dvotes=new_votes)
        #db.upvotes.delete(item_id=item.id && upvoted_by=auth.user.id)
        db( (db.downvotes.news_id==item.id) & (db.downvotes.downvoted_by==auth.user.id)).delete()
    return str(new_votes)


'''


def upvote():
    item=db.news(request.args(0)) or redirect(URL('index'))
    items=db().select(db.upvotes.ALL)
    poster=item.posted_by
    downvoteditems=db().select(db.downvotes.ALL)
    #new_votes=item.uvotes+1
    #item.update_record(uvotes=new_votes)
    flag=0
    new_votes=item.uvotes
    new_rating=item.rating
    count=0
    for i in items:
        '''if i.news_id==1:
                    count=count+1'''
        if int(i.news_id)==int(item.id) and int(i.upvoted_by)==int(auth.user.id):
             flag=1
             break
    newflag=0;
    for i in downvoteditems:
            if(int(i.news_id)==int(item.id) and int(i.downvoted_by)==int(auth.user.id)):
                newflag=1
                break
    d=0
    if flag==0:
        new_votes=item.uvotes+1;
        new_rating=new_rating+5
        if(newflag==1):
            new_rating=new_rating+3
            d=item.dvotes
            item.update_record(dvotes=d+1)
            db((db.downvotes.news_id==item.id) & (db.downvotes.downvoted_by==auth.user.id)).delete()
        item.update_record(uvotes=new_votes)
        item.update_record(rating=new_rating)
        
        db.upvotes.insert(news_id=item.id)
    elif flag==1:
        new_votes=item.uvotes-1
        new_rating=new_rating-5
        item.update_record(uvotes=new_votes)
        item.update_record(rating=new_rating)
        #db.upvotes.delete(item_id=item.id && upvoted_by=auth.user.id)
        db( (db.upvotes.news_id==item.id) & (db.upvotes.upvoted_by==auth.user.id)).delete()
    item.update_record(posted_by=poster)
    redirect(URL(r=request))
    response.flash='comemnt '
    return dict()

def downvote():
    item=db.news(request.args(0)) or redirect(URL('index'))
    poster=item.posted_by
    upvoteditems=db().select(db.upvotes.ALL)
    items=db().select(db.downvotes.ALL)
    flag=0
    new_rating=item.rating
    new_votes=item.dvotes
    count=0
    for i in items:
        """if i.item_id==1:
                    count=count+1"""
        if int(i.news_id)==int(item.id) and int(i.downvoted_by)==int(auth.user.id):
             flag=1
             break
    new_flag=0
    u=0
    for i in upvoteditems:
        if int(i.news_id)==int(item.id) and int(i.upvoted_by)==int(auth.user.id):
            new_flag=1
            break
    if flag==0:
        new_votes=item.dvotes-1;
        new_rating=new_rating-3
        if new_flag==1:
                new_rating=new_rating-5
                u=item.uvotes         
                item.update_record(uvotes=u-1)
                db((db.upvotes.news_id==item.id) & (db.upvotes.upvoted_by==auth.user.id)).delete()
                
        item.update_record(dvotes=new_votes)
        item.update_record(rating=new_rating)
        db.downvotes.insert(news_id=item.id)
    elif flag==1:
        new_votes=item.dvotes+1
        new_rating=new_rating+3
        item.update_record(dvotes=new_votes)
        item.update_record(rating=new_rating)
        #db.upvotes.delete(item_id=item.id && upvoted_by=auth.user.id)
        db( (db.downvotes.news_id==item.id) & (db.downvotes.downvoted_by==auth.user.id)).delete()
    item.update_record(posted_by=poster)    
    redirect(URL('index'))
    return dict()

def admin_page():
    a=1
    return dict(a=a)
def users_list():
    users=db().select(db.auth_user.ALL)
    return dict(users=users)
    
def delete_user():
    user_id=request.args(0)
    upvoted_posts=db((db.upvotes.upvoted_by==user_id) & (db.upvotes.news_id==db.news.id)).select(db.news.ALL)
    downvoted_posts=db((db.downvotes.downvoted_by==user_id) & (db.downvotes.news_id==db.news.id)).select(db.news.ALL)
    for i in upvoted_posts:
            poster=i.posted_by
            new_rating=i.rating-5
            db(db.news.id==i.id).update(rating=new_rating)
            db(db.news.id==i.id).update(posted_by=poster)
            uvotes=i.uvotes-1
            #db.news.update(uvotes=uvotes)
    for i in downvoted_posts:
        poster=i.posted_by
        new_rating=i.rating+3
        db(db.news.id==i.id).update(rating=new_rating)
        dvotes=i.dvotes+1
        db(db.news.id==i.id).update(posted_by=poster)
        #db.news.update(dvotes=dvotes)
    db(db.auth_user.id==user_id).delete()
    redirect(URL(r=request,f='users_list'))


def add_cats():
    if auth.user.id==3:
        return dict(form=crud.create(db.category))
    else:
        redirect(URL('index'))
