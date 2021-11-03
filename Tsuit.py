#encoding:utf-8
from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template
from flask_moment import Moment
from datetime import datetime
import flask_wtf
from form import LoginForm

from flask import session, url_for
from flask import flash

from flask_bootstrap import Bootstrap
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir=os.path.abspath(os.path.dirname('Tsuit.py'))

app=Flask(__name__)
bootstrap=Bootstrap(app)
moment=Moment(app)

app.config['SECRET_KEY']='my first app'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////'+os.path.join(basedir,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

migrate=Migrate(app,db)


class Role(db.Model):
    tablename='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role',lazy='dynamic')
    def repr(self):
        return '<Role %r>' % self.name


class User(db.Model):
    tablename='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    def repr(self):
        return '<User %r>' % self.username



@app.route('/mybase')
def mybase():
    return render_template("mybase.html")

@app.route('/')
def index():
    # user_agent=request.headers.get('User-Agent')
    # return "<h1>Hello index</h1> <p> your browser is :{}</p>".format(user_agent)
    # response=make_response("<h1>Hello index</h1> <p> your browser is :{}</p>".format(user_agent))
    # response.set_cookie('answer','42')
    return render_template('index.html',cur_time=datetime.utcnow())

@app.route('/redirection')
def redirection():
    return redirect('http://www.baidu.com')

@app.route('/user/<name>')
def user(name):
    if name.lower() == 'fuck':
        page_not_found("脏话")
        abort(404)
    return render_template('user.html',name=name)

@app.route('/login',methods=['GET','POST'])
def login():
    name=None
    password=None
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user =User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known']=False
        else:
            session['known']=True

        session['name']=form.name.data
        session['password']=form.password.data
        form.name.data=""
        form.password.data=''
        return redirect(url_for('login'))
    return render_template('login.html',form=form,name=session.get('name'),known=session.get('known',False))
    #     old_name=session.get('name')
    #     if old_name is not None and old_name !=form.name.data:
    #         flash('you have changed your name')
    #     session['name']=form.name.data
    #     session['password']=form.password.data
    #     return redirect(url_for('login'))
    #     # print(name,password)
    #     form.name.data=''
    #     form.password.data=''
    # return render_template('login.html',form=form,name=session.get('name'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role)





if __name__=='__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)