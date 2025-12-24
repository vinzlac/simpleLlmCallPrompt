#!/usr/bin/env python3

import os
import logging
import argparse
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_TIMEOUT = 30
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

@dataclass
class APIConfig:
    """Configuration for API endpoints and models"""
    mistral_endpoint: str = "https://api.mistral.ai/v1/chat/completions"
    mistral_model: str = "mistral-tiny"
    gemini_model: str = "gemini-2.5-flash"

    @property
    def gemini_endpoint(self) -> str:
        """Generate Gemini endpoint URL using the configured model"""
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent"

class LLMAPIClient:
    """Base class for LLM API clients"""

    def __init__(self, api_key: str, config: APIConfig):
        self.api_key = api_key
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def call_api(self, prompt: str) -> Optional[str]:
        """Call the LLM API with the given prompt"""
        raise NotImplementedError("Subclasses must implement this method")

    def _validate_prompt(self, prompt: str) -> bool:
        """Validate the user prompt"""
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt provided")
            return False
        return True

class MistralAPIClient(LLMAPIClient):
    """Client for Mistral API"""

    def __init__(self, api_key: str, config: APIConfig = APIConfig()):
        super().__init__(api_key, config)
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })

    def call_api(self, prompt: str) -> Optional[str]:
        """Call Mistral API with the given prompt"""
        if not self._validate_prompt(prompt):
            return None

        try:
            data = {
                "model": self.config.mistral_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt.strip()
                    }
                ],
                "temperature": DEFAULT_TEMPERATURE,
                "max_tokens": DEFAULT_MAX_TOKENS
            }

            logger.info(f"Calling Mistral API with prompt: {prompt[:50]}...")
            response = self.session.post(
                self.config.mistral_endpoint,
                json=data,
                timeout=DEFAULT_TIMEOUT
            )

            response.raise_for_status()
            result = response.json()

            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                logger.info("Successfully received response from Mistral API")
                return content
            else:
                logger.error(f"Unexpected API response format: {result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Mistral API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Mistral API response: {e}")
            return None

class GeminiAPIClient(LLMAPIClient):
    """Client for Gemini API"""

    def __init__(self, api_key: str, config: APIConfig = APIConfig()):
        super().__init__(api_key, config)
        self.session.headers.update({
            "X-goog-api-key": api_key
        })

    def call_api(self, prompt: str) -> Optional[str]:
        """Call Gemini API with the given prompt"""
        if not self._validate_prompt(prompt):
            return None

        try:
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt.strip()
                            }
                        ]
                    }
                ]
            }

            logger.info(f"Calling Gemini API with prompt: {prompt[:50]}...")
            response = self.session.post(
                self.config.gemini_endpoint,
                json=data,
                timeout=DEFAULT_TIMEOUT
            )

            response.raise_for_status()
            result = response.json()

            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text'].strip()
                logger.info("Successfully received response from Gemini API")
                return content
            else:
                logger.error(f"Unexpected API response format: {result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Gemini API response: {e}")
            return None

class LLMInteractiveClient:
    """Interactive client for LLM APIs"""

    def __init__(self, provider: str, api_key: str, config: APIConfig = APIConfig()):
        self.provider = provider
        self.api_key = api_key
        self.config = config
        self.client = self._initialize_client()

    def _initialize_client(self) -> LLMAPIClient:
        """Initialize the appropriate API client based on provider"""
        if self.provider == "mistral":
            return MistralAPIClient(self.api_key, self.config)
        elif self.provider == "gemini":
            return GeminiAPIClient(self.api_key, self.config)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def run_interactive_session(self):
        """Run an interactive session with the LLM"""
        provider_name = self.provider.capitalize()
        model_name = self.config.mistral_model if self.provider == "mistral" else self.config.gemini_model
        
        logger.info(f"{provider_name} LLM Interactive Client")
        logger.info(f"Provider: {provider_name}")
        logger.info(f"Modèle: {model_name}")
        logger.info("Type 'quit', 'exit', or 'q' to end the session")
        logger.info("----------------------------------------")

        while True:
            try:
                user_prompt = input("\nEnter your prompt: ").strip()

                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    logger.info("Goodbye!")
                    break

                if not user_prompt:
                    logger.warning("Please enter a valid prompt.")
                    continue

                response = self.client.call_api(user_prompt)
                if response:
                    logger.info(f"\n{provider_name} Response:")
                    logger.info(response)
                    logger.info(f"\n[Provider: {provider_name} | Modèle: {model_name}]")
                else:
                    logger.error(f"No response received from {provider_name} API.")

            except KeyboardInterrupt:
                logger.info("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")

