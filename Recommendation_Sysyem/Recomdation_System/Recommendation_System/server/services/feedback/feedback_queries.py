def insert_feedback(cursor, user_id, comment, sentiment_type, item_id):
    cursor.execute(
        "INSERT INTO feedback (user_id, comment, sentiment, menu_item_id) VALUES (%s, %s, %s, %s)",
        (user_id, comment, sentiment_type, item_id)
    )

def get_feedback_counts(cursor, item_id):
    cursor.execute(
        """
        SELECT sentiment, COUNT(*) as count 
        FROM feedback 
        WHERE menu_item_id = %s 
        GROUP BY sentiment
        """,
        (item_id,)
    )
    return cursor.fetchall()

def update_average_rating(cursor, item_id, avg_rating):
    cursor.execute("UPDATE menu_items SET average_rating = %s WHERE id = %s", (avg_rating, item_id))
