from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
db = SQLAlchemy(app)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    choice = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    polls = Poll.query.all()
    return render_template('home.html', polls=polls)

@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        name = request.form['name']
        poll = Poll(name=name)
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('poll', poll_id=poll.id))
    return render_template('create_poll.html')

@app.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll = Poll.query.get(poll_id)
    if request.method == 'POST':
        name = request.form['name']
        choice = request.form['choice']
        vote = Vote(poll_id=poll_id, name=name, choice=choice)
        db.session.add(vote)
        db.session.commit()
    votes = Vote.query.filter_by(poll_id=poll_id).all()
    return render_template('poll.html', poll=poll, votes=votes)
