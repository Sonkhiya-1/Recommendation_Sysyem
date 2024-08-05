import datetime
def insert_vote(cursor, menu_item_id, user_id, meal_type):
    now = datetime.datetime.now()
    cursor.execute("INSERT INTO votes (menu_item_id, user_id, meal_type, voted_at) VALUES (%s, %s, %s, %s)", (menu_item_id, user_id, meal_type, datetime.datetime.now()))

def get_vote_counts(cursor, today):
    cursor.execute("""
        SELECT mi.name, v.meal_type, COUNT(v.id) as vote_count
        FROM votes v
        JOIN menu_items mi ON v.menu_item_id = mi.id
        JOIN rollout_items ri ON ri.menu_item_id = mi.id
        WHERE DATE(v.voted_at) = %s AND DATE(ri.timestamp) = %s AND ri.chosen = TRUE
        GROUP BY mi.name, v.meal_type
    """, (today, today))
    return cursor.fetchall()
