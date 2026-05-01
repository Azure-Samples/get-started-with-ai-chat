from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Endpoint do seu serviço Azure OpenAI (Autopilot)
endpoint = "https://sfi-autopilot-ai-service.openai.azure.com/"

# Nome do DEPLOYMENT que você já confirmou que funciona
deployment = "gpt-5.2-chat"

# Autenticação via AAD (Codespaces / Azure login)
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

# Cliente Azure OpenAI (API PREVIEW, como você pediu)
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-12-01-preview"
)

# Chamada mínima (sanity check)
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "Você é um assistente simples."},
        {"role": "user", "content": "Diga apenas: ambiente funcionando."}
    ]
)

print(response.choices[0].message.content)

