---
name: resolve-pr-comments
description: Workflow for AI agents to fetch, critically evaluate, and resolve GitHub Pull Request comments. Automatically trigger this skill when the user asks to "resolve comments", "fix pr", "fix comments", "address pr feedback", or "resolve pr comments".
---

# PR Review Comment Resolution Guide

This skill defines the step-by-step procedure for AI agents to retrieve, evaluate, and address review comments on GitHub Pull Requests (from automated reviewers like CodeRabbit/Sourcery or human reviewers).

---

## Trigger Phrases

Automatically activate and execute this skill whenever the user says or asks:
- `"resolve comments"`
- `"fix pr"`
- `"fix comments"`
- `"address pr feedback"`
- `"resolve review comments"`
- `"check pr comments"`

---

## Principles

1. **Critical Analysis**: NEVER make changes blindly. Evaluate whether each comment represents a valid issue before editing code.
2. **Selective Fixing**: Fix only valid bugs, security vulnerabilities, or meaningful improvements. Skip false positives or incorrect suggestions with technical justification.
3. **Verification**: Always run build/test verification after making changes before committing.

---

## Workflow Steps

### Step 1: Fetch PR Review Comments

Use the GitHub CLI (`gh`) to retrieve both conversation comments and inline code review comments:

```bash
# View PR summary and conversation thread
gh pr view <pr-number> --comments

# Fetch inline diff comments via GitHub API
gh api repos/{owner}/{repo}/pulls/<pr-number>/comments
```

---

### Step 2: Evaluate Each Comment

Categorize every review comment into one of the following buckets:

* **Category A: Valid Issue (Must Fix)**
  * Real bugs, security risks, broken logic, missing error handling, or performance bottlenecks.
  * Violations of project architecture rules (e.g., breaking layer boundaries).
  * *Action*: Implement targeted fix.

* **Category B: Invalid / False Positive (Do NOT Fix)**
  * Suggested changes based on incorrect assumptions about external libraries or frameworks.
  * Recommendations that break existing API contracts or architectural rules.
  * *Action*: Do not change code. Provide a clear, technical response explaining why the comment is invalid.

* **Category C: Style / Nitpick (Evaluate Contextually)**
  * Minor styling or naming suggestions.
  * *Action*: Adopt only if it aligns with existing repository style and improves readability.

---

### Step 3: Implement & Verify Fixes

1. Edit only the relevant code files.
2. Verify the changes locally (run tests, type checks, or linters).
3. Ensure no regressions or unintended side-effects were introduced.

---

### Step 4: Commit, Push & Respond on GitHub

1. Stage and commit valid fixes with clear commit messages:
   ```bash
   git add <modified-files>
   git commit -m "fix(pr): address review feedback for <feature>"
   git push origin <branch-name>
   ```

2. Post a resolution response on the PR summary thread explaining what was fixed and why any invalid comments were rejected:
   ```bash
   gh pr comment <pr-number> --body "## Review Feedback Resolution..."
   ```
