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

from flask_bootstrap import Bootstrap
app=Flask(__name__)
app.config['SECRET_KEY']='my first app'
bootstrap=Bootstrap(app)
moment=Moment(app)

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
        name=form.name.data
        password=form.password.data
        print(name,password)
        form.name.data=''
        form.password.data=''
    return render_template('login.html',form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html')



if __name__=='__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)