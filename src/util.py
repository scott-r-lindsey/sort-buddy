import os
import re

def remove_prefix(folder_name):
    if folder_name.startswith(os.environ.get("FOLDER_PREFIX")):
        return folder_name[len(os.environ.get("FOLDER_PREFIX")):]
    return folder_name

def get_stripped_folder_list(folder_list):
    return [remove_prefix(folder) for folder in folder_list]

def limit_consecutive_linefeeds(text, max_linefeeds=2):
    """Limit consecutive linefeeds to `max_linefeeds`."""
    pattern = r'(\n|\r\n){%d,}' % (max_linefeeds + 1)
    replacement = '\n' * max_linefeeds
    return re.sub(pattern, replacement, text)

def safe_decode(byte_content):
    try:
        return byte_content.decode('utf-8')
    except UnicodeDecodeError:
        return byte_content.decode('latin-1', errors='replace')

