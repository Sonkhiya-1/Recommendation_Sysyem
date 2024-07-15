def get_user_by_credentials(cursor, employee_id, password):
    cursor.execute("SELECT * FROM users WHERE employee_id=%s AND password=%s", (employee_id, password))
    return cursor.fetchone()

def replace_user_preferences(cursor, user_id, preferences):
    cursor.execute(
        """
        REPLACE INTO user_preferences (user_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, preferences['dietary_preference'], preferences['spice_level'], preferences['cuisine_preference'], preferences['sweet_tooth'])
    )
