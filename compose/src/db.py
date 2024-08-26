import psycopg2
import os

TABLE_NAME = 'descriptions'


def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
    )
    return conn


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        prompt TEXT,
        image_name TEXT,
        description TEXT);
    ''')
    conn.commit()
    cur.close()
    conn.close()


def get_description(image_name, prompt):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''
    SELECT description FROM {TABLE_NAME} WHERE image_name = '{image_name}' AND prompt = '{prompt}';
    ''')
    description = cur.fetchone()
    cur.close()
    conn.close()
    return description


def get_all_descriptions(image_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''
    SELECT prompt, description FROM {TABLE_NAME} WHERE image_name = '{image_name}';
    ''')
    descriptions = {prompt: description for prompt, description in cur.fetchall()}
    cur.close()
    conn.close()
    return descriptions


def save_description(prompt, image_name, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''
    INSERT INTO {TABLE_NAME} (prompt, image_name, description)
    VALUES (%s, %s, %s);
    ''', (prompt, image_name, description))
    conn.commit()
    cur.close()
    conn.close()
