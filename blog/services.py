from django.core.cache import cache
from blog.models import Post
from config.settings import CACHE_ENABLED


def get_posts_from_cache():
    if not CACHE_ENABLED:
        return Post.objects.filter(is_published=True)

    key = 'published_posts_list'
    posts = cache.get(key)
    if posts is not None:
        return posts

    posts = Post.objects.filter(is_published=True)
    cache.set(key, posts, timeout=60 * 15)  # Кешируем на 15 минут
    return posts
