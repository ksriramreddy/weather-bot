import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
def init_db():
    try:
        connect = psycopg2.connect(DATABASE_URL)
        cursor = connect.cursor()
        cursor.execute("""
                create table if not exists users(
                    id serial,
                    telegram_id bigint unique,
                    username text,
                    is_blocked boolean default false
                    )
        """)
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        print(f"Error connecting database {e}")

def add_subscription(telegram_id,first_name):
    connect  = psycopg2.connect(DATABASE_URL)
    cursor = connect.cursor()
    cursor.execute("""
        insert into users (telegram_id,username) values(%s,%s) on conflict (telegram_id) do nothing;
    """,(telegram_id,first_name))
    connect.commit()
    cursor.close()
    connect.close()

def remove_subscription(telegram_id):
    connect = psycopg2.connect(DATABASE_URL)
    cursor = connect.cursor()
    cursor.execute("""
        delete from users where telegram_id = %s    
    """,(telegram_id,))

def block_user(telegram_id):
    connect = psycopg2.connect(DATABASE_URL)
    cursor = connect.cursor()
    cursor.execute("""
            update users set is_blocked = true
            where telegram_id = %s
    """,(telegram_id))
    connect.commit()
    cursor.close()
    connect.close()


def unblock_user(telegram_id):
    connect = psycopg2.connect(DATABASE_URL)
    cursor = connect.cursor()
    cursor.execute("""
            update users set is_blocked = false
            where telegram_id = %s
    """,(telegram_id))
    connect.commit()
    cursor.close()
    connect.close()

def all_users():
    connect = psycopg2.connect(DATABASE_URL)
    cursor = connect.cursor()
    cursor.execute("""
        select telegram_id from users where is_blocked = false    
    """)
    return cursor.fetchall()