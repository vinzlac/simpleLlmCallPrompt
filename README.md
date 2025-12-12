# Mistral LLM Interactive Client

A simple Python application that allows you to interact with the Mistral LLM API in an interactive mode.

## Features

- Interactive prompt input
- Real-time API calls to Mistral LLM
- Easy configuration via .env file
- Clean output formatting

## Requirements

- Python 3.14+
- uv (for dependency management)
- Mistral API key

## Installation

1. Clone this repository or copy the files
2. Navigate to the project directory: `cd cline_mistral_app`
3. Install dependencies: `uv sync`

## Configuration

1. Create a `.env` file in the project root
2. Add your Mistral API key: `MISTRAL_API_KEY=your_api_key_here`

## Usage

1. Activate the virtual environment: `source .venv/bin/activate`
2. Run the application: `python main.py`
3. Enter your prompts interactively
4. Type 'quit', 'exit', or 'q' to end the session

## Example

```bash
$ python main.py
Mistral LLM Interactive Client
Type 'quit' or 'exit' to end the session
----------------------------------------

Enter your prompt: What is the capital of France?

Mistral Response:
The capital of France is Paris.

Enter your prompt: quit
Goodbye!
```

## Customization

You can modify the following parameters in `main.py`:

- `model`: Change the Mistral model (e.g., "mistral-tiny", "mistral-small", etc.)
- `temperature`: Adjust creativity (0.0 to 1.0)
- `max_tokens`: Set maximum response length

## Dependencies

- requests: For making HTTP requests to the Mistral API
- python-dotenv: For loading environment variables from .env file

## License

This project is open source and available under the MIT License.
