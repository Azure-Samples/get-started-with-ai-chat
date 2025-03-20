@description('The AI Foundry Hub Resource name')
param name string
@description('The display name of the AI Foundry Hub Resource')
param displayName string = name
@description('The storage account ID to use for the AI Foundry Hub Resource')
param storageAccountId string
@description('The key vault ID to use for the AI Foundry Hub Resource')
param keyVaultId string
@description('The application insights ID to use for the AI Foundry Hub Resource')
param applicationInsightsId string = ''
@description('The container registry ID to use for the AI Foundry Hub Resource')
param containerRegistryId string = ''
@description('The AI Services account name to use for the AI Foundry Hub Resource')
param aiServicesName string
@description('The AI Services connection name to use for the AI Foundry Hub Resource')
param aiServicesConnectionName string
@description('The AI Services Content Safety connection name to use for the AI Foundry Hub Resource')
param aiServicesContentSafetyConnectionName string
@description('The Azure Cognitive Search service name to use for the AI Foundry Hub Resource')
param aiSearchName string = ''
@description('The Azure Cognitive Search service connection name to use for the AI Foundry Hub Resource')
param aiSearchConnectionName string


@description('The SKU name to use for the AI Foundry Hub Resource')
param skuName string = 'Basic'
@description('The SKU tier to use for the AI Foundry Hub Resource')
@allowed(['Basic', 'Free', 'Premium', 'Standard'])
param skuTier string = 'Basic'
@description('The public network access setting to use for the AI Foundry Hub Resource')
@allowed(['Enabled','Disabled'])
param publicNetworkAccess string = 'Enabled'

param location string = resourceGroup().location
param tags object = {}

resource hub 'Microsoft.MachineLearningServices/workspaces@2024-07-01-preview' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: skuName
    tier: skuTier
  }
  kind: 'Hub'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: displayName
    storageAccount: storageAccountId
    keyVault: keyVaultId
    applicationInsights: !empty(applicationInsightsId) ? applicationInsightsId : null
    containerRegistry: !empty(containerRegistryId) ? containerRegistryId : null
    hbiWorkspace: false
    managedNetwork: {
      isolationMode: 'Disabled'
    }
    v1LegacyMode: false
    publicNetworkAccess: publicNetworkAccess
  }

  resource aiServiceConnection 'connections' = {
    name: aiServicesConnectionName
    properties: {
      category: 'AIServices'
      authType: 'AAD'
      isSharedToAll: true
      target: aiService.properties.endpoint
      metadata: {
        ApiVersion: '2025-01-01-preview'
        ApiType: 'azure'
        ResourceId: aiService.id
      }
    }
  }

  resource contentSafetyConnection 'connections' = {
    name: aiServicesContentSafetyConnectionName
    properties: {
      category: 'AzureOpenAI'
      authType: 'AAD'
      isSharedToAll: true
      target: aiService.properties.endpoints['Content Safety']
      metadata: {
        ApiVersion: '2025-01-01-preview'
        ApiType: 'azure'
        ResourceId: aiService.id
      }
    }
  }

  resource searchConnection 'connections' =
    if (!empty(aiSearchName)) {
      name: aiSearchConnectionName
      properties: {
        category: 'CognitiveSearch'
        authType: 'ApiKey'
        isSharedToAll: true
        target: 'https://${search.name}.search.windows.net/'
        credentials: {
          key: !empty(aiSearchName) ? search.listAdminKeys().primaryKey : ''
        }
      }
    }
}

resource aiService 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: aiServicesName
}

resource search 'Microsoft.Search/searchServices@2021-04-01-preview' existing =
  if (!empty(aiSearchName)) {
    name: aiSearchName
  }

output name string = hub.name
output id string = hub.id
output principalId string = hub.identity.principalId
