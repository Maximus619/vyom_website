from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__, static_url_path='')

# local database connection using xampp
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/vyom'

# online free database using https://www.freesqldatabase.com 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql6468004:FazEykrgDG@sql6.freesqldatabase.com:3306/sql6468004'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'super-secret-key'

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# with open('team.json', 'a') as t:
#     params = json.load(t)["teams"]


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    phonenum = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    dateposted = db.Column(db.String(12), nullable=True)


@ app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@ app.route("/events", methods=['GET', 'POST'])
def events():
    return render_template('events.html')


@ app.route("/team", methods=['GET', 'POST'])
def team():
    return render_template('team.html')


@ app.route("/art", methods=['GET', 'POST'])
def art():
    return render_template('art.html')


@ app.route("/gallery", methods=['GET', 'POST'])
def gallery():
    return render_template('gallery.html')


@ app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('aboutus.html')


@ app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        return redirect(url_for('contact'))
        # name_req = request.form.get('names')
        # email_req = request.form.get('email')
        # phone_req = request.form.get('phonenum')
        # message_req = request.form.get('message')
        # entry = Contacts(name=name_req, email=email_req,
        #                  phonenum=phone_req, message=message_req, dateposted=datetime.now())
        # print(request.form['message'])
        # db.session.add(entry)
        # db.session.commit()
    return render_template('contactus.html')


@ app.route("/admin", methods=['GET', 'POST'])
def admin():
    if "user" in session and session['user'] == params['admin_user']:
        forms = Contacts.query.all()
        return render_template("admin.html", params=params, forms=forms)
    if request.method == "POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable
            session['user'] = username
            forms = Contacts.query.all()
            return render_template("admin.html", params=params, forms=forms)
    else:
        return render_template('login.html')


@ app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user')
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)
