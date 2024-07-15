def get_menu(cursor):
    cursor.execute("SELECT * FROM menu_items")
    return cursor.fetchall()

def insert_menu_item(cursor, name, price, availability, dietary_category,spice_level, is_sweet):
    cursor.execute("INSERT INTO menu_items (name, price, availability, dietary_category, spice_level, is_sweet) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, availability, dietary_category, spice_level, is_sweet))

def update_menu_item(cursor, item_id, name, price, availability, dietary_category, spice_level, is_sweet):
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
    if dietary_category:
        query += " dietary_category=%s,"
        params.append(dietary_category)
    if spice_level:
        query += " spice_level=%s,"
        params.append(spice_level)
    if is_sweet is not None:
        query += " is_sweet=%s,"
        params.append(is_sweet)
    query = query.rstrip(',')
    query += " WHERE id=%s"
    params.append(item_id)
    cursor.execute(query, tuple(params))

def delete_menu_item(cursor, item_id):
    cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
