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

def agent(question: str) -> str:
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Você é um agente simples e objetivo."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    answer = agent("Explique em uma frase o que é RAG.")
    print(answer)
