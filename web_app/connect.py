from flask import Flask, render_template, url_for, request, session, redirect
from flask.ext.pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'heroku_2g2nnp30'
app.config['MONGO_URI'] = 'mongodb://engage48:engage48@ds149134.mlab.com:49134/heroku_2g2nnp30'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'name' in session:
        return 'You are logged in as ' + session['name']

    return render_template('index.html')
    
    
    
    
    @app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['name']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'], 'password' : hashpass})
            session['name'] = request.form['name']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('inner.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
