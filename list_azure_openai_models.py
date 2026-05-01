#!/usr/bin/env python3
"""
List available Azure OpenAI deployments
"""
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://sfi-autopilot-ai-service.cognitiveservices.azure.com/"
api_version = "2024-12-01-preview"

try:
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
    )
    
    print("🔍 Listing available deployments...\n")
    
    # Try to list models
    models = client.models.list()
    
    print("Available models/deployments:")
    for model in models:
        print(f"  - {model.id}")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
