import json

class JSONEmailFetcher:
    def __init__(self, json_file):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.ai_folders = self.data.get("ai_folders", [])
        self.messages = self.data.get("messages", [])
        self.current_index = 0

    def list_ai_folders(self):
        return self.ai_folders

    def fetch_next_message(self):
        if self.current_index >= len(self.messages):
            return None

        message = self.messages[self.current_index]
        self.current_index += 1
        return {
            "id": message["id"],
            "from": message["from"],
            "subject": message["subject"],
            "body": message["body"],
            "responses": message.get("responses", [])
        }

    def has_more_messages(self):
        return self.current_index < len(self.messages)

    def move_message(self, message_id, target_folder):
        # No-op for JSON data, but could log or print an action
        print(f"Message {message_id} would be moved to {target_folder} in a real environment.")

