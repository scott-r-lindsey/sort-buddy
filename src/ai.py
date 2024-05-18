import openai
import os

def configure_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.base_url = os.getenv("OPENAI_API_URL")

def remove_prefix(folder_name):
    if folder_name.startswith(os.environ.get("FOLDER_PREFIX")):
        return folder_name[len(os.environ.get("FOLDER_PREFIX")):]
    return folder_name

def get_stripped_folder_list(folder_list):
    return [remove_prefix(folder) for folder in folder_list]

def generate_prompt(message, folders, show_prompt=False):

    stripped_folders = get_stripped_folder_list(folders)

    system_prompt = "You are an email classifier.  I will give you an email, "
    system_prompt += "and you will respond with a the name of the best folder "
    system_prompt += "for that email, followed by a colon and a space.  If an "
    system_prompt += "email seems genuine, or too hard, please respond with "
    system_prompt += "'Inbox'.  After the colon and space, please provide a "
    system_prompt += "brief explanation of why you chose that folder. "

    system_prompt += f"The available folders are: {', '.join(stripped_folders)} and Inbox\n"

    prompt = f"Email Subject: {message['subject']}\n"
    prompt += f"Email From: {message['from']}\n"

    if show_prompt:
        print(system_prompt)
        print(prompt)

    prompt += f"Email Body: {message['body']}\n"

    return (system_prompt, prompt)

def get_ai_response(prompt, system_prompt, folders, show_rate_limits):
    try:

        response = openai.chat.completions.with_raw_response.create(
            model=os.environ.get("OPENAI_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # print the rate limit information from the response, but label it
        if show_rate_limits:
            print("Rate Limit Requests: ", response.headers.get('x-ratelimit-limit-requests'))
            print("Rate Limit Tokens: ", response.headers.get('x-ratelimit-limit-tokens'))
            print("Rate Limit Tokens Usage Based: ", response.headers.get('x-ratelimit-limit-tokens_usage_based'))

            print("Rate Limit Remaining Requests: ", response.headers.get('x-ratelimit-remaining-requests'))
            print("Rate Limit Remaining Tokens: ", response.headers.get('x-ratelimit-remaining-tokens'))
            print("Rate Limit Remaining Tokens Usage Based: ", response.headers.get('x-ratelimit-remaining-tokens_usage_based'))

            print("Rate Limit Reset Requests: ", response.headers.get('x-ratelimit-reset-requests'))
            print("Rate Limit Reset Tokens: ", response.headers.get('x-ratelimit-reset-tokens'))
            print("Rate Limit Reset Tokens Usage Based: ", response.headers.get('x-ratelimit-reset-tokens_usage_based'))

        response = response.parse()

        message = response.choices[0].message.content

    except Exception as e:
        print(f"Error in calling OpenAI API: {e}")
        exit()

    try:
        # split the parts on the first colon and space
        (folder, explanation) = message.split(': ', 1)
        folder = folder.strip()

    except ValueError:
        # if the split fails, the response is invalid
        return ("invalid", "could not split response")

    # if the folder is "Inbox"
    if folder == "Inbox":
        return ("Inbox", explanation)
    # check if the folder is valid
    elif folder not in folders:
        return (f"invalid: \"{folder}\"", explanation)

    return (str(folder), str(explanation))


def get_ai_response_from_message(message, folders, show_prompt=False, show_rate_limits=False):
    system_prompt, prompt = generate_prompt(message, folders, show_prompt)
    return get_ai_response(prompt, system_prompt, folders, show_rate_limits)
