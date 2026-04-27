# `/up` Skill — Example Output

This is a sample interaction showing what the `/up` skill looks like when run
end-to-end through the **full path** (all steps).

---

## Step 1 — Choose environment name

```
> azd env list -o json
```

Detected environments:
- `my-chat-1` (non-default)
- `my-chat-2` (default) ✅

**Copilot asks:**
> Do you want to `azd up` the current environment **`my-chat-2`**, or create a new one?
>
> 1. Use current environment my-chat-2
> 2. Create new environment my-chat-3

**User selects:** Use current environment my-chat-2

---

## Step 1½ — Check for existing AI project

```
> azd env get-value AZURE_EXISTING_AIPROJECT_RESOURCE_ID --environment my-chat-2
```

No existing AI project detected — proceeding with **full path**.

> **Up Skill — Steps Overview** (environment: `my-chat-2`)
>
> 1. ✅ Choose environment name
> 2. Resolve subscription
> 3. Check RBAC permissions
> 4. Resolve region
> 5. Check chat model quota
> 6. Create the azd environment
> 7. Set subscription, region, and model overrides
> 8. Run `azd up`
> 9. Retrieve the app endpoint
> 10. Health-check the app
> 11. Report results

---

## Step 2 — Resolve subscription

```
> az account show --query "{id:id, name:name}" -o json
```

Detected subscription: **My Subscription** (`00000000-0000-0000-0000-000000000000`)

**Copilot asks:**
> Which subscription should I use?
>
> 1. Use detected subscription 00000000-0000-0000-0000-000000000000 (My Subscription)
> 2. Enter a different subscription

**User selects:** Use detected subscription

---

## Step 3 — Check RBAC permissions

### 3a. Check direct role assignments

```
> az ad signed-in-user show --query id -o tsv
aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

> az role assignment list --assignee aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee \
    --scope "/subscriptions/00000000-0000-0000-0000-000000000000" \
    --query "[].roleDefinitionName" -o json
[]
```

No direct Owner or User Access Administrator role found. Checking group memberships...

### 3b. Check group-based role assignments

```
> az rest --method GET --url "https://graph.microsoft.com/v1.0/me/memberOf"
```

Found user is a member of multiple groups. Cross-referencing with subscription role
assignments...

```
> az role assignment list --scope "/subscriptions/00000000-0000-0000-0000-000000000000" \
    --query "[?roleDefinitionName=='Owner' || roleDefinitionName=='User Access Administrator']" -o json
```

✅ User is a member of group `11111111-2222-3333-4444-555555555555` which has **Owner**
role on the subscription. RBAC check passed.

---

## Step 4 — Resolve region

`AZURE_LOCATION` is not set.

**Copilot asks:**
> Which Azure region should I use?
>
> 1. eastus (Recommended)
> 2. eastus2
> 3. swedencentral
> 4. westus
> 5. westus3

**User selects:** swedencentral

---

## Step 5 — Check chat model quota

```
> az cognitiveservices usage list --location swedencentral \
    --subscription 00000000-0000-0000-0000-000000000000 -o json
```

Checking default model **gpt-4o-mini** (GlobalStandard, need 80 capacity)...

✅ `gpt-4o-mini` GlobalStandard has **148,000** available capacity in `swedencentral`
— more than sufficient.

---

## Step 6 — Create the azd environment

Skipped — user chose the existing environment `my-chat-2`.

---

## Step 7 — Set subscription, region, and model overrides

```
> azd env set AZURE_SUBSCRIPTION_ID 00000000-0000-0000-0000-000000000000 --environment my-chat-2
> azd env set AZURE_LOCATION swedencentral --environment my-chat-2
```

Using default chat model (gpt-4o-mini GlobalStandard) — no model overrides needed.

---

## Step 8 — Run `azd up`

```
> azd up --environment my-chat-2 --no-prompt
```

Streaming output (updates every ~15–20 seconds):

```
Packaging services (azd package)
  (✓) Done: Packaging service api_and_frontend

Provisioning Azure resources (azd provision)
Subscription: My Subscription (00000000-0000-0000-0000-000000000000)
Location: Sweden Central

Creating/Updating resources
  (✓) Done: Resource group: rg-my-chat-2 (12.5s)
  (✓) Done: Log Analytics workspace: log-abc123xyz (29.6s)
  (✓) Done: Storage account: stabc123xyz (28.8s)
  (✓) Done: Application Insights: appi-abc123xyz (10.0s)
  (✓) Done: Foundry: aoai-abc123xyz (26.0s)
  (✓) Done: Azure AI Services Model Deployment: aoai-abc123xyz/gpt-4o-mini (4.0s)
  (✓) Done: Foundry project: aoai-abc123xyz/proj-abc123xyz (11.9s)
  (✓) Done: Container Registry: crabc123xyz (23.6s)
  (✓) Done: Container Apps Environment: containerapps-env-abc123xyz (53.7s)
  (✓) Done: Container App: ca-api-abc123xyz (8m39.0s)

Deploying services (azd deploy)
  Publishing service api_and_frontend (Uploading remote build context)
  Deploying service api_and_frontend (Updating container app revision)
  (✓) Done: Deploying service api_and_frontend
  - Endpoint: https://ca-api-abc123xyz.example-a1b2c3d4.swedencentral.azurecontainerapps.io/

SUCCESS: Your up workflow to provision and deploy to Azure completed in 15 minutes 31 seconds.
```

---

## Step 9 — Retrieve app endpoint

```
> azd env get-value SERVICE_API_URI --environment my-chat-2
https://ca-api-abc123xyz.example-a1b2c3d4.swedencentral.azurecontainerapps.io
```

---

## Step 10 — Health-check

```
Attempt 1 - HTTP 200 - App is running!
```

---

## Step 11 — Results Summary

| Field            | Value                        |
|------------------|------------------------------|
| Subscription     | `00000000-0000-0000-0000-000000000000` (My Subscription) |
| Environment      | `my-chat-2`                  |
| Resource Group   | `rg-my-chat-2`               |
| Region           | `swedencentral`              |
| Chat Model       | `gpt-4o-mini` (`GlobalStandard`) |
| App URL          | https://ca-api-abc123xyz.example-a1b2c3d4.swedencentral.azurecontainerapps.io |
| Status           | ✅ PASS                       |

> 🎉 Deployment completed in **15m 31s**. Health check passed on first attempt.
>
> The environment is still running (costs apply). Would you like to tear it down?