def fetch_mistral_models(api_key: str, force_refresh: bool = False) -> Dict[str, tuple]:
    """Fetch available models from Mistral API dynamically"""
    # Charger depuis le cache si disponible et si pas de refresh forcé
    if not force_refresh:
        cached_models = load_mistral_models_from_cache()
        if cached_models:
            return cached_models
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info("Récupération de la liste des modèles depuis l'API Mistral...")
        response = requests.get(
            'https://api.mistral.ai/v1/models',
            headers=headers,
            timeout=DEFAULT_TIMEOUT
        )
        
        response.raise_for_status()
        data = response.json()
        
        models_list = []
        if 'data' in data and isinstance(data['data'], list):
            for model in data['data']:
                model_id = model.get('id', '')
                # Filtrer seulement les modèles de chat (pas les embeddings, pas les modèles CLI)
                if 'embed' not in model_id.lower() and 'cli' not in model_id.lower():
                    description = model.get('description', f'Modèle {model_id}')
                    # Nettoyer la description (limiter la longueur)
                    if len(description) > 80:
                        description = description[:77] + "..."
                    models_list.append((model_id, description))
            
            # Trier les modèles : priorités aux modèles "latest", puis par nom
            def sort_key(item):
                model_id, _ = item
                priority = 0
                if '-latest' in model_id:
                    priority = 1
                elif any(x in model_id for x in ['mistral-small', 'mistral-medium', 'mistral-large', 'pixtral']):
                    priority = 2
                return (priority, model_id)
            
            models_list.sort(key=sort_key, reverse=True)
            
            # Convertir en dictionnaire avec index
            models_dict = {str(idx): model for idx, model in enumerate(models_list, start=1)}
            
            logger.info(f"✅ {len(models_dict)} modèles récupérés depuis l'API Mistral")
            # Sauvegarder dans le cache
            save_mistral_models_to_cache(models_dict)
            return models_dict
        else:
            logger.warning("Format de réponse inattendu de l'API Mistral")
            return get_fallback_mistral_models()
            
    except requests.exceptions.RequestException as e:
        logger.warning(f"Impossible de récupérer les modèles depuis l'API Mistral: {e}")
        logger.info("Utilisation de la liste de modèles par défaut...")
        return get_fallback_mistral_models()
    except Exception as e:
        logger.warning(f"Erreur lors de la récupération des modèles: {e}")
        logger.info("Utilisation de la liste de modèles par défaut...")
        return get_fallback_mistral_models()

def fetch_gemini_models(api_key: str, force_refresh: bool = False) -> Dict[str, tuple]:
    """Fetch available Gemini models by testing known models dynamically"""
    # Charger depuis le cache si disponible et si pas de refresh forcé
    if not force_refresh:
        cached_models = load_gemini_models_from_cache()
        if cached_models:
            return cached_models
    
    try:
        headers = {
            'X-goog-api-key': api_key,
            'Content-Type': 'application/json'
        }
        
        logger.info("Test des modèles Gemini disponibles...")
        
        # Liste des modèles Gemini connus à tester (les plus courants en premier)
        known_models = [
            ("gemini-2.5-flash", "Version flash optimisée et performante"),
            ("gemini-2.5-flash-001", "Version flash avec numéro de version explicite"),
            ("gemini-2.5-pro", "Modèle pro pour raisonnement avancé"),
            ("gemini-2.5-pro-001", "Version pro avec numéro de version explicite"),
            ("gemini-2.0-flash-exp", "Version expérimentale de Gemini 2.0 Flash"),
            ("gemini-1.5-pro", "Modèle 1.5 Pro"),
            ("gemini-1.5-pro-001", "Modèle 1.5 Pro avec numéro de version"),
            ("gemini-pro", "Modèle Gemini Pro classique"),
            ("gemini-1.5-flash", "Modèle 1.5 Flash"),
            ("gemini-1.5-flash-001", "Modèle 1.5 Flash avec numéro de version"),
        ]
        
        available_models = []
        test_data = {"contents": [{"parts": [{"text": "test"}]}]}
        
        for model_id, description in known_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent"
            try:
                response = requests.post(url, headers=headers, json=test_data, timeout=5)
                # 200 = modèle disponible, 400 = modèle existe mais erreur de requête (donc disponible)
                # 401 = problème d'auth mais modèle existe probablement, 404 = modèle n'existe pas
                if response.status_code in [200, 400]:
                    available_models.append((model_id, description))
                    logger.debug(f"✅ {model_id} - disponible")
                elif response.status_code == 401:
                    # 401 peut signifier que le modèle existe mais nécessite plus de permissions
                    # On l'inclut quand même car il existe probablement
                    available_models.append((model_id, description))
                    logger.debug(f"⚠️  {model_id} - probablement disponible (401)")
            except requests.exceptions.Timeout:
                # Timeout = modèle probablement disponible mais lent, on l'inclut
                available_models.append((model_id, description))
                logger.debug(f"⏱️  {model_id} - timeout (inclu quand même)")
            except Exception:
                # Autre erreur, on ignore ce modèle
                pass
        
        if available_models:
            # Convertir en dictionnaire avec index
            models_dict = {str(idx): model for idx, model in enumerate(available_models, start=1)}
            logger.info(f"✅ {len(models_dict)} modèles Gemini testés et disponibles")
            # Sauvegarder dans le cache
            save_gemini_models_to_cache(models_dict)
            return models_dict
        else:
            logger.warning("Aucun modèle Gemini disponible trouvé via test dynamique")
            return get_fallback_gemini_models()
            
    except Exception as e:
        logger.warning(f"Erreur lors du test des modèles Gemini: {e}")
        logger.info("Utilisation de la liste de modèles par défaut...")
        return get_fallback_gemini_models()

