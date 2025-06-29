
# Azure AI Foundry Starter Template: Deployment customization

This document describes how to customize the deployment of the Azure AI Foundry Starter Template. Once you follow the steps here, you can run `azd up` as described in the [Deploying](./../README.md#deploying-steps) steps.

* [Disabling resources](#disabling-resources)
* [Customizing resource names](#customizing-resource-names)
* [Customizing model deployments](#customizing-model-deployments)

## Disabling resources

* To disable AI Search, run `azd env set USE_SEARCH_SERVICE false`
* To disable Application Insights, run `azd env set USE_APPLICATION_INSIGHTS false`
* To disable Container Registry, run `azd env set USE_CONTAINER_REGISTRY false`

Then run `azd up` to deploy the remaining resources.

## Customizing resource names

By default this template will use a default naming convention to prevent naming collisions within Azure.
To override default naming conventions the following can be set.

* `AZURE_EXISTING_AIPROJECT_CONNECTION_STRING` - An existing connection string to be use.   If specified, resources for AI Foundry Hub,  AI Foundry Project, and Azure AI service will not be created.
* `AZURE_AIHUB_NAME` - The name of the AI Foundry Hub resource
* `AZURE_AIPROJECT_NAME` - The name of the AI Foundry Project
* `AZURE_AISERVICES_NAME` - The name of the Azure AI service
* `AZURE_SEARCH_SERVICE_NAME` - The name of the Azure Search service
* `AZURE_STORAGE_ACCOUNT_NAME` - The name of the Storage Account
* `AZURE_KEYVAULT_NAME` - The name of the Key Vault
* `AZURE_CONTAINER_REGISTRY_NAME` - The name of the container registry
* `AZURE_APPLICATION_INSIGHTS_NAME` - The name of the Application Insights instance
* `AZURE_LOG_ANALYTICS_WORKSPACE_NAME` - The name of the Log Analytics workspace used by Application Insights

To override any of those resource names, run `azd env set <key> <value>` before running `azd up`.

## Customizing model deployments

To customize the model deployments, you can set the following environment variables:

### Using a different chat model

Change the chat deployment name:

```shell
azd env set AZURE_AI_CHAT_DEPLOYMENT_NAME Phi-3.5-MoE-instruct
```

Change the chat model format (either OpenAI or Microsoft):

```shell
azd env set AZURE_AI_CHAT_MODEL_FORMAT Microsoft
```

Change the chat model name:

```shell
azd env set AZURE_AI_CHAT_MODEL_NAME Phi-3.5-MoE-instruct
```

Set the version of the chat model:

```shell
azd env set AZURE_AI_CHAT_MODEL_VERSION 2
```

### Setting models, capacity, and deployment SKU

By default, this template sets the chat model deployment capacity to 80,000 tokens per minute. For AI Search, the embedding model requires a capacity of 50,000 tokens per minute. Due to current Bicep limitations, only the chat model quota is validated when you select a location during `azd up`. If you want to change these defaults, set the desired region using `azd env set AZURE_LOCATION <region>` (for example, `eastus`) to bypass quota validation. Follow the instructions below to update the model settings before running `azd up`.

Change the default capacity (in thousands of tokens per minute) of the chat deployment:

```shell
azd env set AZURE_AI_CHAT_DEPLOYMENT_CAPACITY 50
```

Change the SKU of the chat deployment:

```shell
azd env set AZURE_AI_CHAT_DEPLOYMENT_SKU Standard
```

Change the default capacity (in thousands of tokens per minute) of the embeddings deployment:

```shell
azd env set AZURE_AI_EMBED_DEPLOYMENT_CAPACITY 50
```

Change the SKU of the embeddings deployment:

```shell
azd env set AZURE_AI_EMBED_DEPLOYMENT_SKU Standard
```

## Bringing an existing AI project resource

If you have an existing AI project resource, you can bring it into the Azure AI Foundry Starter Template by setting the following environment variable:

```shell
azd env set AZURE_EXISTING_AIPROJECT_CONNECTION_STRING "<connection-string>"
```

You can find the connection string on the overview page of your Azure AI project.

If you do not have a deployment named "gpt-4o-mini" in your existing AI project, you should either create one in Azure AI Foundry or follow the steps in [Customizing model deployments](#customizing-model-deployments) to specify a different model.
