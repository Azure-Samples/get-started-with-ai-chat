---
page_type: sample
languages:
- azdeveloper
- bicep
- python
products:
- azure
- azure-openai
- azure-ai
- azure-cognitive-search
- azure-container-apps
urlFragment: azureai-basic-python
name: Azure AI basic template (Python)
description: Creates an Azure AI Studio hub, project and required dependent resources including Azure AI Services, Azure AI Search and more. Deploys a simple chat application.
---
<!-- YAML front-matter schema: https://review.learn.microsoft.com/en-us/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# Azure AI Studio Starter Template

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/azureai-basic-python)
[![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/azureai-basic-python)

This project creates an Azure AI Studio hub, project and connected resources including Azure AI Services, AI Search and more. It also deploys a simple chat application to Azure Container Apps.

* [Features](#features)
* [Architecture diagram](#architecture-diagram)
* [Getting started](#getting-started)
  * [GitHub Codespaces](#github-codespaces)
  * [VS Code Dev Containers](#vs-code-dev-containers)
  * [Local environment](#local-environment)
* [Deploying](#deploying)
* [Development server](#development-server)
* [Guidance](#guidance)
* [Resources](#resources)
* [Testing](#testing)

## Features

This template creates everything you need to get started with Azure AI Studio:

* [AI Hub Resource](https://learn.microsoft.com/azure/ai-studio/concepts/ai-resources)
* [AI Project](https://learn.microsoft.com/azure/ai-studio/how-to/create-projects)
* [Azure AI Service](https://learn.microsoft.com/azure/ai-services): Default models deployed are gpt-4o-mini and text-embedding-ada-002, but any Azure AI models can be specified per the [documentation](docs/deploy_customization.md#customizing-model-deployments).
* [AI Search Service](https://learn.microsoft.com/azure/search/) *(Optional, disabled by default)*

The template also includes dependent resources required by all AI Hub resources:

* [Storage Account](https://learn.microsoft.com/azure/storage/blobs/)
* [Key Vault](https://learn.microsoft.com/azure/key-vault/general/)
* [Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview) *(Optional, enabled by default)*
* [Container Registry](https://learn.microsoft.com/azure/container-registry/) *(Optional, enabled by default)*

## Architecture diagram

![Architecture diagram showing that user input used in conjunction with user identity to call app code running in Azure Container apps that processes the user input and generates a response to the user. The app code leverages Azure AI projects, Azure AI model inference, prompty, and Azure AI Search.](docs/architecture.png)

## Getting started

You have a few options for getting started with this template.
The quickest way to get started is GitHub Codespaces, since it will setup all the tools for you, but you can also [set it up locally](#local-environment).

### GitHub Codespaces

You can run this template virtually by using GitHub Codespaces. The button will open a web-based VS Code instance in your browser:

1. Open the template (this may take several minutes):

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/azureai-basic-python)

2. Open a terminal window
3. Continue with the [deploying steps](#deploying)

### VS Code Dev Containers

A related option is VS Code Dev Containers, which will open the project in your local VS Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Start Docker Desktop (install it if not already installed)
2. Open the project:

    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/azureai-basic-python)

3. In the VS Code window that opens, once the project files show up (this may take several minutes), open a terminal window.
4. Continue with the [deploying steps](#deploying)

### Local environment

If you're not using one of the above options for opening the project, then you'll need to:

1. Make sure the following tools are installed:

    * [Azure Developer CLI (azd)](https://aka.ms/install-azd)
    * [Python 3.9+](https://www.python.org/downloads/)
    * [Docker Desktop](https://www.docker.com/products/docker-desktop/)
    * [Git](https://git-scm.com/downloads)

2. Download the project code:

    ```shell
    azd init -t azureai-basic-python
    ```

3. Open the project folder in your terminal or editor.

4. Continue with the [deploying steps](#deploying).

## Deploying

Once you've opened the project in [Codespaces](#github-codespaces), in [Dev Containers](#vs-code-dev-containers), or [locally](#local-environment), you can deploy it to Azure.

### Azure account setup

1. Sign up for a [free Azure account](https://azure.microsoft.com/free/) and create an Azure Subscription.
2. Check that you have the necessary permissions:
    * Your Azure account must have `Microsoft.Authorization/roleAssignments/write` permissions, such as [Role Based Access Control Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#role-based-access-control-administrator-preview), [User Access Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#user-access-administrator), or [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#owner).
    * Your Azure account also needs `Microsoft.Resources/deployments/write` permissions on the subscription level.

### Deploying with azd

1. Login to Azure:

    ```shell
    azd auth login
    ```

2. (Optional) If you would like to customize the deployment to [disable resources](docs/deploy_customization.md#disabling-resources), [customize resource names](docs/deploy_customization.md#customizing-resource-names),
or [customize the models](docs/deploy_customization.md#customizing-model-deployments), you can follow those steps now.

3. Provision and deploy all the resources:

    ```shell
    azd up
    ```

    It will prompt you to provide an `azd` environment name (like "azureaiapp"), select a subscription from your Azure account, and select a location which has quota for all the resources. Then it will provision the resources in your account and deploy the latest code. If you get an error or timeout with deployment, changing the location can help, as there may be availability constraints for the resources.

4. When `azd` has finished deploying, you'll see an endpoint URI in the command output. Visit that URI, and you should see the app! 🎉

5. You can now proceed to run the [development server](#development-server) to test the app locally, or if you are done trying out the app, you can delete the resources by running `azd down`.

### Bringing an existing AI project resource

If you have an existing AI project resource, you can bring it into the Azure AI Studio Starter Template by setting the following environment variable:

```shell
azd env set AZURE_EXISTING_AIPROJECT_CONNECTION_STRING "<connection-string>"
```

You can find the connection string on the overview page of your Azure AI project.

If you do not have a deployment named "gpt-4o-mini" in your existing AI project, you should either create one in Azure AI studio or follow the steps in [Customizing model deployments](#customizing-model-deployments) to specify a different model.

## Development server

Make sure you first [deployed the app](#deploying) to Azure before running the development server.

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

    On Windows:

    ```shell
    py -3 -m venv .venv
    .venv\scripts\activate
    ```

    On Linux:

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Navigate to the `src` directory:

    ```shell
    cd src
    ```

3. Install required Python packages:

    ```shell
    python -m pip install -r requirements.txt
    ```

4. Run the local server:

    ```shell
    python -m uvicorn "api.main:create_app" --factory --reload
    ```

5. Click 'http://127.0.0.1:8000' in the terminal, which should open a new tab in the browser.

6. Enter your message in the box.

## Testing

### Setting up the development environment

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

    On Windows:

    ```shell
    py -3 -m venv .venv
    .venv\scripts\activate
    ```

    On Linux:

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Navigate to the project directory:

    ```shell
    cd <project-directory>
    ```

3. Install required Python packages:

    ```shell
    python -m pip install -r requirements-dev.txt
    ```

### Running tests

1. Run the tests with coverage:

    ```shell
    pytest --cov=src
    ```

## Guidance

### Costs

Pricing varies per region and usage, so it isn't possible to predict exact costs for your usage.
The majority of the Azure resources used in this infrastructure are on usage-based pricing tiers.
However, Azure Container Registry has a fixed cost per registry per day.

You can try the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator) for the resources:

* Azure AI Studio: Free tier. [Pricing](https://azure.microsoft.com/pricing/details/ai-studio/)
* Azure AI Search: Standard tier, S1. Pricing is based on the number of documents and operations. [Pricing](https://azure.microsoft.com/pricing/details/search/)
* Azure Storage Account: Standard tier, LRS. Pricing is based on storage and operations. [Pricing](https://azure.microsoft.com/pricing/details/storage/blobs/)
* Azure Key Vault: Standard tier. Pricing is based on the number of operations. [Pricing](https://azure.microsoft.com/pricing/details/key-vault/)
* Azure AI Services: S0 tier, defaults to gpt-4o-mini and text-embedding-ada-002 models. Pricing is based on token count. [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)
* Azure Container App: Consumption tier with 0.5 CPU, 1GiB memory/storage. Pricing is based on resource allocation, and each month allows for a certain amount of free usage. [Pricing](https://azure.microsoft.com/pricing/details/container-apps/)
* Azure Container Registry: Basic tier. [Pricing](https://azure.microsoft.com/pricing/details/container-registry/)
* Log analytics: Pay-as-you-go tier. Costs based on data ingested. [Pricing](https://azure.microsoft.com/pricing/details/monitor/)

⚠️ To avoid unnecessary costs, remember to take down your app if it's no longer in use,
either by deleting the resource group in the Portal or running `azd down`.

### Security guidelines

This template uses Azure AI Studio connections to communicate between resources, which stores keys in Azure Key Vault.
This template also uses [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) for local development and deployment.

To ensure continued best practices in your own repository, we recommend that anyone creating solutions based on our templates ensure that the [Github secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) setting is enabled.

You may want to consider additional security measures, such as:

* Enabling Microsoft Defender for Cloud to [secure your Azure resources](https://learn.microsoft.com/azure/security-center/defender-for-cloud).
* Protecting the Azure Container Apps instance with a [firewall](https://learn.microsoft.com/azure/container-apps/waf-app-gateway) and/or [Virtual Network](https://learn.microsoft.com/azure/container-apps/networking?tabs=workload-profiles-env%2Cazure-cli).

### Resources

Links to documentation for the resources used in this template.
