from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://sfi-autopilot-ai-service.openai.azure.com/"
deployment = "gpt-5.2-chat"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-12-01-preview"
)

def run_agent(messages):
    response = client.chat.completions.create(
        model=deployment,
        messages=messages
    )
    return response.choices[0].message.content
