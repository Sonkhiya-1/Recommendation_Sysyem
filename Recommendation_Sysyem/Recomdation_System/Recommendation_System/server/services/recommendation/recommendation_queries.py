def get_user_preferences(cursor, user_id):
    cursor.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

def get_recommendations(cursor):
    cursor.execute("""
        SELECT mi.id, mi.name, mi.price, mi.average_rating, mi.dietary_category, mi.spice_level, mi.is_sweet, mi.meal_type
        FROM menu_items mi
        ORDER BY mi.average_rating DESC
    """)
    return cursor.fetchall()

def get_menu_item_price(cursor, menu_item_id):
    cursor.execute("SELECT price FROM menu_items WHERE id=%s", (menu_item_id,))
    return cursor.fetchone()

def get_menu_item_price_and_meal_type(cursor, menu_item_id):
    cursor.execute("SELECT price, meal_type FROM menu_items WHERE id=%s", (menu_item_id,))
    return cursor.fetchone()

def insert_rollout_item(cursor, menu_item_id, chef_id, price, timestamp, meal_type):
    cursor.execute(
        "INSERT INTO rollout_items (menu_item_id, chef_id, chosen, price, timestamp, meal_type) VALUES (%s, %s, %s, %s, %s, %s)",
        (menu_item_id, chef_id, True, price, timestamp, meal_type)
    )