---
name: up
description: Creates an azd environment, checks prerequisites (RBAC, model quota), provisions the AI chat app infrastructure via `azd up`, and health-checks the deployed app.
---

# Up Skill

## Goal

Provision a fresh Azure environment end-to-end and verify the app starts successfully.

## Before starting

When the skill is triggered, **always re-read this SKILL.md file** from disk before
executing, in case it has been updated since the last run.

Then proceed to **Step 1 (Choose environment name)** immediately — the user must pick
an environment before anything else.

## Terminal usage

All shell commands in this skill **must** be run using the `powershell` tool with
`mode="sync"`. Use a short `initial_wait` (30 seconds) for quick commands like
`az account show`, `az ad signed-in-user show`, `az role assignment list`,
`azd env list`, `azd env new`, and `azd env set`.

**Exception — `azd up` and `azd down`:** These long-running commands **must** be run
with `mode="async"` and a short `initial_wait` (10 seconds) so the user can see
streaming progress output in real time (just like running in a terminal). After
launching, **poll frequently** using `read_powershell` with a **short delay (15–20
seconds)** — this is critical so the user sees output updates as they happen, similar
to watching the command in a terminal. Keep calling `read_powershell` in a loop
(each call in a new response turn) until the command completes or you receive a
completion notification. Do NOT use long delays like 120 seconds — that defeats the
purpose of streaming output.

Chain short related commands with `&&` or `;` into a single `powershell` call
when they have no branching logic between them.

## Steps

### 1. Choose environment name

#### 1a. Resolve existing environment

First, check whether there is already a default azd environment:

```powershell
$existingEnvs = azd env list -o json 2>$null | ConvertFrom-Json
```

Find the default environment (the entry where `IsDefault` is `true` or the `DefaultEnvironment`
field is set, depending on the azd version).

#### 1b. Generate a suggested new name

Regardless of whether a default environment exists, always prepare a suggested new name
for use as a choice.

Scan `$existingEnvs` for names matching the pattern `<prefix><number>` (e.g., `aichat1`,
`test-env3`, `chat-2`). If found, take the one with the **highest number** and suggest
the next increment (e.g., `aichat2`, `test-env4`, `chat-3`).

If no numbered environments exist, generate a default name:

```powershell
$suffix = -join ((0..9) + ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z') | Get-Random -Count 6)
$suggestedName = "aichat-$suffix"
```

#### 1c. Ask the user

**If a default environment was found**, present the user with choices:

1. **Use the current environment `<defaultEnvName>`** — re-provision/update the existing
   environment (first choice, include the environment name in the label)
2. **Create a new environment `<suggestedName>`** — use the suggested new name from 1b
3. **Enter a different name** — the user provides their own name

For example:

> Do you want to `azd up` the current environment **`aichat2`**, or create a new one?

**If no default environment was found**, present the user with choices:

1. **Use the suggested name `<suggestedName>`** — use the name generated in 1b
2. **Enter a different name** — the user provides their own name

- If the user **provides a different name**, use their name instead.
- Environment names must be **lowercase alphanumeric and hyphens only**, max 64 characters.

The resource group will be `rg-<envName>`.

### 1½. Check for existing AI project (shortcut)

After resolving the environment name, check whether the selected environment already has
`AZURE_EXISTING_AIPROJECT_RESOURCE_ID` set:

```powershell
$existingProject = azd env get-value AZURE_EXISTING_AIPROJECT_RESOURCE_ID --environment $envName 2>$null
```

If the value is **non-empty**, the environment is pre-configured to use an existing AI project.
Print the **short-path** steps overview and **jump directly to Step 8 (`azd up`)**:

> **Up Skill — Steps Overview** (environment: `<envName>`, existing AI project)
>
> 1. ✅ Choose environment name
> 2–7. ⏭️ Skipped (existing AI project detected)
> 8. Run `azd up`
> 9. Retrieve the app endpoint
> 10. Health-check the app
> 11. Report results

If the value is **empty or not set**, print the **full-path** steps overview and continue
to Step 2:

> **Up Skill — Steps Overview** (environment: `<envName>`)
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

### 2. Resolve subscription

Auto-detect the default Azure Subscription ID using this priority order (use the first one found):

1. Environment variable `AZURE_SUBSCRIPTION_ID`
2. `azd config get defaults.subscription` (may return empty)
3. `az account show --query id -o tsv` (current Azure CLI login)

Present the user with **2 choices**:

1. **Use the detected subscription** — show the subscription ID (and name if available via
   `az account show --query "{id:id, name:name}" -o json`) as the default choice
