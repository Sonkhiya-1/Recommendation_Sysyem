def get_discard_list(cursor):
    cursor.execute("""
        SELECT mi.id, mi.name, mi.average_rating, 
               GROUP_CONCAT(DISTINCT f.comment SEPARATOR '; ') as sentiments
        FROM menu_items mi
        LEFT JOIN feedback f ON mi.id = f.menu_item_id AND f.sentiment = 'negative'
        WHERE mi.average_rating < 2
        GROUP BY mi.id, mi.name, mi.average_rating
    """)
    return cursor.fetchall()

def delete_menu_item(cursor, item_id):
    cursor.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
