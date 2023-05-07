import sqlite3, random, datetime
from config.classes import Product, Client, Order


def getNewId():
    return random.getrandbits(28)

def connect():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, name STRING, quantity INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name STRING)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, client_id STRING, items STRING)")
    conn.commit()
    conn.close()

# ---- INVENTORY Operations ----
def insert_product(product):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO inventory VALUES (?,?,?)", (
        product.id,
        product.name,
        product.quantity
    ))
    conn.commit()
    conn.close()


def view_inventory():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    rows = cur.fetchall()
    products = []

    for i in rows:
        product = Product(i[0], i[1], i[2])
        products.append(product)

    conn.close()

    return products


def view_product(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory WHERE id=?", (id))
    rows = cur.fetchall()
    products = []

    for i in rows:
        product = Product(i[0], True if i[1] == 1 else False, i[2], i[3])
        products.append(product)

    conn.close()

    return products


def update_product(product):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE inventory SET quantity=?, name=? WHERE id=?", (product.quantity, product.name, product.id))
    conn.commit()
    conn.close()


def delete_product(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory WHERE id=?", (id,))
    conn.commit()
    conn.close()


def delete_all_products():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory")
    conn.commit()
    conn.close()


# ---- CLIENT operations ----
def insert_client(client):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO clients VALUES (?,?)", (
        client.id,
        client.name
    ))
    conn.commit()
    conn.close()


def view_clients():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    clients = []

    for i in rows:
        client = Product(i[0], i[1])
        clients.append(client)

    conn.close()

    return client


def view_client(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE id=?", (id))
    rows = cur.fetchall()
    clients = []

    for i in rows:
        client = Client(i[0], i[1])
        clients.append(client)

    conn.close()

    return clients


def update_client(client):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE clients SET name=? WHERE id=?", (client.name, client.id))
    conn.commit()
    conn.close()


def delete_client(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id=?", (id,))
    conn.commit()
    conn.close()


def delete_all_clients():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM clients")
    conn.commit()
    conn.close()


# ---- Order methods ----
def insert_order(client):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO orders VALUES (?,?,?)", (
        client.id,
        client.client_id,
        client.items
    ))
    conn.commit()
    conn.close()


def view_orders():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    orders = []

    for i in rows:
        order = Order(i[0], i[1])
        orders.append(order)

    conn.close()

    return order


def view_client(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (id))
    rows = cur.fetchall()
    orders = []

    for i in rows:
        order = Order(i[0], i[1])
        orders.append(order)

    conn.close()

    return orders


def update_client(client):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE orders SET client_id=? WHERE id=?", (client.client_id, client.id))
    conn.commit()
    conn.close()


def delete_client(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()


def delete_all_clients():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM orders")
    conn.commit()
    conn.close()