2. **Enter a different subscription** — prompt the user to input a subscription ID

If no subscription was detected, skip choice 1 and ask the user to provide one directly.

Show the resolved subscription to the user for confirmation before proceeding.

### 3. Check RBAC permissions (prerequisite)

Verify the user has sufficient permissions to create role assignments on the subscription,
which is required for provisioning. The user needs **Owner** or **User Access Administrator**
— either assigned directly or inherited through a group membership.

#### 3a. Check direct role assignments

```powershell
$principalId = az ad signed-in-user show --query id -o tsv
$subScope = "/subscriptions/<subscriptionId>"
$roles = az role assignment list --assignee $principalId --scope $subScope --query "[].roleDefinitionName" -o json | ConvertFrom-Json
```

Check if `$roles` contains `Owner` or `User Access Administrator`.

- If **yes**, proceed to Step 4.
- If **no**, continue to 3b to check group-based assignments.

#### 3b. Check group-based role assignments

The user may hold the required role through a group membership. Query the user's group
memberships and check whether any of those groups have the required roles on the subscription.

```powershell
$groupIds = az ad signed-in-user get-member-of --query "[].id" -o json | ConvertFrom-Json
```

If `$groupIds` is non-empty, check role assignments for each group on the subscription:

```powershell
$groupRoles = @()
foreach ($gid in $groupIds) {
    $gr = az role assignment list --assignee $gid --scope $subScope --query "[].roleDefinitionName" -o json 2>$null | ConvertFrom-Json
    if ($gr) { $groupRoles += $gr }
}
```

Check if `$groupRoles` contains `Owner` or `User Access Administrator`.

- If **yes**, proceed to Step 4.
- If **no**, report the issue:
  - Show the **subscription name and ID** that failed the check
  - Show the user's current roles on the subscription
  - Explain that `azd up` will fail because the deployment creates `Microsoft.Authorization/roleAssignments`
  - Present **3 choices**:
    1. **"I just added the role — re-check"** → Re-run the RBAC check on the same subscription
    2. **"Use a different subscription"** → Prompt the user for a new subscription ID, then go back to Step 3
    3. **"Exit"** → Stop the skill

### 4. Resolve region

Check environment variable `AZURE_LOCATION` first. If not set,
ask the user — must be one of: `eastus`, `eastus2`, `swedencentral`, `westus`, `westus3`.
Default to `eastus` if the user has no preference.

Show the resolved region to the user for confirmation before proceeding.

### 5. Check chat model quota (prerequisite)

Before provisioning, verify the default chat model has sufficient quota in the selected region.

**Default model:** `gpt-4o-mini` | **SKU:** `GlobalStandard` | **Required capacity:** 80

#### 5a. Query quota and model availability

```powershell
$usage = az cognitiveservices usage list --location <region> --subscription <subscriptionId> -o json | ConvertFrom-Json
$modelList = az cognitiveservices model list --location <region> --subscription <subscriptionId> -o json | ConvertFrom-Json
```

Cache both `$usage` and `$modelList` for potential reuse.

#### 5b. Check default chat model quota

```powershell
$defaultUsageName = "OpenAI.GlobalStandard.gpt-4o-mini"
$entry = $usage | Where-Object { $_.name.value -eq $defaultUsageName }
```

If the entry exists, compute `available = limit - currentValue`.

- If `available >= 80`, the default model has enough quota — **skip to Step 6**.
- If the entry is **missing**, the model/SKU is not available in this region — continue to 5c.
- If `available < 80`, quota is insufficient — continue to 5c.

Report the finding to the user (e.g., "gpt-4o-mini has 40/80 quota available — insufficient").

#### 5c. Find alternative chat models

From the quota usage list, find all GPT entries with `Global` or `GlobalStandard` SKUs
that have sufficient available quota:

```powershell
$gptEntries = $usage | Where-Object {
    $_.name.value -match '^OpenAI\.(Global|GlobalStandard)\.gpt-' -and
    ($_.limit - $_.currentValue) -ge 80
}
```

For each candidate, **cross-reference with `$modelList`** to confirm the model is actually
deployable (exists with format `OpenAI` and is not retired). Discard any candidate not
confirmed by the model list.

#### 5d. Rank chat model candidates

Use this preference order (higher is better):

1. `gpt-4o-mini`
2. `gpt-4.1-mini`
3. `gpt-5-mini`
4. `gpt-4o`
5. `gpt-4.1`
6. `gpt-5`

Within the same model name, prefer `GlobalStandard` over `Global`.

#### 5e. Suggest the best alternative

