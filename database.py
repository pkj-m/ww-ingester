import psycopg2
from config import load_config
import asyncio


def connect(config):
    """ Connect to the PostgresSQL database server """

    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to PostgresSQL database')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def write_event(event):
    """ Inserts a new string into the events table in the database """

    sql = """INSERT INTO events (body)
    VALUES(%s) RETURNING id"""

    event_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute INSERT statement
                print("attempting to save to db: ", event)
                cur.execute(sql, (event,))
                rows = cur.fetchone()
                if rows:
                    event_id = rows[0]

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return event_id


if __name__ == '__main__':
    config = load_config()
    connect(config)
