# Mock clients for local development without Azure
import asyncio
from typing import Optional, List, Dict, Any, AsyncGenerator

class MockDelta:
    def __init__(self, content: str):
        self.content = content

class MockChoice:
    def __init__(self, content: str = None):
        self.delta = MockDelta(content)

class MockMessage:
    def __init__(self, content: str = ""):
        self.choices = [MockChoice(content)]

class MockAsyncIterator:
    """Mock async iterator for streaming responses"""
    def __init__(self, text: str, chunk_size: int = 10):
        self.text = text
        self.chunk_size = chunk_size
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.text):
            raise StopAsyncIteration
        
        chunk = self.text[self.index:self.index + self.chunk_size]
        self.index += self.chunk_size
        await asyncio.sleep(0.05)  # Simulate delay
        return MockMessage(chunk)

class MockChatCompletionsClient:
    """Mock ChatCompletionsClient for local development"""
    
    def __init__(self, endpoint: str, credential, credential_scopes: List[str]):
        self.endpoint = endpoint
        self.credential = credential
        self.credential_scopes = credential_scopes
        print(f"🔧 Using MOCK ChatCompletionsClient (endpoint: {endpoint})")
    
    async def complete(self, model: str = None, messages: List[Dict] = None, stream: bool = False, **kwargs):
        """Mock chat completion with streaming support"""
        mock_response = "Este é um mock de resposta do AI Chat. Configure AZURE_EXISTING_AIPROJECT_ENDPOINT com um valor real para usar a IA de verdade."
        
        if stream:
            return MockAsyncIterator(mock_response)
        else:
            return {
                "choices": [
                    {
                        "message": {
                            "content": mock_response
                        }
                    }
                ]
            }
    
    async def close(self):
        pass

class MockEmbeddingsClient:
    """Mock EmbeddingsClient for local development"""
    
    def __init__(self, endpoint: str, credential, credential_scopes: List[str]):
        self.endpoint = endpoint
        self.credential = credential
        self.credential_scopes = credential_scopes
        print(f"🔧 Using MOCK EmbeddingsClient (endpoint: {endpoint})")
    
    async def embed(self, input_data, **kwargs):
        """Mock embeddings"""
        if isinstance(input_data, str):
            input_data = [input_data]
        
        return {
            "data": [
                {"embedding": [0.1] * 1536, "index": i}
                for i in range(len(input_data))
            ]
        }
    
    async def close(self):
        pass

class MockAIProjectClient:
    """Mock AIProjectClient for local development"""
    
    def __init__(self, credential, endpoint: str):
        self.credential = credential
        self.endpoint = endpoint
        self.telemetry = MockTelemetry()
        print(f"🔧 Using MOCK AIProjectClient (endpoint: {endpoint})")
    
    async def close(self):
        pass

class MockTelemetry:
    """Mock telemetry for local development"""
    
    async def get_application_insights_connection_string(self):
        return None
