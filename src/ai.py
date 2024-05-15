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

    system_prompt = "You are an email classifier.  I will give you an email and you will respond with a single word, that being the name of the best folder for that email.  If an email seems genuine, or too hard, please respond with 'inbox'.  Do not summarize the email; just respond with a single word.\n"
    system_prompt += f"The available folders are: {', '.join(stripped_folders)}\n"

    prompt = f"Email Subject: {message['subject']}\n"
    prompt += f"Email From: {message['from']}\n"

    if show_prompt:
        print(system_prompt)
        print(prompt)

    prompt += f"Email Body: {message['body']}\n"

    return (system_prompt, prompt)

def get_ai_response(prompt, system_prompt):
    try:

        response = openai.chat.completions.create(
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

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error in calling OpenAI API: {e}")
        exit()

def get_ai_response_from_message(message, folders, show_prompt=False):
    system_prompt, prompt = generate_prompt(message, folders, show_prompt)
    return get_ai_response(prompt, system_prompt)
