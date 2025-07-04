from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('history.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    events = conn.execute('SELECT id, name FROM events ORDER BY name').fetchall()
    event_id = request.args.get('event_id')
    selected_event = None
    sections = []
    if event_id:
        selected_event = conn.execute('SELECT id, name FROM events WHERE id = ?', (event_id,)).fetchone()
        sections = conn.execute('SELECT section_title, content FROM event_sections WHERE event_id = ?', (event_id,)).fetchall()
    conn.close()
    return render_template('index.html', events=events, selected_event=selected_event, sections=sections)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


if __name__ == '__main__':
    app.run(debug=True)