Present the top candidate to the user with:

- Model name
- SKU type (`Global` or `GlobalStandard`)
- Available quota

Ask for confirmation before proceeding.

#### 5f. Resolve chat model version

For the selected model, look up the version from the model list:

```powershell
$match = $modelList | Where-Object {
    $_.model.name -eq '<selectedModel>' -and
    $_.model.format -eq 'OpenAI'
}
```

If multiple versions exist, prefer the **newest Generally Available** version.
If only preview versions exist, warn the user before proceeding.

Store the resolved chat model name, SKU, and version for use in Step 7.

#### 5g. No chat model quota available

If **no** GPT model in `Global` or `GlobalStandard` has sufficient quota (≥ 80) in the
selected region, stop and report the issue. Suggest the user try a different region or
request a quota increase.

### 6. Create the azd environment

If the user chose an **existing** environment in Step 1c, skip this step — the environment
already exists. Proceed directly to Step 7.

If the user chose a **new** environment name, create it:

```powershell
azd env new $envName --no-prompt
```

If this fails, stop and report the error.

### 7. Set subscription, region, and model overrides

```powershell
azd env set AZURE_SUBSCRIPTION_ID <subscriptionId> --environment $envName --no-prompt
azd env set AZURE_LOCATION <region> --environment $envName --no-prompt
```

Use the values collected in Steps 2 and 4.

If Step 5 determined an alternative chat model, apply the chat model overrides:

```powershell
azd env set AZURE_AI_CHAT_MODEL_NAME "<selectedChatModel>" --environment $envName --no-prompt
azd env set AZURE_AI_CHAT_DEPLOYMENT_NAME "<selectedChatModel>" --environment $envName --no-prompt
azd env set AZURE_AI_CHAT_DEPLOYMENT_SKU "<selectedChatSku>" --environment $envName --no-prompt
azd env set AZURE_AI_CHAT_MODEL_VERSION "<selectedChatVersion>" --environment $envName --no-prompt
azd env set AZURE_AI_CHAT_MODEL_FORMAT "OpenAI" --environment $envName --no-prompt
azd env set AZURE_AI_CHAT_DEPLOYMENT_CAPACITY "80" --environment $envName --no-prompt
```

### 8. Run `azd up`

This provisions infrastructure and deploys the app. It typically takes 10–15 minutes.

Run with `mode="async"` so the user sees live streaming output:

```powershell
azd up --environment $envName --no-prompt
```

After launching, **poll with short delays** — call `read_powershell` with a **15–20 second
delay** on each turn, and show the user whatever new output appeared. Repeat in a loop
(one `read_powershell` per response turn) until the command completes. This gives the
user a near-real-time view of provisioning progress. Do NOT use 120-second delays.

- If `azd up` **fails**, report the error and offer to run `azd down --environment $envName --force --purge --no-prompt` (also `mode="async"`) to clean up.
- If `azd up` **succeeds**, proceed to the health check.

### 9. Retrieve the app endpoint

After `azd up` succeeds, get the deployed app URL:

```powershell
$serviceUri = azd env get-value SERVICE_API_URI --environment $envName
```

If that returns empty, fall back to reading `.azure/<envName>/.env` and parsing the `SERVICE_API_URI` line.

### 10. Health-check the app

Try up to 5 times (15 seconds apart) to reach the app:

```powershell
$healthy = $false
for ($i = 1; $i -le 5; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri $serviceUri -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400) {
            $healthy = $true
            Write-Host "Attempt $i - HTTP $($resp.StatusCode) - App is running!"
            break
        }
    } catch {
        Write-Host "Attempt $i - $($_.Exception.Message)"
    }
    if ($i -lt 5) { Start-Sleep -Seconds 15 }
}
```

### 11. Report results

Print a summary with:

| Field            | Value                        |
|------------------|------------------------------|
| Subscription     | `<subscriptionId>`           |
| Environment      | `$envName`                   |
| Resource Group   | `rg-$envName`                |
| Region           | `<region>`                   |
| Chat Model       | `<chatModel>` (`<chatSku>`)  |
| App URL          | `$serviceUri`                |
| Status           | ✅ PASS or ❌ FAIL            |

- **PASS** = `azd up` succeeded AND health check returned HTTP 2xx/3xx.
- **FAIL** = either `azd up` failed or the app did not respond after 5 retries.

If the test **failed**, ask the user whether to tear down with:
```powershell
azd down --environment $envName --force --purge --no-prompt
```

If the test **passed**, congratulate and remind them the environment is still running (costs apply) and offer to tear it down.
