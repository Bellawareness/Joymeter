from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from joy_tracker import JoyTracker
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}  # For testing only

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user_id'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.', 'error')
        else:
            users[username] = password
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/add_joy_moment', methods=['GET', 'POST'])
def add_joy_moment_form():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        description = request.form['description']
        joy_level = int(request.form['joy_level'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        joy_tracker = JoyTracker(user_id)
        joy_tracker.add_joy_moment(description, joy_level, timestamp)
        return redirect(url_for('view_joy_moments', user_id=user_id))
    return render_template('add_joy_moment.html')

@app.route('/view_joy_moments/<user_id>')
def view_joy_moments(user_id):
    if session.get('user_id') != user_id:
        return redirect(url_for('login'))
    joy_tracker = JoyTracker(user_id)
    joy_moments = joy_tracker.get_joy_moments()
    return render_template('view_joy_moments.html', joy_moments=joy_moments)

@app.route('/add_goal', methods=['GET', 'POST'])
def add_goal():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        goal_description = request.form['goal_description']
        timeline = request.form['timeline']
        joy_tracker = JoyTracker(user_id)
        joy_tracker.add_goal(goal_description, timeline)
        return redirect(url_for('view_goals', user_id=user_id))
    return render_template('add_goal.html')

@app.route('/view_goals/<user_id>')
def view_goals(user_id):
    if session.get('user_id') != user_id:
        return redirect(url_for('login'))
    joy_tracker = JoyTracker(user_id)
    goals = joy_tracker.view_goals()
    return render_template('view_goals.html', goals=goals)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user_id=user_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/joy_moments', methods=['GET'])
def get_joy_moments_api():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([]), 401
    joy_tracker = JoyTracker(user_id)
    moments = joy_tracker.get_joy_moments()
    return jsonify([
        {'description': m[1], 'joyLevel': m[2], 'timestamp': m[3] if len(m) > 3 else None} for m in moments
    ])

@app.route('/api/joy_moments', methods=['POST'])
def add_joy_moment_api():
    user_id = session.get('user_id')
    data = request.get_json()
    description = data.get('description')
    joy_level = data.get('joyLevel')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    joy_tracker = JoyTracker(user_id)
    joy_tracker.add_joy_moment(description, joy_level, timestamp)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
