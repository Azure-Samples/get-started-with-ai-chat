#!/usr/bin/env python3
"""
Test Azure OpenAI Service Connection
"""
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

print("🔍 Testing Azure OpenAI Connection...\n")

endpoint = "https://sfi-autopilot-ai-service.cognitiveservices.azure.com/"
model_name = "gpt-5.2-chat"
deployment = "gpt-5.2-chat"
api_version = "2024-12-01-preview"

try:
    print("1️⃣  Getting credentials...")
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    print("   ✅ Credentials obtained")
    
    print("\n2️⃣  Creating Azure OpenAI client...")
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
    )
    print("   ✅ Client created")
    
    print("\n3️⃣  Sending test message...")
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "I am going to Paris, what should I see?",
            }
        ],
        max_completion_tokens=256,
        model=deployment
    )
    print("   ✅ Response received")
    
    print("\n📝 RESPONSE:\n")
    print(response.choices[0].message.content)
    print("\n✅ Azure OpenAI connection working perfectly!")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"   {str(e)}")
    print("\n💡 Tips:")
    print("   - Make sure you're logged in: az login")
    print("   - Check if deployment name is correct: gpt-5.2-chat")
    print("   - Verify endpoint is accessible")
