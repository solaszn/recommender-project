from flask import Flask, flash, render_template, url_for, request, session, redirect
from master import recommend, alg_accuracy
from flask_pymongo import PyMongo
import bcrypt
import datetime

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'recommender'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recommender'
# session.permanent = False


mongo = PyMongo(app)
salt = b'$2b$12$jyO6geo1lwHtJELmhohhpO'


@app.route('/')
@app.route('/index')
def home():
    if 'username' in session:
        client = session['username']
        return render_template('onboarding.html', value=client)

    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        clients = mongo.db.clients
        admin = mongo.db.admin
        admin_user = admin.find_one({'name' : request.form['username']})
        login_user = clients.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), salt) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
        if admin_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), salt) == admin_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('adminDashboard'))

        flash('Invalid username/password combination!')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        clients = mongo.db.clients
        existing_clients = clients.find_one({'name' : request.form['newuser']})

        if existing_clients is None:
            hashpass = bcrypt.hashpw(request.form['newpswd'].encode('utf-8'), salt)
            clients.insert_one({'name' : request.form['newuser'], 'mail' : request.form['mailbox'], 'password' : hashpass})
            session['username'] = request.form['newuser']
            return redirect(url_for('home'))
        
        flash('That username already exists!')
 
    return render_template('register.html')


@app.route('/client', methods=['POST', 'GET'])
def clientDashboard():
    if 'username' in session:
        if request.method == 'POST':
            # Write requests to chats
            chat_collections = mongo.db.chats
            time = datetime.datetime.now()
            chat_collections.insert_one({'type': 'request', 'clientName': session['username'], 'request': request.form['user-request'], 'time': time.strftime("%c")})

        client = session['username']
        # render recommendations
        return render_template('dashboard.html', value=client, data=[])

    return render_template('index.html')

@app.route('/client/ads')
def clientAdDashboard():
    if 'username' in session:
        client = session['username']
        return render_template('adashboard.html', value=client)

    return render_template('index.html')

@app.route('/admin')
def adminDashboard():
    if 'username' in session:
        admin = mongo.db.admin
        usertype = admin.find_one({'name' : session['username']})
        if usertype is not None:
            client = session['username']
            data = alg_accuracy
            # send algorithm accuracy to admin..
            return render_template('adminboard.html', value=client, data=data)

    return render_template('index.html')

@app.route('/client/session',  methods=['POST', 'GET'])
def clientSession():
    if 'username' in session:
        if request.method == 'POST':
            bus_name = request.form['name']
            ind = request.form.get('industries')
            srvc = request.form.get('services')
            # call recommender f(n), return res to clientDashboard
            results = recommend(ind, srvc, 5)
            # Write results to db.sessions, with username, datetime, business name...
            session_collection = mongo.db.sessions
            time = datetime.datetime.now()
            # send to client template as py.list --> JS.arr.
            newList = []
            for key, value in results.items():
                for x in value:
                    platform = x.lower()
                    newList.append(platform)
            print(newList)
            client = session['username']
            session_collection.insert_one({'clientName': session['username'], 'time': time.strftime("%c"), 'businessName': bus_name, 'results': newList})
            return render_template('dashboard.html', value=client,data=newList)

        return render_template('session.html')

    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'solaszn'
    app.run(host='localhost', port=3000, debug=True)