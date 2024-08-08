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

def get_feedback_questions(cursor):
    cursor.execute("SELECT * FROM feedback_questions")
    return cursor.fetchall()

def insert_feedback_response(cursor, user_id, question_id, response):
    cursor.execute(
        "INSERT INTO feedback_responses (user_id, question_id, response) VALUES (%s, %s, %s)",
        (user_id, question_id, response)
    )

def get_feedback_responses(cursor):
    cursor.execute("""
        SELECT fr.id, u.employee_id, fq.question, fr.response
        FROM feedback_responses fr
        JOIN feedback_questions fq ON fr.question_id = fq.id
        JOIN users u ON fr.user_id = u.id
        ORDER BY fr.id
    """)
    return cursor.fetchall()
