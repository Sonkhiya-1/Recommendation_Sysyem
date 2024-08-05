def filter_and_sort_recommendations(recommendations, preferences, min_items):
    dietary_order = {
        'Vegetarian': 1,
        'Eggetarian': 2,
        'Non Vegetarian': 3
    }

    filtered_recommendations = [
        item for item in recommendations 
        if matches_dietary_preference(item, preferences['dietary_preference'])
    ]

    sorted_recommendations = sorted(filtered_recommendations, key=lambda item: (
        dietary_order.get(item['dietary_category'], 4),
        spice_level_score(item['spice_level'], preferences['spice_level']),
        not item['is_sweet'] if preferences['sweet_tooth'] else item['is_sweet'],
        -item['average_rating'],
        item['price']
    ))

    return limit_items_per_meal_type(sorted_recommendations, min_items)

def matches_dietary_preference(item, preference):
    if preference == 'Vegetarian' and item['dietary_category'] == 'Vegetarian':
        return True
    if preference == 'Eggetarian' and item['dietary_category'] in ['Vegetarian', 'Eggetarian']:
        return True
    if preference == 'Non Vegetarian':
        return True
    return False

def spice_level_score(item_spice, preferred_spice):
    spice_levels = {'Low': 1, 'Medium': 2, 'High': 3}
    return abs(spice_levels.get(item_spice, 2) - spice_levels.get(preferred_spice, 2))

def limit_items_per_meal_type(recommendations, min_items):
    meal_types = ['breakfast', 'lunch', 'dinner']
    result = []
    for meal_type in meal_types:
        items = [item for item in recommendations if item['meal_type'] == meal_type]
        result.extend(items[:min_items])
    return result
