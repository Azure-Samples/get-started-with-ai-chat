

# Retrieval-Augmented Generation (RAG) Setup Guide
## Overview
The Retrieval-Augmented Generation (RAG) feature helps improve the responses from your application by combining the power of large language models (LLMs) with extra context retrieved from an external data source. Simply put, when you ask a question, the application first searches through a set of relevant documents (stored as embeddings) and then uses this context to provide a more accurate and relevant response. If no relevant context is found, the application returns the LLM response directly.
This RAG feature is optional and enabled by default. If you prefer not to use it, simply set the local environment variable `USE_SEARCH_SERVICE` to `false`. Doing so will also skip creating the Azure AI Search resources by `azd up` command.

## How does RAG work in this application?
In our provided example, the application includes a sample dataset containing information about hiking products. This data was split into sentences, and each sentence was transformed into numerical representations called embeddings. These embeddings were created using OpenAI's `text-embedding-3-small` model with `dimensions=100`. The resulting embeddings file (`embeddings.csv`) is located in the `api/data` folder.

When you ask a question, the application:
 
1. Searches these embeddings for information relevant to your query.
2. Identifies relevant context if available.
3. Combines the retrieved context with the LLM to provide a better answer.

## If you want to use your own dataset
To create a custom embeddings file with your own data, you can use the provided helper class `SearchIndexManager`. Below is a straightforward way to build your own embeddings:
```python
from .api.search_index_manager import SearchIndexManager

search_index_manager = SearchIndexManager (
    endpoint=self.search_endpoint,
    credential=your_credentials,
    index_name=index_name,
    dimensions=100,
    model="text-embedding-3-small",
    embeddings_client=embedding_client,
)
await search_index_manager.build_embeddings_file(
    input_directory='data',
    output_file='data/embeddings.csv'
    sentences_per_embedding=4
)
```
- Make sure to replace `your_search_endpoint`, `your_credentials`, `your_index_name`, and `embedding_client` with your own Azure service details.
- Your input data should be placed in the folder specified by `input_directory`.
- `sentences_per_embedding  parameter`, specifies the number of sentences used to construct the embedding. The larger this number, the broader the context that will be identified during the similarity search.

## Deploying the Application with RAG enabled
To deploy your application using the RAG feature, set the following environment variables locally:
In power shell:
```
$env:USE_SEARCH_SERVICE="true"
$env:AZURE_AI_SEARCH_INDEX_NAME="index_sample"
$env:AZURE_AI_EMBED_DEPLOYMENT_NAME="text-embedding-3-small"
```

In bash:
```
export USE_SEARCH_SERVICE="true"
export AZURE_AI_SEARCH_INDEX_NAME="index_sample"
export AZURE_AI_EMBED_DEPLOYMENT_NAME="text-embedding-3-small"
```

In cmd:
```
set USE_SEARCH_SERVICE=true
set AZURE_AI_SEARCH_INDEX_NAME=index_sample
set AZURE_AI_EMBED_DEPLOYMENT_NAME=text-embedding-3-small
```

- `USE_SEARCH_SERVICE`: Enables (default) or disables RAG.
- `AZURE_AI_SEARCH_INDEX_NAME`: The Azure Search Index the application will use.
- `AZURE_AI_EMBED_DEPLOYMENT_NAME`: The Azure embedding deployment used to create embeddings.

**Note:** If either `AZURE_AI_SEARCH_INDEX_NAME` or `AZURE_AI_EMBED_DEPLOYMENT_NAME` is not provided, or the Azure AI Search service connection is unavailable, the application will run without using the RAG feature.

## Creating the Azure Search Index
 
To utilize RAG, you must have an Azure search index. By default, the application uses `index_sample` as the index name. You can create an index either by following these official Azure [instructions](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/azure-ai-search?tabs=azurecli%2Cpython&pivots=overview-azure-ai-search), or programmatically with the provided helper methods:
```python
# Create Azure Search Index (if it does not yet exist)
search_index_manager.ensure_index_created(vector_index_dimensions)

# Upload embeddings to the index
search_index_manager.upload_documents(embeddings_path)
```
**Important:** If you have already created the index before deploying your application, the system will skip this step and directly use your existing Azure Search Index. The parameter `vector_index_dimensions` is only required if dimension information was not already provided when initially constructing the `SearchIndexManager` object.