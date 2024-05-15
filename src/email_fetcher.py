import email
import os
from imapclient import IMAPClient
from bs4 import BeautifulSoup
from util import limit_consecutive_linefeeds, safe_decode

class EmailFetcher:
    def __init__(self):
        self.host = os.getenv("IMAP_HOST")
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imapclient = IMAPClient(self.host, ssl=True)
        self.imapclient.login(self.username, self.password)
        self.imapclient.select_folder('INBOX', readonly=True)
        self.unseen_ids = self.imapclient.search(['UNSEEN'])
        self.current_index = 0

    def list_ai_folders(self):
        folders = self.imapclient.list_folders()
        ai_folders = [folder[2] for folder in folders if folder[2].startswith(os.getenv("FOLDER_PREFIX"))]
        return ai_folders

    def fetch_next_message(self):
        if self.current_index >= len(self.unseen_ids):
            return None

        msg_id = self.unseen_ids[self.current_index]
        self.current_index += 1

        message_data = self.imapclient.fetch(msg_id, ['ENVELOPE', 'BODY[TEXT]', 'RFC822'])[msg_id]
        envelope = message_data[b'ENVELOPE']
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        text_content = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    text_content += safe_decode(part.get_payload(decode=True))
                elif part.get_content_type() == 'text/html':
                    html_content = safe_decode(part.get_payload(decode=True))
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text_content += soup.get_text()
        else:
            if email_message.get_content_type() == 'text/plain':
                text_content = safe_decode(email_message.get_payload(decode=True))
            elif email_message.get_content_type() == 'text/html':
                html_content = safe_decode(email_message.get_payload(decode=True))
                soup = BeautifulSoup(html_content, 'html.parser')
                text_content = soup.get_text()

        text_content = limit_consecutive_linefeeds(text_content.strip())

        return {
            "id": msg_id,
            "subject": safe_decode(envelope.subject) if envelope.subject else "(No Subject)",
            "from": f"{safe_decode(envelope.from_[0].mailbox)}@{safe_decode(envelope.from_[0].host)}",
            "body": text_content,
            "responses": []
        }

    def has_more_messages(self):
        return self.current_index < len(self.unseen_ids)

    def move_message(self, message_id, target_folder):
        self.imapclient.copy(message_id, target_folder)
        self.imapclient.delete_messages(message_id)
        self.imapclient.expunge()

