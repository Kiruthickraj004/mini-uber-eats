from django.core.cache import cache


def restaurant_menu_cache_key(restaurant_id):
    return f"menu:restaurant:{restaurant_id}"


def invalidate_restaurant_menu(restaurant_id):
    cache.delete(
        restaurant_menu_cache_key(restaurant_id)
    )