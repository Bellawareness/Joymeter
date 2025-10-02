# Joy Tracker

Joy Tracker is a web application designed to help you log, reflect on, and celebrate moments of joy in your life. Built with Python and Flask, it provides a simple interface for tracking joyful experiences, setting goals, and fostering a positive mindset.

## Features

- **Log Joyful Moments:** Record daily moments that bring you happiness.
- **View Joy History:** Reflect on your past joyful entries.
- **Set and Track Goals:** Define personal goals and monitor your progress.
- **Feedback:** Share your thoughts and suggestions to improve the app.

## Getting Started

### Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)
- Flask

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/joy_tracker.git
    cd joy_tracker
    ```

2. **Install dependencies:**
    ```bash
    pip install flask
    ```

3. **Project Structure:**
    ```
    joy_tracker/
    ├── [app.py](http://_vscodecontentref_/0)
    ├── [joy_tracker.py](http://_vscodecontentref_/1)
    ├── static/
    │   ├── images/
    │   │   └── glass.png
    │   └── styles.css
    └── templates/
        ├── home.html
        ├── about.html
        ├── login.html
        ├── feedback.html
        ├── add_joy_moment.html
        ├── view_joy_moments.html
        ├── add_goal.html
        └── view_goals.html
    ```

### Running the App

1. **Set the Flask app environment variable:**
    ```bash
    export FLASK_APP=app.py
    ```

2. **Run the Flask development server:**
    ```bash
    flask run
    ```
    python3 app.py

3. **Open your browser and go to:**
    ```
    python3.8 -m venv venv
    source venv/bin/activate    ```

## Usage

- **Home:** Overview and navigation.
- **About:** Learn more about the app.
- **Login:** Access your personalized joy tracker.
- **Feedback:** Submit suggestions or report issues.
- **Add/View Joy Moments & Goals:** Use the navigation to log and view your entries.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

---

