from flask import Flask,render_template,url_for

app = Flask(__name__)

app.route('/',methods =['GET'])
def home():
    return render_tamplate('index.html')

app.route('/inquiries', methods =['GET',['POST']])
def inquiries():
    pass

if __name__ == '__main__':
    app.run(debug=True)