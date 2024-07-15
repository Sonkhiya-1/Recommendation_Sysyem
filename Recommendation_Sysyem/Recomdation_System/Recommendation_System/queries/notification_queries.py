def get_notifications(cursor, user_id):
    cursor.execute("SELECT * FROM notifications WHERE user_id=%s AND viewed=FALSE", (user_id,))
    return cursor.fetchall()

def mark_notifications_as_viewed(cursor, user_id):
    cursor.execute("UPDATE notifications SET viewed=TRUE WHERE user_id=%s AND viewed=FALSE", (user_id,))

def get_rollout_items(cursor):
    cursor.execute("""
        SELECT ri.menu_item_id, mi.name, mi.dietary_category, mi.spice_level, mi.is_sweet, mi.average_rating, ri.price, ri.timestamp
        FROM rollout_items ri
        JOIN menu_items mi ON ri.menu_item_id = mi.id
        WHERE ri.timestamp = (
            SELECT MAX(timestamp)
            FROM rollout_items
            WHERE chosen = TRUE
        )
    """)
    return cursor.fetchall()

def insert_notification(cursor, user_id, message):
    cursor.execute("INSERT INTO notifications (user_id, message, viewed) VALUES (%s, %s, %s)", (user_id, message, False))

def get_employee_ids(cursor):
    cursor.execute("SELECT id FROM users WHERE role = 3")
    return cursor.fetchall()

