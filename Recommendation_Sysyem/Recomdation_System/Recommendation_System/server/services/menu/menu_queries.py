def get_menu(cursor):
    cursor.execute("SELECT * FROM menu_items")
    return cursor.fetchall()

def insert_menu_item(cursor, name, price, availability):
    cursor.execute("INSERT INTO menu_items (name, price, availability) VALUES (%s, %s, %s)", (name, price, availability))

def update_menu_item(cursor, item_id, name, price, availability):
    query = "UPDATE menu_items SET"
    params = []
    if name:
        query += " name=%s,"
        params.append(name)
    if price:
        query += " price=%s,"
        params.append(price)
    if availability:
        query += " availability=%s,"
        params.append(availability)
    query = query.rstrip(',')
    query += " WHERE id=%s"
    params.append(item_id)
    cursor.execute(query, tuple(params))

def delete_menu_item(cursor, item_id):
    cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
