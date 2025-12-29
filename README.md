# Multi-Provider LLM Interactive Client

A simple Python application that allows you to interact with multiple LLM APIs (Mistral, Gemini) directly or via OpenRouter proxy in an interactive mode.

## Features

- Interactive prompt input
- Real-time API calls to Mistral and Gemini LLMs
- Multi-provider support with command-line selection
- **OpenRouter proxy support** - Access Mistral and Gemini models via OpenRouter
- **Dynamic model discovery** - Automatically fetches available models from APIs
- **Interactive model selection** - Choose from available models interactively (filtered by provider when using proxy)
- **Model caching** - Caches model lists for faster startup (persistent cache, separate caches for direct and proxy access)
- **Model refresh option** - Force refresh of cached model lists
- Easy configuration via .env file
- Clean output formatting with provider and model information
- Error handling and validation
- Built-in testing functionality

## Requirements

- Python 3.11+
- uv (for dependency management)
- Mistral API key (for direct Mistral access)
- Gemini API key (for direct Gemini access)
- OpenRouter API key (when using `--proxy openrouter`)

## Installation

1. Clone this repository or copy the files
2. Navigate to the project directory: `cd simpleLlmCallPrompt`
3. Install dependencies: `uv sync`

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API keys:
   - For Mistral (direct access): Get your key from [Mistral Console](https://console.mistral.ai/)
   - For Gemini (direct access): Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - For OpenRouter (when using `--proxy openrouter`): Get your key from [OpenRouter](https://openrouter.ai/keys)

   The `.env.example` file shows the required format for all API keys.
   
   **Note:** You only need the OpenRouter API key if you plan to use the `--proxy openrouter` option.

## Usage

### Basic Usage
1. Run the application: `uv run python main.py` (or `python main.py` if using virtual environment)
2. Select a provider (mistral or gemini)
3. Optionally use OpenRouter proxy: `uv run python main.py --provider mistral --proxy openrouter`
4. Select a model from the displayed list
5. Enter your prompts interactively
6. Type 'quit', 'exit', or 'q' to end the session

### Provider Selection and Proxy Option

You can choose between Mistral and Gemini providers using the `--provider` flag. Optionally, you can use OpenRouter as a proxy to access these providers with `--proxy openrouter`:

```bash
# Use Mistral directly (default)
uv run python main.py --provider mistral

# Use Gemini directly
uv run python main.py --provider gemini

# Use Mistral via OpenRouter proxy
uv run python main.py --provider mistral --proxy openrouter

# Use Gemini via OpenRouter proxy
uv run python main.py --provider gemini --proxy openrouter

# Force refresh of model lists (bypass cache)
uv run python main.py --provider mistral --refresh
uv run python main.py --provider gemini --refresh
uv run python main.py --provider mistral --proxy openrouter --refresh
uv run python main.py --provider gemini --proxy openrouter --refresh
```

**Model Selection Process:**
1. After selecting a provider (and optionally a proxy), available models are displayed
2. **Direct access:**
   - For Mistral: Models are fetched dynamically from the Mistral API (or loaded from cache)
   - For Gemini: Models are tested dynamically (or loaded from cache)
3. **Via OpenRouter proxy:**
   - Models are fetched from OpenRouter API and filtered by provider (only `mistralai/*` for Mistral, only `google/*` for Gemini)
   - Model lists are cached separately from direct access
4. Select a model by entering its number
5. Pricing information links are displayed for reference

**Model Caching:**
- **Direct access caches:**
  - `.mistral_models_cache.json` - Cached Mistral models (direct API)
  - `.gemini_models_cache.json` - Cached Gemini models (direct API)
- **OpenRouter proxy caches:**
  - `.mistral_models_openrouter_cache.json` - Cached Mistral models via OpenRouter
  - `.gemini_models_openrouter_cache.json` - Cached Gemini models via OpenRouter
- Cache is persistent and never expires automatically
- Use `--refresh` flag to force update the cache
- First run will fetch models from APIs (may take a few seconds)
- Subsequent runs load instantly from cache

## Examples

### Mistral Example (Direct Access)
```bash
$ uv run python main.py --provider mistral

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

### Gemini Example (Direct Access)
```bash
$ uv run python main.py --provider gemini

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

### Mistral via OpenRouter Example
```bash
$ uv run python main.py --provider mistral --proxy openrouter

============================================================
Modèles disponibles pour Mistral (via OpenRouter):
============================================================
  [1] mistralai/mistral-small-latest   - Mistral Small via OpenRouter
  [2] mistralai/mistral-medium-latest  - Mistral Medium via OpenRouter
  [3] mistralai/mistral-large-latest   - Mistral Large via OpenRouter
  ...
============================================================
💡 Pour consulter les tarifs : https://openrouter.ai/models
============================================================

Sélectionnez un modèle (1-15): 1

✅ Modèle sélectionné: mistralai/mistral-small-latest
   Mistral Small via OpenRouter

Mistral (via OpenRouter) LLM Interactive Client
Provider: Mistral (via OpenRouter)
Modèle: mistral-small-latest
Type 'quit', 'exit', or 'q' to end the session
----------------------------------------

Enter your prompt: Hello!
...
```

### Gemini via OpenRouter Example
```bash
$ uv run python main.py --provider gemini --proxy openrouter

============================================================
Modèles disponibles pour Gemini (via OpenRouter):
============================================================
  [1] google/gemini-2.5-flash   - Gemini 2.5 Flash via OpenRouter
  [2] google/gemini-2.5-pro     - Gemini 2.5 Pro via OpenRouter
  ...
============================================================
💡 Pour consulter les tarifs : https://openrouter.ai/models
============================================================
...
```

## Model Management

### Dynamic Model Discovery

The application automatically discovers available models:

**Direct Access:**
- **Mistral**: Fetches models from the Mistral API endpoint (`GET /v1/models`)
- **Gemini**: Tests known models to determine availability (since no public listing endpoint exists)

**Via OpenRouter Proxy:**
- Fetches all models from OpenRouter API endpoint (`GET /v1/models`)
- Filters models by provider prefix:
  - `mistralai/*` for Mistral models
  - `google/*` for Gemini models
- Model lists are cached separately from direct access

### Model Caching

Model lists are cached in JSON files for fast startup:

**Direct Access Caches:**
- `.mistral_models_cache.json` - Cached Mistral models (direct API)
- `.gemini_models_cache.json` - Cached Gemini models (direct API)

**OpenRouter Proxy Caches:**
- `.mistral_models_openrouter_cache.json` - Cached Mistral models via OpenRouter
- `.gemini_models_openrouter_cache.json` - Cached Gemini models via OpenRouter

**Cache behavior:**
- Cache is persistent (never expires automatically)
- First run: Fetches models from APIs (takes a few seconds)
- Subsequent runs: Loads instantly from cache
- Use `--refresh` to force update the cache
- Separate caches for direct access vs. proxy access ensure accurate model lists

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
- MistralAPIClient (direct and proxy support)
- GeminiAPIClient (direct and proxy support)
- LLMInteractiveClient
- Utility functions

## Dependencies

- requests: For making HTTP requests to LLM APIs
- python-dotenv: For loading environment variables from .env file

## Project Structure

```
simpleLlmCallPrompt/
├── .env                           # Environment variables and API keys (not in git)
├── .env.example                   # Example environment file with API key placeholders
├── .gitignore                     # Git ignore rules
├── .python-version                # Python version specification
├── .mistral_models_cache.json                # Cached Mistral models (direct API)
├── .gemini_models_cache.json                 # Cached Gemini models (direct API)
├── .mistral_models_openrouter_cache.json     # Cached Mistral models (via OpenRouter)
├── .gemini_models_openrouter_cache.json      # Cached Gemini models (via OpenRouter)
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