def get_fallback_mistral_models() -> Dict[str, tuple]:
    """Fallback list of Mistral models if API call fails"""
    return {
        "1": ("mistral-tiny", "Modèle rapide et économique"),
        "2": ("mistral-small-latest", "Modèle équilibré, bonne qualité"),
        "3": ("mistral-medium-latest", "Modèle haute performance"),
        "4": ("mistral-large-latest", "Modèle le plus puissant"),
    }

def get_gemini_models_cache_path() -> Path:
    """Get the path to the Gemini models cache file"""
    return Path(__file__).parent / ".gemini_models_cache.json"

def get_mistral_models_cache_path() -> Path:
    """Get the path to the Mistral models cache file"""
    return Path(__file__).parent / ".mistral_models_cache.json"

def save_gemini_models_to_cache(models: Dict[str, tuple]) -> None:
    """Save Gemini models to cache file"""
    cache_path = get_gemini_models_cache_path()
    try:
        # Convertir les tuples en listes pour la sérialisation JSON
        models_serializable = {
            key: [model_id, description]
            for key, (model_id, description) in models.items()
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(models_serializable, f, indent=2, ensure_ascii=False)
        logger.info(f"Modèles Gemini sauvegardés dans {cache_path}")
    except Exception as e:
        logger.warning(f"Erreur lors de la sauvegarde du cache: {e}")

def load_gemini_models_from_cache() -> Optional[Dict[str, tuple]]:
    """Load Gemini models from cache file"""
    cache_path = get_gemini_models_cache_path()
    if not cache_path.exists():
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            models_serializable = json.load(f)
        # Convertir les listes en tuples
        models = {
            key: tuple(value)
            for key, value in models_serializable.items()
        }
        logger.info(f"Modèles Gemini chargés depuis le cache ({len(models)} modèles)")
        return models
    except Exception as e:
        logger.warning(f"Erreur lors du chargement du cache: {e}")
        return None

def save_mistral_models_to_cache(models: Dict[str, tuple]) -> None:
    """Save Mistral models to cache file"""
    cache_path = get_mistral_models_cache_path()
    try:
        # Convertir les tuples en listes pour la sérialisation JSON
        models_serializable = {
            key: [model_id, description]
            for key, (model_id, description) in models.items()
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(models_serializable, f, indent=2, ensure_ascii=False)
        logger.info(f"Modèles Mistral sauvegardés dans {cache_path}")
    except Exception as e:
        logger.warning(f"Erreur lors de la sauvegarde du cache: {e}")

def load_mistral_models_from_cache() -> Optional[Dict[str, tuple]]:
    """Load Mistral models from cache file"""
    cache_path = get_mistral_models_cache_path()
    if not cache_path.exists():
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            models_serializable = json.load(f)
        # Convertir les listes en tuples
        models = {
            key: tuple(value)
            for key, value in models_serializable.items()
        }
        logger.info(f"Modèles Mistral chargés depuis le cache ({len(models)} modèles)")
        return models
    except Exception as e:
        logger.warning(f"Erreur lors du chargement du cache: {e}")
        return None

def get_fallback_gemini_models() -> Dict[str, tuple]:
    """Fallback list of Gemini models if dynamic testing fails"""
    return {
        "1": ("gemini-2.5-flash", "Version flash optimisée et performante"),
        "2": ("gemini-2.5-pro", "Modèle pro pour raisonnement avancé"),
        "3": ("gemini-2.0-flash-exp", "Version expérimentale de Gemini 2.0 Flash"),
    }

def get_available_models(provider: str, api_key: Optional[str] = None, force_refresh: bool = False) -> Dict[str, tuple]:
    """Get available models for a provider with descriptions"""
    if provider == "mistral":
        if api_key:
            # Essayer de récupérer dynamiquement depuis l'API
            models = fetch_mistral_models(api_key, force_refresh=force_refresh)
            if models:
                return models
        # Fallback vers liste statique si pas de clé API ou erreur
        return get_fallback_mistral_models()
    elif provider == "gemini":
        if api_key:
            # Essayer de récupérer dynamiquement en testant les modèles connus
            models = fetch_gemini_models(api_key, force_refresh=force_refresh)
            if models:
                return models
        # Fallback vers liste statique si pas de clé API ou erreur
        return get_fallback_gemini_models()
    else:
        return {}

def select_model_interactively(provider: str, api_key: Optional[str] = None, force_refresh: bool = False) -> Optional[str]:
    """Interactively select a model for the given provider"""
    models = get_available_models(provider, api_key, force_refresh=force_refresh)
    
    if not models:
        logger.error(f"No models available for provider: {provider}")
        return None
    
    provider_name = provider.capitalize()
    
    # URLs de pricing pour chaque provider
    pricing_urls = {
        "mistral": "https://mistral.ai/fr/pricing",
        "gemini": "https://ai.google.dev/pricing"
    }
    
    print(f"\n{'='*60}")
    print(f"Modèles disponibles pour {provider_name}:")
    print(f"{'='*60}")
    
    # Trier par clé numérique pour un affichage ordonné
    for key in sorted(models.keys(), key=lambda x: int(x)):
        model, description = models[key]
        print(f"  [{key}] {model:25} - {description}")
    
    print(f"{'='*60}")
    
    # Afficher le lien vers la page de pricing
    if provider in pricing_urls:
        print(f"\n💡 Pour consulter les tarifs : {pricing_urls[provider]}")
        print(f"{'='*60}")
    
    while True:
        try:
            max_choice = max(int(k) for k in models.keys())
            choice = input(f"\nSélectionnez un modèle (1-{max_choice}): ").strip()
            
            if choice in models:
                selected_model, description = models[choice]
                print(f"\n✅ Modèle sélectionné: {selected_model}")
                print(f"   {description}")
                return selected_model
            else:
                print(f"❌ Choix invalide. Veuillez entrer un nombre entre 1 et {max_choice}.")
        except KeyboardInterrupt:
            print("\n\n❌ Sélection annulée.")
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la sélection: {e}")
            return None

def get_api_key(provider: str) -> Optional[str]:
    """Get API key from environment variables"""
    env_var = f"{provider.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if not api_key or not api_key.strip():
        logger.error(f"Error: {env_var} not found in .env file")
        return None

    return api_key

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="LLM Interactive Client")
    parser.add_argument(
        "--provider",
        choices=["mistral", "gemini"],
        default="mistral",
        help="Choose the LLM provider to use (default: mistral)"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh of model list (for Gemini, reload from API instead of cache)"
    )
    return parser.parse_args()

def main():
    """Main entry point for the LLM interactive client"""
    args = parse_arguments()

    # Load environment variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=dotenv_path, override=True)

    # Get API key
    api_key = get_api_key(args.provider)
    if not api_key:
        return

    # Select model interactively (pass API key to fetch models dynamically)
    selected_model = select_model_interactively(args.provider, api_key, force_refresh=args.refresh)
    if not selected_model:
        logger.error("Aucun modèle sélectionné. Arrêt de l'application.")
        return

    # Create config with selected model
    config = APIConfig()
    if args.provider == "mistral":
        config.mistral_model = selected_model
    elif args.provider == "gemini":
        config.gemini_model = selected_model

    # Initialize and run client with selected model
    client = LLMInteractiveClient(args.provider, api_key, config)
    client.run_interactive_session()

if __name__ == "__main__":
    main()
