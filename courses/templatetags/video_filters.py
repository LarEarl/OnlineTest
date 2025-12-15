import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def youtube_id(url):
    """
    Извлекает ID видео из различных форматов YouTube URL
    Поддерживает:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if not url:
        return ''
    
    # Паттерн для youtube.com/watch?v=
    watch_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
    match = re.search(watch_pattern, url)
    if match:
        return match.group(1)
    
    # Паттерн для youtu.be/
    short_pattern = r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)'
    match = re.search(short_pattern, url)
    if match:
        return match.group(1)
    
    # Паттерн для youtube.com/embed/
    embed_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
    match = re.search(embed_pattern, url)
    if match:
        return match.group(1)
    
    # Если ничего не найдено, возвращаем пустую строку
    return ''


@register.filter
def youtube_embed_url(video_id):
    """
    Создает URL для встраивания YouTube с безопасными параметрами.
    """
    if not video_id:
        return ''

    params = {
        'modestbranding': '1',
        'rel': '0',
        'controls': '1',
        'fs': '1',
        'enablejsapi': '1',
    }
    query = '&'.join([f"{k}={v}" for k, v in params.items()])
    return f'https://www.youtube.com/embed/{video_id}?{query}'


@register.filter
def is_youtube(url):
    """
    Проверяет, является ли URL ссылкой на YouTube
    """
    if not url:
        return False
    return bool(re.search(r'youtube\.com|youtu\.be', url))
