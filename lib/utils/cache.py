import os

cache_dir = 'lib/cache'

# Ensure cache directory exists
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

def get_cache_file_path(transcript_hash):
    return f'{cache_dir}/{transcript_hash}.txt'

def load_from_cache(transcript_hash):
    """
    Load processed transcript from cache if available.
    """
    cache_file = get_cache_file_path(transcript_hash)
    try:
        with open(cache_file, 'r', encoding='utf-8') as cache:
            return cache.read()
    except FileNotFoundError:
        return None

def save_to_cache(transcript_hash, content):
    """
    Save processed transcript to cache.
    """
    cache_file = get_cache_file_path(transcript_hash)
    with open(cache_file, 'w', encoding='utf-8') as cache:
        cache.write(content)