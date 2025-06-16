import sqlite3
import wikipediaapi
import datetime

wars_to_fetch = [
    "Russo-Ukrainian War",
    "Syrian Civil War",
    "War on Terror",
    "Iraq War",
    "Libyan Civil War",
    "Afghanistan conflict (1978–present)",
    "Yom Kippur War",
    "Six-Day War",
    "Iran–Iraq War",
    "Bosnian War",
    "Kosovo War"
]

def fetch_summary(title):
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='history-api-bot/1.0 (frederick@example.com)'
    )
    page = wiki.page(title)
    return page.summary if page.exists() else None

def update_database():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()

    for war in wars_to_fetch:
        summary = fetch_summary(war)
        if not summary:
            print(f"⚠️ Could not fetch: {war}")
            continue

        cursor.execute('SELECT 1 FROM events WHERE name = ?', (war,))
        if cursor.fetchone():
            print(f"🔁 Already in DB: {war}")
            continue

        today = datetime.date.today().isoformat()
        cursor.execute(
            'INSERT INTO events (name, start_date, end_date, location) VALUES (?, ?, ?, ?)',
            (war, today, "", "Various")
        )
        event_id = cursor.lastrowid
        cursor.execute(
            'INSERT INTO event_sections (event_id, section_title, content) VALUES (?, ?, ?)',
            (event_id, "Overview", summary)
        )
        print(f"✅ Added: {war}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_database()
