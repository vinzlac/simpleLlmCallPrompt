# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
uv sync                    # Install dependencies
cp .env.example .env       # Then add API keys to .env
```

Required env vars: `MISTRAL_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY` (only when using `--provider openrouter`).

## Running

```bash
uv run python main.py                                        # Default (Mistral, interactive model selection)
uv run python main.py --provider gemini
uv run python main.py --provider openrouter --model google/gemini-2.5-flash-lite --prompt "Test prompt"
uv run python main.py --provider mistral --refresh          # Bypass model cache
```

## Testing

```bash
# Quick Mistral API key validation
source .venv/bin/activate && python test_mistral_call.py

# Setup/env check
uv run python test_app.py

# Unit tests
uv run python test_unit.py
```

## Architecture

All code is in `main.py`. The class hierarchy:

- `APIConfig` (dataclass) — holds endpoints, model names, `use_proxy` flag
- `LLMAPIClient` (base) — shared session setup, prompt validation
  - `MistralAPIClient` — direct or via OpenRouter (OpenAI-compatible format)
  - `GeminiAPIClient` — direct (native Gemini format) or via OpenRouter (OpenAI-compatible format)
- `LLMInteractiveClient` — wraps a provider client and runs the REPL loop

**Key design detail:** When `use_proxy=True`, both Mistral and Gemini clients route through `openrouter_endpoint` using the OpenAI-compatible chat format (`choices[0].message.content`). Direct Gemini calls use a different payload shape (`contents[]/parts[]`) and parse `candidates[0].content.parts[0].text`.

**Model caching:** Model lists are fetched from provider APIs and persisted as JSON files (`.mistral_models_cache.json`, `.gemini_models_cache.json`, `.mistral_models_openrouter_cache.json`, `.gemini_models_openrouter_cache.json`). Use `--refresh` to invalidate.

**Model prefix stripping:** OpenRouter returns model IDs with provider prefixes (`mistralai/`, `google/`). The `main()` function strips these before storing in `APIConfig`; `call_api()` re-adds them when building the request.

**Tunable constants** at top of `main.py`: `DEFAULT_TEMPERATURE`, `DEFAULT_MAX_TOKENS`, `DEFAULT_TIMEOUT`.
