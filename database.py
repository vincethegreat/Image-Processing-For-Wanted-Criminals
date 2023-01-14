import sqlite3

def create_database():
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS records (
                name text,
                gender text,
                alleged_offense text
                )""")
    conn.commit()
    conn.close()

def insert_data_to_database(name, gender, alleged_offense):
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("INSERT INTO records VALUES (?, ?, ?)", (name, gender, alleged_offense))
    conn.commit()
    conn.close()

def update_data(name, gender, alleged_offense):
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("UPDATE records SET gender = ?, alleged_offense = ? WHERE name = ?", (gender, alleged_offense, name))
    conn.commit()
    conn.close()

def delete_data(name):
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def fetch_all_records():
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    records = c.fetchall()
    conn.close()
    return records

