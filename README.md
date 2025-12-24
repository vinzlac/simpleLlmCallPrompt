# Multi-Provider LLM Interactive Client

A simple Python application that allows you to interact with multiple LLM APIs (Mistral and Gemini) in an interactive mode.

## Features

- Interactive prompt input
- Real-time API calls to Mistral and Gemini LLMs
- Multi-provider support with command-line selection
- **Dynamic model discovery** - Automatically fetches available models from APIs
- **Interactive model selection** - Choose from available models interactively
- **Model caching** - Caches model lists for faster startup (persistent cache)
- **Model refresh option** - Force refresh of cached model lists
- Easy configuration via .env file
- Clean output formatting with provider and model information
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

### Provider Selection and Model Selection

You can choose between Mistral and Gemini providers using the `--provider` flag. After selecting a provider, you'll be prompted to choose a model interactively:

```bash
# Use Mistral (default)
python main.py --provider mistral

# Use Gemini
python main.py --provider gemini

# Force refresh of model lists (bypass cache)
python main.py --provider mistral --refresh
python main.py --provider gemini --refresh
```

**Model Selection Process:**
1. After selecting a provider, available models are displayed
2. For Mistral: Models are fetched dynamically from the API (or loaded from cache)
3. For Gemini: Models are tested dynamically (or loaded from cache)
4. Select a model by entering its number
5. Pricing information links are displayed for reference

**Model Caching:**
- Model lists are cached in `.mistral_models_cache.json` and `.gemini_models_cache.json`
- Cache is persistent and never expires automatically
- Use `--refresh` flag to force update the cache
- First run will fetch models from APIs (may take a few seconds)
- Subsequent runs load instantly from cache

## Examples

### Mistral Example
```bash
$ python main.py --provider mistral

============================================================
Modèles disponibles pour Mistral:
============================================================
  [1] pixtral-large-2411        - Official pixtral-large-2411 Mistral AI model
  [2] mistral-small-latest      - Modèle équilibré, bonne qualité
  [3] mistral-medium-latest     - Modèle haute performance
  [4] mistral-large-latest      - Modèle le plus puissant
  ...
============================================================
💡 Pour consulter les tarifs : https://mistral.ai/fr/pricing
============================================================

Sélectionnez un modèle (1-61): 2

✅ Modèle sélectionné: mistral-small-latest
   Modèle équilibré, bonne qualité

Mistral LLM Interactive Client
Provider: Mistral
Modèle: mistral-small-latest
Type 'quit', 'exit', or 'q' to end the session
----------------------------------------

Enter your prompt: What is the capital of France?

Mistral Response:
The capital of France is Paris.

[Provider: Mistral | Modèle: mistral-small-latest]

Enter your prompt: quit
Goodbye!
```

### Gemini Example
```bash
$ python main.py --provider gemini

============================================================
Modèles disponibles pour Gemini:
============================================================
  [1] gemini-2.5-flash          - Version flash optimisée et performante
  [2] gemini-2.5-pro            - Modèle pro pour raisonnement avancé
  [3] gemini-2.0-flash-exp      - Version expérimentale de Gemini 2.0 Flash
============================================================
💡 Pour consulter les tarifs : https://ai.google.dev/pricing
============================================================

Sélectionnez un modèle (1-3): 1

✅ Modèle sélectionné: gemini-2.5-flash
   Version flash optimisée et performante

Gemini LLM Interactive Client
Provider: Gemini
Modèle: gemini-2.5-flash
Type 'quit', 'exit', or 'q' to end the session
----------------------------------------

Enter your prompt: Explain quantum computing in simple terms

Gemini Response:
Quantum computing is a type of computing that uses quantum bits (qubits) instead of traditional bits. Unlike classical bits that can be either 0 or 1, qubits can exist in multiple states simultaneously thanks to quantum superposition...

[Provider: Gemini | Modèle: gemini-2.5-flash]

Enter your prompt: exit
Goodbye!
```

## Model Management

### Dynamic Model Discovery

The application automatically discovers available models:

- **Mistral**: Fetches models from the Mistral API endpoint (`GET /v1/models`)
- **Gemini**: Tests known models to determine availability (since no public listing endpoint exists)

### Model Caching

Model lists are cached in JSON files for fast startup:
- `.mistral_models_cache.json` - Cached Mistral models
- `.gemini_models_cache.json` - Cached Gemini models

**Cache behavior:**
- Cache is persistent (never expires automatically)
- First run: Fetches models from APIs (takes a few seconds)
- Subsequent runs: Loads instantly from cache
- Use `--refresh` to force update the cache

### Customization

You can modify the following parameters in `main.py`:

- `DEFAULT_TEMPERATURE`: Adjust creativity (0.0 to 1.0, default: 0.7)
- `DEFAULT_MAX_TOKENS`: Set maximum response length (default: 1000)
- `DEFAULT_TIMEOUT`: API request timeout in seconds (default: 30)

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
├── .env                           # Environment variables and API keys
├── .gitignore                     # Git ignore rules
├── .python-version                # Python version specification
├── .mistral_models_cache.json     # Cached Mistral models list
├── .gemini_models_cache.json      # Cached Gemini models list
├── check_api_key.py               # API key validation utility
├── main.py                        # Main application entry point
├── pyproject.toml                 # Project configuration and dependencies
├── README.md                      # Project documentation
├── test_app.py                    # Testing script
├── test_unit.py                   # Unit tests
└── uv.lock                        # Dependency lock file
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check:
- The official Mistral API documentation
- The official Gemini API documentation
- Project GitHub repository (if available)
