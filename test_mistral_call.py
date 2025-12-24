#!/usr/bin/env python3

"""Script simple pour tester un appel API Mistral"""

import os
from dotenv import load_dotenv
from main import MistralAPIClient, APIConfig, get_api_key

def main():
    # Charger les variables d'environnement
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=dotenv_path, override=True)
    
    # Obtenir la clé API
    api_key = get_api_key("mistral")
    if not api_key:
        print("❌ Erreur: MISTRAL_API_KEY non trouvée dans le fichier .env")
        return
    
    # Créer le client Mistral
    config = APIConfig()
    client = MistralAPIClient(api_key, config)
    
    print("🔄 Appel API en cours...")
    print("-" * 50)
    print(f"Provider: Mistral")
    print(f"Modèle: {config.mistral_model}")
    print("-" * 50)
    
    # Faire un appel simple
    prompt = "Dis-moi en une phrase: qu'est-ce que l'intelligence artificielle?"
    print(f"Prompt: {prompt}\n")
    
    response = client.call_api(prompt)
    
    if response:
        print("✅ Réponse reçue:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        print(f"Provider utilisé: Mistral")
        print(f"Modèle utilisé: {config.mistral_model}")
    else:
        print("❌ Erreur: Aucune réponse reçue de Mistral")

if __name__ == "__main__":
    main()

