from flask import Flask,render_template,redirect,request,flash,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager as l
from flask_wtf import FlaskForm
import sqlite3
import pandas as pd
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError
from wtforms import StringField,IntegerField,SelectField,SubmitField,PasswordField,BooleanField,TextAreaField
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required
from flask_mail import Mail, Message
app=Flask(__name__,template_folder='template')
key='@boxing'
app.config['SECRET_KEY']=key
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user_order.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tonykungu2@gmail.com'
app.config['MAIL_PASSWORD'] = 'siyysipyizwiufvm'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
data=SQLAlchemy(app)
lm=l(app)
def send_mssg(subject,recipient,sender,mssg):
    msg = Message(subject,sender=sender,recipients =[recipient] )
    msg.body = mssg
    mail.send(msg)
@lm.user_loader
def load_user(s_id):
    return member.query.get(int(s_id))
class member(data.Model,UserMixin):
    id=data.Column(data.Integer,primary_key=True)
    fname=data.Column(data.String(50),nullable=False)
    eid=data.Column(data.Integer,nullable=False)
    password=data.Column(data.String,nullable=False)
    image=data.Column(data.String(50),nullable=True,default='default.jpg')
    relt=data.relationship('orders',backref='members',lazy=True)
    def __repr__(self):
        return str(self.id)
class logform(FlaskForm):
    eid=StringField('Employee Id',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=6,max=30)])
    remember=BooleanField('remember me')
    submit=SubmitField('login')
class regform(FlaskForm):
    fname=StringField("Employee Full name",validators=[DataRequired()])
    eid=StringField('Employee Id',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=6,max=30)])
    submit=SubmitField('Register User')
class orders(data.Model):
    id=data.Column(data.Integer,primary_key=True)
    eid=data.Column(data.Integer,nullable=True)
    fname=data.Column(data.String(50),nullable=True)
    phone=data.Column(data.String(20),nullable=True)
    item=data.Column(data.String(20),nullable=True)
    size=data.Column(data.Integer,nullable=True)
    quant=data.Column(data.Integer,nullable=True)
    desc=data.Column(data.Text,nullable=True)
    quantity=data.Column(data.String(10),nullable=True)
    sprice=data.Column(data.Integer,nullable=True)
    dprice=data.Column(data.Integer,nullable=True)
    ddate=data.Column(data.String(20),nullable=True)
    customer=data.Column(data.String(50),nullable=True)
    cphone=data.Column(data.String(20),nullable=True)
    town=data.Column(data.String(50),nullable=True)
    loc=data.Column(data.Text,nullable=True)
    date=data.Column(data.DateTime,nullable=False,default=datetime.utcnow)
    s_id=data.Column(data.Integer,data.ForeignKey('member.eid'),nullable=False)
    def __repr__(self):
        return str(self.id)
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        subject=request.form["subject"]
        mssg=request.form["message"]
        subject=str(subject)+" by "+ str(name)
        send_mssg(subject,email,"tonykungu2@gmail.com",mssg)
        return redirect(url_for('email_sent'))
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def reg():
    form=regform()
    if form.validate_on_submit():
        members=member(fname=form.fname.data,eid=form.eid.data,password=form.password.data)
        data.session.add(members)
        data.session.commit()
        return redirect(url_for('index'))
    return render_template('reg.html',form=form)
@app.route('/login',methods=['GET','POST'])
def login():
    form=logform()
    if form.validate_on_submit():
        credentials=member.query.filter_by(eid=form.eid.data).first()
        if credentials and credentials.password:
            login_user(credentials,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'invalid email or password','danger')
    return render_template('login.html',form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    if request.method=="POST":
        savings=orders(eid=current_user.eid,fname=current_user.fname,phone=request.form["iphone"],
        item=request.form["iname"],size=request.form["isize"],quant=request.form["quantity"],
        desc=request.form["desc"],sprice=request.form["sprice"],
        dprice=request.form["dprice"],ddate=request.form["ddate"],customer=request.form["cname"],cphone=request.form["cphone"],
        town=request.form["town"],loc=request.form["loc"],members=current_user)
        data.session.add(savings)
        data.session.commit()
        return redirect(url_for('success'))
    return render_template('order.html')
@app.route("/success")
@login_required
def success():
    return render_template("suc.html")
@app.route("/sales")
@login_required
def sales():
    page=request.args.get("page",1,type=int)
    info=orders.query.filter_by(eid=current_user.eid).paginate(page=page,per_page=5)
    return render_template("sales.html",info=info,all=all)

@app.route("/incoming")
def dump_data():
    conx=sqlite3.connect("user_order.db")
    data=pd.read_sql_query("select *from orders",conx)
    html_data=data.to_html()
    file=open("template/data.html","w")
    file.write(html_data)
    file.close()
    return render_template("data.html")
@app.route("/sales/delete/<int:id>")
def delete(id):
    row=orders.query.get_or_404(id)
    data.session.delete(row)
    data.session.commit()
    return redirect(url_for('sales'))
@app.route("/camera")
def get_cam():
    scan_qr()
    return render_template("camera.html",code=code)
@app.route("/confirm")
def delivery():
    return render_template("delivery.html")
@app.route("/email-sent-successfully")
def email_sent():
    return render_template('email')
@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404
@app.errorhandler(500)
def error500(error):
    return render_template('500.html'),500
if __name__=="__main__":
    app.run(debug=True)
