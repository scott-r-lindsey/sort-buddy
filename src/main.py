import argparse
import os
import signal
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from email_fetcher import EmailFetcher
from json_email_fetcher import JSONEmailFetcher
from ai import get_ai_response_from_message, configure_openai
from util import get_stripped_folder_list

load_dotenv()

def signal_handler(signal, frame):
    print("\nExiting...")
    sys.exit(0)

def save_results_to_json(ai_folders, messages, filename):
    results = {
        "ai_folders": ai_folders,
        "messages": messages
    }
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)

def main(dry_run=False, show_prompt=False, limit=None, save_to_json=None, use_json=None):
    configure_openai()

    if use_json:
        fetcher = JSONEmailFetcher(use_json)
    else:
        fetcher = EmailFetcher()

    print(f"Fetching list of folders that start with {os.getenv('FOLDER_PREFIX')}...")
    ai_folders = fetcher.list_ai_folders()

    formatted_inboxes = get_stripped_folder_list(ai_folders)
    messages = []

    count = 0
    while fetcher.has_more_messages():
        if limit is not None and count >= limit:
            break

        message = fetcher.fetch_next_message()
        if not message:
            continue

        print('-' * 80)
        print(f"From: {message['from']}")
        print(f"Subject: {message['subject']}")

        response = get_ai_response_from_message(message, formatted_inboxes, show_prompt)

        print('-' * 80)
        print(f" --> {response}")

        response_data = {
            "datetime": datetime.now().isoformat(),
            "model": os.getenv("OPENAI_MODEL"),
            "response": response
        }

        message["responses"].append(response_data)

        messages.append(message)

        if not dry_run:
            if response == "inbox":
                print("Leaving message in inbox.")
            elif response in formatted_inboxes:
                fetcher.move_message(message["id"], response)
            else:
                print("Received invalid response, please review manually.")

        count += 1

    if save_to_json:
        save_results_to_json(ai_folders, messages, save_to_json)
        print(f"Results saved to {save_to_json}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Parse emails and process them.")
    parser.add_argument("--dry-run", action="store_true", help="Only print prompts and messages without processing them.")
    parser.add_argument("--show-prompt", action="store_true", help="Show the prompt, minus the body of the email.")
    parser.add_argument("--limit", type=int, help="Limit the number of messages to process.")
    parser.add_argument("--save-to-json", type=str, help="Save the results to a JSON file.")
    parser.add_argument("--use-json", type=str, help="Use a JSON file for input instead of connecting to IMAP.")
    args = parser.parse_args()

    main(dry_run=args.dry_run, show_prompt=args.show_prompt, limit=args.limit, save_to_json=args.save_to_json, use_json=args.use_json)

