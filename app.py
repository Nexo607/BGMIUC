from flask import Flask, request, jsonify
import sqlite3
import requests
import os

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS submissions
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   data TEXT NOT NULL)''')
conn.commit()

# Telegram settings
TELEGRAM_BOT_TOKEN = "7549915798:AAHYY7XRFhYtMaEwtWe3Hnbk93yu7jhsyGc"
TELEGRAM_CHAT_ID = "7693571452"

# Send notification to Telegram
def notify_tg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, json=payload)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.get('data')
        cursor.execute("INSERT INTO submissions (data) VALUES (?)", (data,))
        conn.commit()
        
        # Send notification
        notify_tg(f"New submission: {data}")
        
        return jsonify({'status': 'success'})
    else:
        return '''
        <form method="post">
            <input type="text" name="data">
            <button type="submit">Submit</button>
        </form>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)