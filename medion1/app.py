from flask import *
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Sequence
import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash
import os

auth = Blueprint('auth', __name__)
app=Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'awe072355@gmail.com'
app.config['MAIL_PASSWORD'] = 'dlch xbph djim vfgh'

mail=Mail(app)
basedir = os.path.abspath(os.path.dirname(__file__))
def get_data_from_database():
        conn = sqlite3.connect(basedir+'\static\Medicine_Data.db') 
        cursor = conn.cursor()
        cursor.execute('Select id,name,cost,url from Medicine')  
        data = cursor.fetchall()
        conn.close()
        return data

app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db=SQLAlchemy(app)

class OrderData(db.Model):
    order_id = db.Column(db.Integer,Sequence('id_sequence'), primary_key=True, autoincrement=True)
    name=db.Column(db.String(30))
    phone=db.Column(db.Integer())
    email = db.Column(db.String(100))
    medicine=db.Column(db.String(100))
    username=db.Column(db.String(200))
    price=db.Column(db.Float)

class Userr(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@app.route('/')
def home():
    data = get_data_from_database()
    return render_template('index.html',data=data)

@app.route('/index')
def index():
    data = get_data_from_database()
    return render_template('index.html',data=data)
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/medicine')
def medicine():
    data = get_data_from_database()
    return render_template('medicine.html',data=data)

@app.route('/news')
def News():
    return render_template('news.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile(): 
    user = OrderData.query.filter_by(username=session['username']).all()
    count = len(user)
    name=[]
    price=[]
    for i in user:
        name.append(i.medicine)
        price.append(i.price)
    print(user)
    print(name,price)
    data={"count":count,"name":name,"price":price}
    return render_template('profile.html',data=data)

@app.route('/login/',methods=['POST','GET'])
def login():
    print(request.method)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # remember = True if request.form.get('remember') else False

        user = Userr.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login')) 
        session['username'] = email 
        session['name']=user.name
        return redirect(url_for('home')) 
    session.pop('username',None)
    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = Userr.query.filter_by(email=email).first() 

        if user:
            flash('Email address already exists')
            return redirect(url_for('register'))
        
        
        new_user = Userr(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.create_all()
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/buy',methods=['POST','GET'])
def buy():
    if request.method == 'GET':
        id = request.args.get('data')
        conn = sqlite3.connect(basedir+'\static\Medicine_Data.db')
        cur=conn.cursor()
        cur.execute('SELECT name,cost FROM Medicine where id={}'.format(id))
        data=cur.fetchall()
        return render_template('order.html', data=data[0])
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        medicine = request.form.get('medicine')
        price = request.form.get('price')
        username = session['username']
        form_data = OrderData(name=name, phone=phone, email=email,medicine=medicine,username=username,price=price)
        db.create_all()
        subject="Delivery order"
        recipients=[email]
        body="Hello {} \n\n Thank you for placing an Order.  \n\n Your Order has been Placed Successfully \n Order Details: \n\n Medicine Name -: {} \n Price-:{} \n\n Thankyou \n\n\n Regards \n Medion".format(name,medicine,price)
        message=Message(subject=subject,sender="noreply.dpkgtm12@gmail.com",recipients=recipients,body=body)
        mail.send(message)
        db.session.add(form_data)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)



