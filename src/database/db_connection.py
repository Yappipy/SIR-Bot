import sqlite3
import csv

def initialize_database():
    conn = sqlite3.connect('bot_database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    uid INTEGER PRIMARY KEY,
                    username TEXT,
                    discord_id INTEGER UNIQUE
                 )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS buildings (
                    name TEXT PRIMARY KEY,
                    tier TEXT,
                    max_level INTEGER,
                    set_name TEXT
                 )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS building_values (
                    level INTEGER PRIMARY KEY,
                    upgrade_cost TEXT,
                    cumulative_cost INTEGER,
                    blue_value INTEGER,
                    purple_value INTEGER,
                    gold_value INTEGER
                 )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS player_buildings (
                    uid INTEGER,
                    building_name TEXT,
                    current_level INTEGER,
                    PRIMARY KEY (uid, building_name),
                    FOREIGN KEY (uid) REFERENCES users(uid),
                    FOREIGN KEY (building_name) REFERENCES buildings(name)
                 )''')

    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('bot_database.db')

# Populate table with CSV data
def import_csv_to_database(table_name, csv_filepath):
    conn = get_db_connection()
    c = conn.cursor()

    with open(csv_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Insert data based on table name
        if table_name == 'buildings':
            for row in reader:
                if 'Set' in row:
                    c.execute('''
                        INSERT OR IGNORE INTO buildings (name, tier, max_level, set_name)
                        VALUES (?, ?, ?, ?)
                    ''', (row['Building'], row['Tier'], row['Max Level'], row['Set']))
                else:
                    c.execute('''
                        INSERT OR IGNORE INTO buildings (name, tier, max_level)
                        VALUES (?, ?, ?)
                    ''', (row['Building'], row['Tier'], row['Max Level']))
        
        elif table_name == 'building_values' :
            for row in reader:
                c.execute(f'''
                    INSERT OR IGNORE INTO building_values (level, upgrade_cost, cumulative_cost, blue_value, purple_value, gold_value)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['level'], row['upgrade'], row['cumulative'], row['blue value'], row['purple value'], row['gold value']))
    
    conn.commit()
    conn.close()
