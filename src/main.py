import argparse
import os
import signal
from datetime import datetime
from dotenv import load_dotenv
from email_fetcher import EmailFetcher
from json_email_fetcher import JSONEmailFetcher
from ai import get_ai_response_from_message, configure_openai
from util import get_stripped_folder_list, save_results_to_json, signal_handler

load_dotenv()

def main(
        dry_run=False,
        show_prompt=False,
        limit=None,
        save_to_json=None,
        use_json=None,
        show_rate_limits=False):

    configure_openai()

    if use_json:
        fetcher = JSONEmailFetcher(use_json)
        dry_run = True
    else:
        fetcher = EmailFetcher()

    print('-' * 80)
    print(f"Fetching list of folders that start with {os.getenv('FOLDER_PREFIX')}...")
    ai_folders = fetcher.list_ai_folders()

    formatted_inboxes = get_stripped_folder_list(ai_folders)
    messages = []
    print(f"Found {len(ai_folders)} folders: {ai_folders}")

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

        folder, explanation = get_ai_response_from_message(message, formatted_inboxes, show_prompt, show_rate_limits)

        print(f" --> {folder}: {explanation}")

        response_data = {
            "datetime": datetime.now().isoformat(),
            "model": os.getenv("OPENAI_MODEL"),
            "folder": folder,
            "explanation": explanation,
        }

        message["responses"].append(response_data)

        messages.append(message)

        if not dry_run:
            if folder == "Inbox":
                print("Leaving message in inbox.")
            elif folder == "invalid":
                print("AI failure: Leaving message in inbox.")
            elif folder in formatted_inboxes:
                fetcher.move_message(message["id"], f"{os.getenv('FOLDER_PREFIX')}{folder}")
            else:
                print("Received invalid response, please review manually.")

        count += 1

    print('-' * 80)
    print(f"Processed {count} messages.")
    print('-' * 80)

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
    parser.add_argument("--print-rate-limits", action="store_true", help="Show the rate limits header from the OpenAI API response.")
    args = parser.parse_args()

    main(
        dry_run=args.dry_run,
        show_prompt=args.show_prompt,
        limit=args.limit,
        save_to_json=args.save_to_json,
        use_json=args.use_json,
        show_rate_limits=args.print_rate_limits)

