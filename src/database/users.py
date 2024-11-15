from src.database.db_connection import get_db_connection


# Check if user is registered
def is_user_registered(discord_id):
    conn = get_db_connection()
    c = conn.cursor()

    # Check if the user exists
    c.execute('SELECT uid FROM users WHERE discord_id = ?', (discord_id,))
    user = c.fetchone()

    conn.close()
    return user is not None

def add_or_update_user(discord_id, username, uid):
    conn = get_db_connection()
    c = conn.cursor()

    # Insert or update the user with the discord_id
    c.execute('''
        INSERT INTO users (uid, username, discord_id)
        VALUES (?, ?, ?)
        ON CONFLICT(uid) DO UPDATE SET discord_id=excluded.discord_id, username=excluded.username
    ''', (uid, username, discord_id))

    conn.commit()
    conn.close()