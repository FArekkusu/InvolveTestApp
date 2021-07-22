import sqlite3

DATABASE = "test.db"

PAYMENT_REQUESTS = "payment_requests"

CREATE_PAYMENT_REQUESTS = f"""
CREATE TABLE IF NOT EXISTS {PAYMENT_REQUESTS} (
    id INTEGER PRIMARY KEY,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount TEXT NOT NULL,
    currency INTEGER NOT NULL,
    description TEXT NOT NULL,
    shop_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL
);
"""
DROP_PAYMENT_REQUESTS = f"""
DROP TABLE IF EXISTS {PAYMENT_REQUESTS};
"""
INSERT_PAYMENT_REQUEST = f"""
INSERT INTO {PAYMENT_REQUESTS} (amount, currency, description, shop_id, order_id)
VALUES (?, ?, ?, ?, ?);
"""


def create_tables():
    with sqlite3.connect(DATABASE) as con:
        con.execute(CREATE_PAYMENT_REQUESTS)
        con.commit()


def drop_tables():
    with sqlite3.connect(DATABASE) as con:
        con.execute(DROP_PAYMENT_REQUESTS)
        con.commit()


def insert_payment_request(amount, currency, description, shop_id, order_id):
    with sqlite3.connect(DATABASE) as con:
        try:
            cursor = con.cursor()
            cursor.execute(INSERT_PAYMENT_REQUEST, (amount, currency, description, shop_id, order_id))
            con.commit()
        finally:
            cursor.close()


def log_prqs():
    with sqlite3.connect(DATABASE) as con:
        try:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM payment_requests")
            for x in cursor.fetchall():
                print(x)
            con.commit()
        finally:
            cursor.close()