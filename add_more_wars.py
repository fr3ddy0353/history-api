import sqlite3

def add_new_wars():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    new_events = [
        ("Franco-Prussian War",),
        ("War of the Spanish Succession",),
        ("French Revolutionary Wars",),
        ("Napoleonic Wars",),
        ("Algerian War",),
        ("Spanish-American War",),
        ("Mexican-American War",),
        ("Chilean War of Independence",),
        ("Peninsular War",),
        ("Spanish Civil War",),
        ("Guatemalan Civil War",)
    ]

    # Insert new wars into events table
    c.executemany('INSERT OR IGNORE INTO events (name) VALUES (?)', new_events)
    conn.commit()

    # Get event IDs for the inserted wars
    c.execute('SELECT id, name FROM events WHERE name IN ({})'.format(
        ','.join('?' for _ in new_events)), [e[0] for e in new_events])
    event_ids = {name: id for id, name in c.fetchall()}

    # Prepare sections for each war - title + content pairs
    sections_data = {
        "Franco-Prussian War": [
            ("Dates", "1870-1871"),
            ("Overview", "A conflict between the Second French Empire and the Kingdom of Prussia which resulted in the unification of Germany."),
            ("Key Battles", "Battle of Sedan, Siege of Paris"),
            ("Significance", "Led to the downfall of Napoleon III and major shift in European power.")
        ],
        "War of the Spanish Succession": [
            ("Dates", "1701-1714"),
            ("Overview", "War over who would succeed to the Spanish throne, involving most European powers."),
            ("Key Battles", "Battle of Blenheim, Battle of Ramillies"),
            ("Significance", "Changed the balance of power in Europe significantly.")
        ],
        "French Revolutionary Wars": [
            ("Dates", "1792-1802"),
            ("Overview", "Wars sparked by the French Revolution spreading across Europe."),
            ("Key Battles", "Battle of Valmy, Siege of Toulon"),
            ("Significance", "Ended with the rise of Napoleon Bonaparte.")
        ],
        "Napoleonic Wars": [
            ("Dates", "1803-1815"),
            ("Overview", "Series of wars led by Napoleon Bonaparte against various European coalitions."),
            ("Key Battles", "Battle of Austerlitz, Battle of Waterloo"),
            ("Significance", "Reshaped European borders and power.")
        ],
        "Algerian War": [
            ("Dates", "1954-1962"),
            ("Overview", "War of independence fought between France and Algerian Nationalists."),
            ("Key Battles", "Battle of Algiers"),
            ("Significance", "Led to Algerian independence and end of French colonial rule.")
        ],
        "Spanish-American War": [
            ("Dates", "1898"),
            ("Overview", "Conflict between Spain and the United States resulting in the end of Spanish colonial rule in the Americas."),
            ("Key Battles", "Battle of San Juan Hill, Battle of Manila Bay"),
            ("Significance", "Marked the emergence of the US as a global power.")
        ],
        "Mexican-American War": [
            ("Dates", "1846-1848"),
            ("Overview", "War between the United States and Mexico over territorial disputes."),
            ("Key Battles", "Battle of Palo Alto, Battle of Chapultepec"),
            ("Significance", "Resulted in the US acquiring large territories in the southwest.")
        ],
        "Chilean War of Independence": [
            ("Dates", "1810-1826"),
            ("Overview", "Struggle for independence from Spanish colonial rule."),
            ("Key Battles", "Battle of Maipú"),
            ("Significance", "Established Chile as an independent nation.")
        ],
        "Peninsular War": [
            ("Dates", "1807-1814"),
            ("Overview", "Napoleon's invasion of Spain and Portugal."),
            ("Key Battles", "Battle of Bailén, Battle of Vitoria"),
            ("Significance", "Weakened Napoleon's forces and boosted Spanish nationalism.")
        ],
        "Spanish Civil War": [
            ("Dates", "1936-1939"),
            ("Overview", "Conflict between Republicans and Nationalists."),
            ("Key Battles", "Battle of Madrid, Battle of the Ebro"),
            ("Significance", "Led to Franco's dictatorship and was a prelude to WWII.")
        ],
        "Guatemalan Civil War": [
            ("Dates", "1960-1996"),
            ("Overview", "Internal conflict between the government and leftist insurgents."),
            ("Key Battles", "Numerous guerrilla actions and counterinsurgency campaigns"),
            ("Significance", "Devastated Guatemala with human rights abuses on both sides.")
        ],
    }

    # Insert sections for each event
    for war_name, sections in sections_data.items():
        event_id = event_ids.get(war_name)
        if event_id:
            for title, content in sections:
                c.execute('INSERT INTO event_sections (event_id, section_title, content) VALUES (?, ?, ?)',
                          (event_id, title, content))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_new_wars()
    print("New wars added to database.")