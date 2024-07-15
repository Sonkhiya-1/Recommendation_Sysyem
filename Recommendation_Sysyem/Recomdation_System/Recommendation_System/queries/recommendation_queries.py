def get_user_preferences(cursor, user_id):
    cursor.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

def get_recommendations(cursor):
    cursor.execute("""
        SELECT mi.id, mi.name, mi.price, mi.average_rating, mi.dietary_category, mi.spice_level, mi.is_sweet
        FROM menu_items mi
        ORDER BY mi.average_rating DESC
        LIMIT 5
    """)
    return cursor.fetchall()

def get_menu_item_price(cursor, menu_item_id):
    cursor.execute("SELECT price FROM menu_items WHERE id=%s", (menu_item_id,))
    return cursor.fetchone()

def insert_rollout_item(cursor, menu_item_id, chef_id, price, timestamp):
    cursor.execute("INSERT INTO rollout_items (menu_item_id, chef_id, chosen, price, timestamp) VALUES (%s, %s, %s, %s, %s)",
                   (menu_item_id, chef_id, True, price, timestamp))
