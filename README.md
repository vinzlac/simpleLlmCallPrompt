# Multi-Provider LLM Interactive Client

A simple Python application that allows you to interact with multiple LLM APIs (Mistral and Gemini) in an interactive mode.

## Features

- Interactive prompt input
- Real-time API calls to Mistral and Gemini LLMs
- Multi-provider support with command-line selection
- Easy configuration via .env file
- Clean output formatting
- Error handling and validation
- Built-in testing functionality

## Requirements

- Python 3.11+
- uv (for dependency management)
- Mistral API key (for Mistral provider)
- Gemini API key (for Gemini provider)

## Installation

1. Clone this repository or copy the files
2. Navigate to the project directory: `cd simpleLlmCallPrompt`
3. Install dependencies: `uv sync`

## Configuration

1. Create a `.env` file in the project root
2. Add your API keys:
   - For Mistral: `MISTRAL_API_KEY=your_mistral_api_key_here`
   - For Gemini: `GEMINI_API_KEY=your_gemini_api_key_here`

## Usage

### Basic Usage
1. Activate the virtual environment: `source .venv/bin/activate`
2. Run the application: `python main.py`
3. Enter your prompts interactively
4. Type 'quit', 'exit', or 'q' to end the session

### Provider Selection
You can choose between Mistral and Gemini providers using the `--provider` flag:

```bash
# Use Mistral (default)
python main.py --provider mistral

# Use Gemini
python main.py --provider gemini
```

## Examples

### Mistral Example
```bash
$ python main.py --provider mistral
Mistral LLM Interactive Client
Type 'quit' or 'exit' to end the session
----------------------------------------

Enter your prompt: What is the capital of France?

Mistral Response:
The capital of France is Paris.

Enter your prompt: quit
Goodbye!
```

### Gemini Example
```bash
$ python main.py --provider gemini
Gemini LLM Interactive Client
Type 'quit' or 'exit' to end the session
----------------------------------------

Enter your prompt: Explain quantum computing in simple terms

Gemini Response:
Quantum computing is a type of computing that uses quantum bits (qubits) instead of traditional bits. Unlike classical bits that can be either 0 or 1, qubits can exist in multiple states simultaneously thanks to quantum superposition...

Enter your prompt: exit
Goodbye!
```

## Customization

You can modify the following parameters in `main.py`:

### For Mistral:
- `model`: Change the Mistral model (e.g., "mistral-tiny", "mistral-small", etc.)
- `temperature`: Adjust creativity (0.0 to 1.0)
- `max_tokens`: Set maximum response length

### For Gemini:
- `model`: Currently uses "gemini-2.5-flash" by default
- `temperature`: Adjust creativity (0.0 to 1.0)
- `max_tokens`: Set maximum response length

## Testing

The project includes multiple testing utilities:

### Basic Setup Verification

Run the setup verification script:

```bash
python test_app.py
```

This will check:
- Presence of .env file
- API key configuration
- Dependency availability
- Application structure

### Unit Tests

Run the unit test suite:

```bash
python test_unit.py
```

This will run comprehensive unit tests for all classes:
- APIConfig
- LLMAPIClient (base class)
- MistralAPIClient
- GeminiAPIClient
- LLMInteractiveClient
- Utility functions

## Dependencies

- requests: For making HTTP requests to LLM APIs
- python-dotenv: For loading environment variables from .env file

## Project Structure

```
simpleLlmCallPrompt/
├── .env                # Environment variables and API keys
├── .gitignore          # Git ignore rules
├── .python-version     # Python version specification
├── check_api_key.py    # API key validation utility
├── main.py             # Main application entry point
├── pyproject.toml      # Project configuration and dependencies
├── README.md           # Project documentation
├── test_app.py         # Testing script
└── uv.lock             # Dependency lock file
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check:
- The official Mistral API documentation
- The official Gemini API documentation
- Project GitHub repository (if available)
