# Sort Buddy

This is a very simple python program that leverages OpenAI or Ollama to classify and organize emails based on their content. The system connects to an IMAP email server, retrieves unread emails, and uses AI to decide the most suitable folder to store them in.

[![asciicast](https://asciinema.org/a/4acaOzAWasgMqqvpMAGeQUppc.svg)](https://asciinema.org/a/4acaOzAWasgMqqvpMAGeQUppc)

## Features

- Fetches unread emails from the specified IMAP server folders.
- Uses OpenAI (ChatGPT), Ollama or other compatible api to determine the folder where each email should be placed.
- Supports a dry-run mode to simulate processing without actual folder movement.
- Can optionally display prompts used to query AI for debugging. 

## Performance
In my testing, ChatGPT-4o has given me extremly good results at a cost of about $0.005 per email (one half of one cent).  This is much higher than the cost of using a purpose built model, but the ease and flexibility of doing it this way is amazing.
I have also tested with various local models via [Ollama](https://ollama.com/), but acheiving a result that competes with ChatGPT-4o is difficult.

## Prerequisites
- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management
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

## Running the Project
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
  - --limit: Max number of messages to process.
  - --save-to-json: Save messages and the resulting sort to a file, for benchmarking different LLMs.
  - --use-json: Instead of connecting to an IMAP server, use a previously saved file as input.
  - --print-rate-limits: Output the [rate limit](https://platform.openai.com/docs/guides/rate-limits) headers provided by OpenAI.

## Contribution
Feel free to submit issues or pull requests to improve the functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
