
import login
import database
from config import *
from mysql import connector
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

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

load()
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
    #print(request.remote_addr,request.environ['REMOTE_ADDR'])
    name = request.args.get("name", "world")
    return render_template("login/form.html", name=name)

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

   return render_template('load.html',f=tbl[0],r=tbl[1],title=title,detail=detail)

@app.route('/login',methods = ['POST', 'GET'])
def sign():
   if request.method == 'POST':
      var = request.form
      val = login.verification(var)
      
      

      if val == 1:
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