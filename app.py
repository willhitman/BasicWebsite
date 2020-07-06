from flask import Flask,render_template,url_for,request,redirect
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
 
app.config['SECRET_KEY'] = "7c0d5223a0809d6e3b31b714ec5a6a53"

mysql = MySQL(app)

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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,number,email,enquiry) VALUES(%s, %s, %s, %s)",(name,number,email,enquir))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Enquiries'))
    return render_template('Enquiries.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email= %s AND password = %s" ,(email,password,))
        user = cur.fetchone()
        if user :
            return redirect(url_for('enquirieslist'))
            
    return render_template('adminlogin.html')


@app.route('/enquirieslist')
def enquirieslist():
    return'''<h1>We are in Boys</h1>'''


if __name__ == '__main__':
    app.run(debug=True)