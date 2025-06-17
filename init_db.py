import sqlite3
import wikipediaapi

# Major wars plus less common French and Hispanic wars
wars = [
    "World War II",
    "World War I",
    "Vietnam War",
    "Korean War",
    "American Civil War",
    "Napoleonic Wars",
    "Crimean War",
    "Franco-Prussian War",
    "Russo-Japanese War",
    "Spanish Civil War",
    "Gulf War",
    "Iraq War",
    "Syrian Civil War",
    "Russian Civil War",
    "Bosnian War",
    "Yugoslav Wars",
    "Falklands War",
    "War in Afghanistan (2001–2021)",
    "Iran–Iraq War",
    "Six-Day War",
    "Yom Kippur War",
    "Thirty Years' War",
    "Hundred Years' War",
    "Peloponnesian War",
    "Punic Wars",
    # Added less common wars
    "French Revolutionary Wars",
    "Franco-Dutch War",
    "War of the Spanish Succession",
    "Mexican-American War",
    "Chaco War",
    "War of the Triple Alliance",
    "Colombian Civil War",
]

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='HistoryApp/1.0 (frederick@example.com)'
)

def get_sections(page, sections_dict):
    """Recursively extract all sections and subsections."""
    for sec in page.sections:
        sections_dict[sec.title] = sec.text
        if sec.sections:
            get_sections(sec, sections_dict)

def fetch_war_details(title):
    page = wiki.page(title)
    if not page.exists():
        return None

    details = {"Overview": page.summary}
    get_sections(page, details)
    return details

def init_db():
    conn = sqlite3.connect('history.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS events')
    cur.execute('DROP TABLE IF EXISTS event_sections')
    cur.execute('''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE event_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            section_title TEXT,
            content TEXT,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
    ''')
    conn.commit()
    conn.close()

def populate_db():
    conn = sqlite3.connect('history.db')
    cur = conn.cursor()
    for title in wars:
        print(f"Fetching: {title} ...")
        details = fetch_war_details(title)
        if not details:
            print(f"⚠️ Skipping: {title} (not found)")
            continue
        cur.execute('INSERT INTO events (name) VALUES (?)', (title,))
        eid = cur.lastrowid
        for sec_title, content in details.items():
            cur.execute(
                'INSERT INTO event_sections (event_id, section_title, content) VALUES (?, ?, ?)',
                (eid, sec_title, content[:10000])  # cap to 10k chars
            )
        print(f"✅ Loaded {title}: {len(details)} sections")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    populate_db()