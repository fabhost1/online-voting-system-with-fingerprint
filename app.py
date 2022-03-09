from flask import Flask,flash, render_template,request, redirect, url_for,jsonify
import cv2
import AddUser as db
from pickle import TRUE
#import serial
from serial import Serial

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def landing():
    return render_template('home.html')

@app.route("/login",methods=["POST"])
def login():
    
    [name,id,password,fingerprint] = [request.form['name'],request.form['id'],request.form['password'],request.form['fingerid']]
    status = db.VerifyUser(id,password,fingerprint)
    if(status!=1):
        return render_template("Error.html",status=status)
    if(request.form["id"]=="0000"):
        return render_template("admin.html",name="Admin")
    else:
        return redirect("/vote/"+request.form['id']+"/"+request.form['name'])

@app.route("/admin")
def admin():
    return render_template("admin.html",name="Admin")
    
@app.route('/vote/<id>/<name>',methods=["GET"])
def vote(id,name):
    return render_template('vote.html',name=name,id=id)

@app.route('/addfinger',methods=['GET','POST'])
def addfinger():
    s = Serial('COM5')
    res = s.read()
    output=int(res)
    return render_template("login.html",finger=output)


@app.route('/addVoter',methods=['GET','POST'])
def addVoter(name=None):
    if request.method == 'GET':
        return render_template('addVoter.html')
    if request.method == 'POST':
        status = db.addVoter(request.form['Name'],request.form['Password'],request.form['fingerprint'],request.form['Id'])
        if(status!="Done"):
            return "Voter already exists"
        if(request.form['Name'].lower=="admin"):
            return render_template("admin.html")
        else:
            return redirect('/admin')

@app.route("/CastVote/<party>/<id>")
def addVote(party,id):
    status = db.AddVote(id,party)
    return render_template("Error.html",status=status,link="/")

@app.route("/results")
def results():
    result = db.result() 
    print(result)
    if(result=="0"):
        return render_template("Error.html",status="All voters have not casted their votes yet",link="/admin")
    
    return render_template("results.html",d=result)

@app.route("/clear")
def clear():
    status = db.clearDb()
    return render_template("Error.html",status=status,link="/addVoter")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')