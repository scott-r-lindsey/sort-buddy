from colorama import Fore, Style
import json
import os
import re
import sys

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

def save_results_to_json(ai_folders, messages, filename):
    results = {
        "ai_folders": ai_folders,
        "messages": messages
    }
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)

def signal_handler(signal, frame):
    print("\nExiting...")
    sys.exit(0)

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def print_line():
    print(Fore.YELLOW + "-" * get_terminal_width() + Style.RESET_ALL)
