import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Create the database and tables if they don't exist
def setup_database():
    conn = sqlite3.connect("joy_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS joy_moments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        description TEXT NOT NULL,
        joy_level INTEGER NOT NULL,
        timestamp TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        contribution TEXT,
        feeling TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timeline TEXT,
        goal_description TEXT,
        progress INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# JoyTracker class encapsulating the joy moments and goal functionalities
class JoyTracker:
    def __init__(self, user_id):
        self.user_id = user_id

    def add_joy_moment(self, description, joy_level, timestamp):
        conn = sqlite3.connect('joy_tracker.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO joy_moments (user_id, description, joy_level, timestamp) VALUES (?, ?, ?, ?)",
            (self.user_id, description, joy_level, timestamp)
        )
        conn.commit()
        conn.close()

    def generate_weekly_summary(self):
        today = datetime.now()
        start_date = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")  # Monday of the current week
        end_date = (today + timedelta(days=(6 - today.weekday()))).strftime("%Y-%m-%d")  # Sunday of the current week
        
        conn = sqlite3.connect("joy_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT description, joy_level, date FROM joy_moments
        WHERE user_id = ? AND date BETWEEN ? AND ?
        """, (self.user_id, start_date, end_date))
        
        joy_moments = cursor.fetchall()
        conn.close()

        print(f"Weekly Summary from {start_date} to {end_date}:")
        for moment in joy_moments:
            print(f"Date: {moment[2]}, Joy Level: {moment[1]}, Description: {moment[0]}")

    def generate_monthly_trend(self):
        today = datetime.now()
        first_day_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        
        conn = sqlite3.connect("joy_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT date, joy_level FROM joy_moments
        WHERE user_id = ? AND date >= ?
        """, (self.user_id, first_day_of_month))
        
        joy_moments = cursor.fetchall()
        conn.close()

        joy_levels = [moment[1] for moment in joy_moments]
        dates = [moment[0] for moment in joy_moments]
        
        if joy_levels:
            print(f"Monthly Trend for the month starting {first_day_of_month}:")
            for date, level in zip(dates, joy_levels):
                print(f"Date: {date}, Joy Level: {level}")
        else:
            print("No joy moments recorded this month.")

    def plot_monthly_trend(self):
        today = datetime.now()
        first_day_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        
        conn = sqlite3.connect("joy_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT date, joy_level FROM joy_moments
        WHERE user_id = ? AND date >= ?
        """, (self.user_id, first_day_of_month))
        
        joy_moments = cursor.fetchall()
        conn.close()

        joy_levels = [moment[1] for moment in joy_moments]
        dates = [moment[0] for moment in joy_moments]

        if joy_levels:
            plt.plot(dates, joy_levels)
            plt.title("Monthly Joy Trend")
            plt.xlabel("Date")
            plt.ylabel("Joy Level (1-10)")
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("No joy moments recorded this month to plot.")

    def add_goal(self):
        goal_description = input("Enter your goal description: ")
        timeline = input("Enter the goal timeline (e.g., 2025-12-31): ")
        
        conn = sqlite3.connect("joy_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO goals (user_id, timeline, goal_description)
        VALUES (?, ?, ?)
        """, (self.user_id, timeline, goal_description))
        conn.commit()
        conn.close()
        print(f"Goal '{goal_description}' added!")

    def view_goals(self):
        conn = sqlite3.connect("joy_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, goal_description, timeline, progress FROM goals
        WHERE user_id = ?
        """, (self.user_id,))
        
        goals = cursor.fetchall()
        conn.close()

        print("Your Goals:")
        for goal in goals:
            print(f"Goal: {goal[1]}, Timeline: {goal[2]}, Progress: {goal[3]}%")

    def track_goal_progress(self, goal_id):
        progress = int(input("Enter your progress for this goal (0-100): "))
        
        conn = sqlite3.connect("joy_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE goals
        SET progress = ?
        WHERE id = ?
        """, (progress, goal_id))
        conn.commit()
        conn.close()
        print(f"Progress for goal {goal_id} updated to {progress}%.")

    def get_joy_moments(self):
        conn = sqlite3.connect('joy_tracker.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, description, joy_level, timestamp FROM joy_moments WHERE user_id=? ORDER BY timestamp ASC",
            (self.user_id,)
        )
        moments = cursor.fetchall()
        conn.close()
        return moments

# Register function to add new users
def register():
    conn = sqlite3.connect("joy_tracker.db")
    cursor = conn.cursor()

    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different username.")
        conn.close()
        return

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    print(f"User {username} registered successfully!")

# Login function to authenticate users
def login():
    conn = sqlite3.connect("joy_tracker.db")
    cursor = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the username and password match a record in the database
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome back, {username}!")
        conn.close()
        return user[0]  # Return the user ID
    else:
        print("Invalid username or password. Please try again.")
        conn.close()
        return None

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

# Main workflow
def main():
    setup_database()
    print("Welcome to the Joy Tracker!")
    user_id = None
    joy_tracker = None

    while True:
        print("""
        1. Register
        2. Login
        3. Add Joy Moment
        4. View Joy Moments
        5. Add Contribution
        6. View Contributions
        7. Add Goal
        8. View Goals
        9. Track Goal Progress
        10. View Weekly Summary
        11. View Monthly Trend
        12. Plot Monthly Trend
        13. Exit
        """)
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            if user_id:
                joy_tracker = JoyTracker(user_id)  # Create JoyTracker instance after login
        elif choice == "3" and joy_tracker:
            description = input("Enter a description for the joy moment: ")
            joy_level = int(input("Enter the joy level (1-10): "))
            # When saving a moment
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            joy_tracker.add_joy_moment(description, joy_level, timestamp)
        elif choice == "10" and joy_tracker:
            joy_tracker.generate_weekly_summary()
        elif choice == "11" and joy_tracker:
            joy_tracker.generate_monthly_trend()
        elif choice == "12" and joy_tracker:
            joy_tracker.plot_monthly_trend()
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid choice or please login first.")

if __name__ == "__main__":
    main()
