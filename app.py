from flask import Flask,render_template,url_for,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt,check_password_hash,generate_password_hash
from model import *
import yaml
app = Flask(__name__)

db = yaml.load(open('db.yaml'))


 
app.config['SECRET_KEY'] = db['app_secret']
app.config['SQLALCHEMY_DATABASE_URI']=db['my_db']
db = SQLAlchemy(app)


bcrypt =Bcrypt()
@app.route('/',methods =['GET'])
def home():
    return render_template('index.html')

@app.route('/catalogue', methods=['GET','POST'])
def catalogue():
    return render_template('catalogue.html')


@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/Enquiries', methods=['GET','POST'])
def Enquiries():
    if request.method == "POST":
        # return'''<h1>We are in Boys</h1>'''
        inquiry = request.form
        name = inquiry['name']
        number = inquiry['number']
        email = inquiry['email']
        enquir = inquiry['memo']
        check = Queries.query.filter_by(inquiry=enquir)
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM users WHERE enquiry = %s",(enquir,))
        # check = cur.fetchone()
        # cur.close()
        if check:
            flash("Enquiry already exist","info")
            return redirect(url_for('Enquiries'))
        # cur.execute("INSERT INTO users(name,number,email,enquiry) VALUES(%s, %s, %s, %s)",(name,number,email,enquir))
        # mysql.connection.commit()
        # cur.close()
        new_query = Queries(name = name,number=number,email=email,inquiry=enquir)
        db.session.add(new_query)
        db.session.commit()
        return redirect(url_for('Enquiries'))
    return render_template('Enquiries.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM user WHERE email= %s AND password = %s" ,(email,password,))
        # user = cur.fetchone()
        # cur.close()
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password) :
            session['loggedin'] = True
            session['id'] = user.id
            session['EMAIL'] = user.email
            return redirect(url_for('enquirieslist'))
        else:
            flash("Incorrect details, Please retry","danger")
            pass
    return render_template('adminlogin.html')


@app.route('/enquirieslist',methods =['GET'])
def enquirieslist():
    if 'loggedin' in session:
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM users")
        # user = cur.fetchall()
        # cur.close()
        user = Queries.query.all()
        return render_template('admindash.html', user=user)
    else:
        flash("you need to login first","success")
        return redirect(url_for('login'))


@app.route('/reply<int:in_id>',methods=['GET','POST'])
def reply(in_id):
    if 'loggedin' in session:
        if request.method == "POST":
            reply = request.form.get('reply')
            if reply:
                # cur = mysql.connection.cursor()
                # cur.execute("UPDATE users SET reply=%s WHERE id = %s",(reply,in_id,))
                # mysql.connection.commit()
                # cur.close()
                Queriess = Queries.query.filter_by(id = in_id).first()
                Queriess.reply = reply
                db.session.commit()
                flash("REPLY SUCCESSFUL Redirecting... TO OPEN YOUR MAIL APP","success")
                return redirect(url_for('enquirieslist'))
        return redirect(url_for('enquirieslist'))
    else:
        flash("you need to login first","success")
        return redirect(url_for('login'))



@app.route('/response<int:un_id>',methods =['GET','POST'])
def response(un_id):
    if 'loggedin' in session:
     
        res = Queries.query.filter_by(id = un_id).first()
        if res:
            if res.reply:
                return render_template('reply.html', res=res)
            else:
                flash("No reply found for this Enquiry","info")
                return redirect(url_for('enquirieslist'))
        else:
            flash("No reply found for this Enquiry","info")
            return redirect(url_for('enquirieslist'))
    else:
        flash("you need to login first","success")
        return redirect(url_for('login')) 
    
    
@app.route('/createaccount',methods =['GET','POST'])
def createaccount():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user=User(email=email,password=pwd)
        db.session.add(new_user)
        db.session.commit()
        flash("Account Creation Successful!","info")
        return redirect(url_for('login'))
    return render_template('createaccount.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)