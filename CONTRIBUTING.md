# Contributing

## Jira + GitHub workflow

- Always include a Jira issue key in branch names, commit messages, and PR titles.
  - Branch example: `feature/PROJ-123-student-db-ui`
  - Commit example: `PROJ-123 Create GUI for student DB`
  - PR title example: `PROJ-123 Create GUI for student DB`

## Set commit template (optional)

- Run once locally to use the provided template:
  - `git config commit.template .gitmessage.txt`

## Smart commits (optional)

- If GitHub for Jira is installed, you can use Smart Commits in commit messages:
  - `PROJ-123 #comment Add seed data #time 15m #transition Done`

## Install GitHub for Jira (admin steps)

1. In Jira Cloud (admin):
   - Go to `Settings -> Apps -> Explore more apps`, search and install "GitHub for Jira" by Atlassian.
   - Open `Apps -> Manage apps -> GitHub for Jira -> Get started` and click `Connect GitHub organization`.
2. Authorize in GitHub:
   - Approve the GitHub App installation for your organization/user.
   - Select this repository `Miiduoa/0925SQL` (or the whole org, if preferred).
3. Verify sync:
   - In Jira, the GitHub for Jira app should show the org and repo as `Connected` and `Synced`.
4. Test linkage:
   - Create a Jira issue (e.g., `PROJ-1`).
   - Create a branch `feature/PROJ-1-try-link` and push.
   - Open a PR with title starting with `PROJ-1 ...`.
   - Confirm the issue shows the linked branch/PR/commits in Jira.

## CI validation

- This repo includes a GitHub Action `jira-key-check.yml` that fails PRs whose titles do not include a Jira key (e.g., `PROJ-123`).
- To enforce this, protect your `main` branch in GitHub and require the check to pass before merging.

