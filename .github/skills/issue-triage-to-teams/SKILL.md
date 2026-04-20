---
name: issue-triage-to-teams
description: Triage new GitHub issues by summarizing, classifying, proposing labels/assignees, and producing a Teams-ready notification message.
---

# Issue Triage → Teams Notification Skill

## Purpose
When a new GitHub issue is created, produce:
1) A short summary (1–3 bullets)
2) A classification: bug / feature / question / docs
3) Suggested labels (2–6)
4) A Teams-ready message body (short, scannable), including a deep link to the issue

This skill is designed to be used with GitHub issues in this repository and to generate consistent, high-signal notifications.

## Inputs (what you should look for)
- Issue title
- Issue body
- Issue author
- Issue URL
- Existing labels (if any)
- Repository context (README / contributing guidelines if needed)

## Workflow
1. **Read the issue**: title + body.
2. **Summarize** in 1–3 bullets. Keep it factual; do not invent details.
3. **Classify** as one of:
   - `bug` (unexpected behavior, regression, crash, incorrect output)
   - `feature` (new capability request)
   - `question` (how-to, clarification, usage)
   - `docs` (documentation improvements)
4. **Propose labels**:
   - Always include one of: `type:bug`, `type:feature`, `type:question`, `type:docs`
   - Add `area:*` labels if the issue mentions a component
   - Add `priority:*` only if clearly implied (e.g., production down)
5. **Propose next action**:
   - What info is missing? (logs, repro steps, expected/actual)
   - Suggest a first investigation step
6. **Generate Teams message** (final output) using this template:

### Teams Message Template
**New Issue:** #{ISSUE_NUMBER} {ISSUE_TITLE}  
**Repo:** {REPO} | **Author:** {AUTHOR} | **Type:** {CLASSIFICATION}  
**Summary:**  
- {BULLET_1}
- {BULLET_2}
- {BULLET_3 (optional)}

**Suggested labels:** {LABELS_COMMA_SEPARATED}  
**Next step:** {ONE_SENTENCE_NEXT_STEP}  
**Link:** {ISSUE_URL}

## Guardrails
- Don’t guess. If info is missing, say so.
- Keep output short enough to fit within webhook message limits.
- Prefer neutral, actionable language.