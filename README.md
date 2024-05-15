# Sort Buddy

This is a very simple python program that leverages OpenAI or Ollama to classify and organize emails based on their content. The system connects to an IMAP email server, retrieves unread emails, and uses AI to decide the most suitable folder to store them in.

[![asciicast](https://asciinema.org/a/xxiGpgMQqshaGuFU0f0EYel02.svg)](https://asciinema.org/a/xxiGpgMQqshaGuFU0f0EYel02)

## Features

- Fetches unread emails from the specified IMAP server folders.
- Uses OpenAI (ChatGPT), Ollama or other compatible api to determine the folder where each email should be placed.
- Supports a dry-run mode to simulate processing without actual folder movement.
- Can optionally display prompts used to query AI for debugging. 

## Prerequisites
- Python 3.8+
- [https://python-poetry.org/](Poetry) for dependency management
- IMAP email credentials

## Setup
1. Clone the repository

```bash
git clone git@github.com:scott-r-lindsey/ai-email.git
cd ai-email
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Configure environment variables
  - Copy the .env.dist file to .env:

```bash
cp .env.dist .env
  - Fill in the .env file with your IMAP email credentials, AI key (OpenAI or Ollama), and folder prefix.
```

# Running the Project
  - To execute the project, you can use the provided run.sh shell script:
```bash
./run.sh --dry-run
```
  - Alternatively, run the main Python script directly with optional arguments:

```bash
poetry run python main.py --dry-run --show-prompt
```
  - --dry-run: Print prompts and messages without moving any emails.
  - --show-prompt: Display the AI prompt, minus the email body.

# Contribution
Feel free to submit issues or pull requests to improve the functionality.

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
