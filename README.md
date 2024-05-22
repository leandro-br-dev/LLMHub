# LLM Hub

LLM Hub is an API that organizes and facilitates requests to various Language Model (LLM) systems such as Google Gemini, ChatGPT, Ollama, Anthropic, and is also compatible with the Open-WebUI interface. This solution allows you to run a local server and use Open-WebUI as a user interface.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Project Architecture](#project-architecture)
- [Contributing](#contributing)

## Installation

Follow the steps below to install and configure LLM Hub.

### Prerequisites

- Python 3.9 or higher
- Docker
- `pip` (Python package manager)

### Step 1: Clone the Repository

First, clone the GitHub repository to your local environment:

```sh
git clone https://github.com/leandro-br-dev/LLMHub.git
cd LLMHub
```

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate the project's dependencies:

```sh
python -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate
```

### Step 3: Install Dependencies

Install the necessary libraries via the requirements.txt file:

```sh
pip install -r requirements.txt
```

## Configuration

### Step 4: Configure Environment Variables

Rename the .env-sample file to .env and configure the internal variables as shown below:

```ini
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET_KEY=XXXXXXXXXXXXXXXXX
FLASK_RUN_PORT=5001

OLLAMA_API=http://localhost:11434
OPENAI_API_KEY=XXXXXXXXXXXXXXXXX
ANTHROPIC_API_KEY=XXXXXXXXXXXXXXXXX
GOOGLE_API_KEY=XXXXXXXXXXXXXXXXX
```

### Step 5: Configure Models

Configure the models you want to run in the config_models.json file, as shown in the example below:

```json
{
  "llm_services": [
    {
      "model": "llava",
      "service": "Ollama"
    },
    {
      "model": "llava:13b",
      "service": "Ollama"
    },
    {
      "model": "mistral",
      "service": "Ollama"
    },
    {
      "model": "gpt-3.5-turbo-0301",
      "service": "OpenAI"
    },
    {
      "model": "gpt-4-turbo-2024-04-09",
      "service": "OpenAI"
    },
    {
      "model": "gpt-4o",
      "service": "OpenAI"
    },
    {
      "model": "claude-3-haiku-20240307",
      "service": "Anthropic"
    },
    {
      "model": "claude-3-opus-20240229",
      "service": "Anthropic"
    },
    {
      "model": "gemini-pro",
      "service": "Google"
    },
    {
      "model": "gemini-1.5-pro-latest",
      "service": "Google"
    },
    {
      "model": "gemini-pro-vision",
      "service": "Google"
    }
  ]
}
```

## Running the Project

### Step 6: Run the Server with Docker

To run Open-WebUI as an interface, execute the following Docker command, changing the OLLAMA_BASE_URL field as necessary:

```sh
sudo docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:5001 --name open-webui-hub --restart always ghcr.io/open-webui/open-webui:main
```


### Step 7: Start the Flask Server

Start the Flask server:

```sh
flask run
```

## Project Architecture

The project architecture is illustrated below (coming soon).


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or suggestions.
