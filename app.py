
from os import name
import login
import log
import database
from config import *
from mysql import connector
from flask import Flask, redirect, url_for, request, render_template, make_response
from flask_mail import * 
from random import randint

app = Flask(__name__)
mail = Mail(app)  
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = email
app.config['MAIL_PASSWORD'] = email_password  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
otp = randint(000000,999999) 

def load():
    db = connector.connect(
    host=database_host,
    user=database_user,
    password=database_password)
    cursor = db.cursor(buffered=True,dictionary=True)

    sql = "CREATE DATABASE IF NOT EXISTS {s0}".format(s0=database_name)
    cursor.execute(sql)

    db = connector.connect(
    host=database_host,
    user=database_user,
    password=database_password,
    database=database_name)
    cursor = db.cursor(buffered=True,dictionary=True)
    
    database_create = database.database_create(cursor, db)
    database_create.create_base()

#load()
print("database loaded")


def table_create(tbl=None):
   col = []
   roww= []


   for field in tbl[0]:
      col.append(field)   

   i= 0

   for data in tbl:
      roww.append([])
      r=[]
      for x  in data:
         r.append(data[x])
      roww[i].append(r)
      i=i+1
   
   row = []
   
   for c in range (0,i):
      row.append(roww[c][0])

   all = []
   all.append(col)
   all.append(row)

   return all


@app.route("/")
def index():
   try:
      user=getcookie()
      login.verification(user)
      return render_template("sel.html")
   except:
      pass
   return render_template("login/form.html")

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route("/error")
def error():
    return render_template("error/error.html")


@app.route('/select')
def select():
   return render_template("sel.html")


@app.route('/load',methods = ['POST', 'GET'])
def table():
   t=1
   tbl = None

   if request.method == 'POST':
      t = request.form
      print(t)
      t = int(t['select'])
   
   if t == 1:
      tbl=database.get_user()
      title = "User Base"
      detail = "Contains all user's info, the bot has interacted with creating a log"   
   elif t == 2:
      tbl=database.get_chat()
      title = "Chat Base"
      detail = "Contains all group info, the bot has been in"
   elif t == 3:
      tbl=database.get_link()
      title = "Link Base"
      detail = "Contains link details of members the bot has seen in a group"
   elif t == 4:
      tbl=database.get_settings()
      title = "Settings Base"
      detail = "Contains settings of groups"
   elif t == 5:
      tbl=database.get_welcome()
      title = "Welcome Base"
      detail = "Welcome settings of all groups"

   tbl = table_create(tbl)

   return render_template('login/load.html',f=tbl[0],r=tbl[1],title=title,detail=detail)


@app.route('/setcookie')
def setcookie():
    key=request.args.get('key')
    val=request.args.get('val')
    resp = make_response(render_template("sel.html"))
    resp.set_cookie(key,val)
    return resp

@app.route('/register')
def reg():
    return render_template("login/register.html")

@app.route('/confirm/<user>',methods = ['POST', 'GET'])
def confirm(user):
    print(user)
    log.verify(user)
    return render_template("login/ok.html",val="You Have Been Successfully Registered !".format(u=user))

@app.route('/verify',methods = ["POST"])  
def verify():  
   data = request.form
   email=None
   if data['member']=='sudo' or data['member']=='admin':
      return render_template("login/ok.html",val="Wait For approval..")
  
   msg = log.arrange(data['uname'],data['pass'],data['email'],data['fname'],data['lname'], data['member'])

   if msg == 1:
      email = data["email"]
      username = data["uname"]
      msg = Message('My Dashboard OTP Verification Number',sender = 'username@gmail.com', recipients = [email])  
         
      if veri == 1:
         #text= "Hello {f}, \n\n<a href=\"www.google.com\">Click Here</a> to complete your register in My-Dashboard as '{u}'  \n\nVisit our website for more details.\nThank You".format(f=data['fname'],u=data['uname'],n=otp)
         #msg.body = str(text)
         msg.html=render_template('login/veri.html', u=username,f=name, email=email)
         mail.send(msg)
         return render_template("login/ok.html",val="Redirecting..",msg="A verification email has been sent to ", email=email)
      else:
         text= "Hello {f}, \n\nYour (OTP) verification code for My-Dashboard registration (as '{u}') is : {n}\n\nVisit our website for more details.\nThank You".format(f=data['fname'],u=data['uname'],n=otp)
         msg.body = str(text)
         mail.send(msg)
         return render_template("login/reg_otp.html",email=email,username=username)
   else:
      return render_template("login/ok.html",val=msg)


@app.route('/validate',methods=["POST"])   
def validate():  
   user_otp = request.form['no']
   username = request.form['noo']
   email = request.form['nooo']

   try:  
      if otp == int(user_otp):
         log.verify(username)
         return render_template("login/ok.html", val="You Have Been Verified !") 
   except:
      pass
   return render_template("login/reg_otp.html",alert="true")


@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('user', None)
    return name

@app.route('/deletecookie')
def delcookie():
   resp = make_response(render_template("sel.html"))
   resp.set_cookie('user', '', expires=0)
   return resp


@app.route('/ok')
def ok():
   return render_template("login/ok.html", val="You Have Been Verified !")

@app.route('/nig')
def nig():
   resp = make_response(render_template("login/reg_otp.html"))
   return resp


@app.route('/login',methods = ['POST', 'GET'])
def sign():
   if request.method == 'POST':
      var = request.form
      val = login.verification(var)      
      
      if val == 1:
         try:
            if var['remember-me']=="on":
               return redirect(url_for('setcookie', key='user', val=var['username']))
            else:
               return redirect(url_for('select'))    
         except:
            return redirect(url_for('select'))
         return redirect(url_for('getcookie'))
         #return table()
         return redirect(url_for('select'))
         return redirect(url_for('success',name = "to the url"))
      else:
         return render_template('login/form.html', msg = val)
      #user = request.form['nm']
      
   else:
      return redirect(url_for('error'))

if __name__ == '__main__':
   app.run(host = '192.168.85.182', debug = True, port=5000)