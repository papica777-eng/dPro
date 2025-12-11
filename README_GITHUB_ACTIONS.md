# GitHub Actions & required secrets

This repo has CI/CD workflows for building images, running tests, deploying to Render, and optional Firebase deployments.

Workflows

- `firebase-deploy.yml` — Deploy Firebase Cloud Functions & Hosting (in `dpengeneering-main`).
- `build-and-push-ghcr.yml` — Build and publish the root Flask Docker image to GHCR.
- `render-deploy.yml` — Build the Docker image, push to GHCR, and trigger a Render deploy.
- `render-pr-preview.yml` — Build a PR-specific image and create a Render preview service `dpro-pr-<PR_NUMBER>`.

GitHub Secrets

Set these under Settings → Secrets → Actions:

- `FIREBASE_TOKEN` (optional) — CI token for Firebase deployments.
- `FIREBASE_SERVICE_ACCOUNT` (optional) — base64-encoded Firebase service account JSON.
- `FIREBASE_PROJECT_ID` — Firebase project id.
- `GITHUB_TOKEN` (provided automatically) — used for GHCR login.
- `GHCR_PAT` (optional) — PAT to allow PR preview GHCR cleanup (requires `read:packages` and `delete:packages`).
- `RENDER_API_KEY` — Render API key (optional but required to create preview services)
- `RENDER_SERVICE_ID` — Render service ID to trigger for deploys.

Usage notes

- The PR preview workflow creates preview services and comments with health/ping results; it will delete the preview when the PR closes if `RENDER_API_KEY` and `GHCR_PAT` are available.
- The Render/Firebase workflows expect secrets; the GitHub Actions UI shows 'Context access might be invalid' warnings if secrets are not set; this is expected until you configure the secrets.
- The workflows use `environment: production` for production deploy gating; create a GitHub Environment named `production` and configure required reviewers to enable approvals.
# GitHub Actions & required secrets

Two CI/CD workflows were added for this repository:

- `.github/workflows/firebase-deploy.yml` — deploys the Firebase Cloud Functions and frontend located in `dpengeneering-main`.
- `.github/workflows/build-and-push-ghcr.yml` — builds the root Flask app Docker image and pushes it to GitHub Container Registry (GHCR).

Required GitHub Secrets

The workflows use the following secrets. Add these under Settings → Secrets → Actions:

- `FIREBASE_TOKEN` (optional) — a CI token from `firebase login:ci` for Firebase deployments.
- `FIREBASE_SERVICE_ACCOUNT` (optional) — base64-encoded JSON service account. If provided, the workflow decodes and uses it.
- `FIREBASE_PROJECT_ID` — the id of your Firebase project (e.g., `my-project-id`).
- `GITHUB_TOKEN` (provided automatically by GitHub) — used to login to GHCR from the workflow.
- `GHCR_PAT` (optional) — a Personal Access Token (PAT) to allow the preview workflow to cleanup GHCR images. Required scopes: `read:packages` and `delete:packages`. Org-owned repos may require `repo` depending on policy.

Render deployment secrets (optional but recommended if you use Render)

- `RENDER_API_KEY` — API key from your Render account (add as a GitHub secret).
- `RENDER_SERVICE_ID` — The Render service ID to trigger for deploys.
- `RENDER_PLAN` — (optional) Render plan for preview services, e.g., `starter`.
- `RENDER_REGION` — (optional) Render region for preview services, e.g., `oregon`.

How to obtain Render service ID and API key

1. Go to the Render Dashboard → Account → API Keys → Create Key. Save it as a GitHub secret `RENDER_API_KEY`.
2. Go to your Render Service → Settings → General → Service ID (copy it and store as `RENDER_SERVICE_ID`).

Render workflows

`render-deploy.yml`: builds and pushes Docker image to GHCR and triggers a Render deploy.

`render-pr-preview.yml`: builds a PR-specific image and creates/updates a Render preview service named `dpro-pr-<PR_NUMBER>`. The workflow will:

- wait for `/health` to succeed,
- run `/api/ping` smoke tests,
- POST a PR comment with status and a link to the preview,
- delete the preview service and cleanup GHCR image tags when the PR is closed (optional using `GHCR_PAT`).

How to set secrets

1. Go to GitHub repository → Settings → Secrets → Actions.
2. Add `FIREBASE_TOKEN` or `FIREBASE_SERVICE_ACCOUNT` and `FIREBASE_PROJECT_ID`.
3. Add `RENDER_API_KEY`, `RENDER_SERVICE_ID` and optionally `RENDER_PLAN`/`RENDER_REGION`.
4. To automatically cleanup per-PR GHCR images when preview services are removed, add `GHCR_PAT` with `read:packages` and `delete:packages` scopes.

Notes

- The Firebase workflow expects either `FIREBASE_TOKEN` or `FIREBASE_SERVICE_ACCOUNT` in repository secrets.
- If you prefer a different container registry, update `build-and-push-ghcr.yml` and supply registry secrets.

Recommended workflow pipeline

1. Pull Request: run tests and lint; optionally create a Render PR preview.
2. Merge to `main`: build & push to GHCR; deploy to Render; deploy Firebase hosting/functions.
3. Require approval: use GitHub Environments and restrict `environment: production` to require manual approval for production deploys.

Set up GitHub environment & approvals

1. Go to your repository → Settings → Environments.
2. Create an environment named `production`.
3. Under Protection rules, set required reviewers.
4. Add environment-level secrets for production (e.g., `RENDER_API_KEY`, `FIREBASE_SERVICE_ACCOUNT`) if required.

Triggering and approving production deploys (manual approval flow)

1. Merge PR into `main` or push a commit to `main`.
2. Visit the Actions tab and find the workflow run. The `deploy` job will pause for environment approval.
3. Authorized reviewers approve the environment deployment.
4. After approval, the `deploy` job continues and performs the Render/Firebase production deployment.

Why this is important

- Ensures a human is in the loop before deploying to production.
- Use PR previews to validate changes and run a preview smoke test before production approval.
# GitHub Actions & required secrets

Two CI/CD workflows were added for this repository:

- `.github/workflows/firebase-deploy.yml` — deploys the Firebase Cloud Functions and frontend located in `dpengeneering-main`.
- `.github/workflows/build-and-push-ghcr.yml` — builds the root Flask app Docker image and pushes it to GitHub Container Registry (GHCR).

Required GitHub Secrets

- `FIREBASE_TOKEN` (optional) — a CI token from `firebase login:ci` that allows deploys without a Service Account file.
- `FIREBASE_SERVICE_ACCOUNT` (optional) — base64-encoded JSON service account. If provided, the workflow will decode it and use it.
- `FIREBASE_PROJECT_ID` — the id of the Firebase project to deploy to (e.g., `my-project-id`).
- `GITHUB_TOKEN` (provided automatically by GitHub) — used to login to GHCR.
- `GHCR_PAT` (optional) — a Personal Access Token (PAT) that the PR preview workflow can use to delete preview images from GitHub Container Registry after a PR is closed. This token needs the following scopes: `read:packages` and `delete:packages` (and optionally `write:packages` if your workflows require uploading images from the user account). For org-owned repositories you may need `repo` permission depending on your organization policies.

Render deployment secrets (optional but recommended if you use Render):

- `RENDER_API_KEY` — API key from your Render account (add as a GitHub secret).
- `RENDER_SERVICE_ID` — The Render service ID that will be triggered for deploys.
- `RENDER_PLAN` — (optional) Render plan for preview services, e.g., `starter`.
- `RENDER_REGION` — (optional) Render region for preview services, e.g., `oregon`.

How to obtain Render service ID and API key:
1. Go to the Render Dashboard → Account → API Keys → Create Key. Save it as a GitHub secret `RENDER_API_KEY`.
2. Go to your Render Service → Settings → General → Service ID (copy it and store as `RENDER_SERVICE_ID`).

This repository also contains a `render-deploy.yml` GitHub Actions workflow that builds the root Docker image, publishes to GHCR, then triggers the Render service to deploy the updated container.

Pull Request preview deployments (Render PR Preview)

- A `render-pr-preview.yml` workflow is included that builds a PR-specific image and creates/updates a Render preview service named `dpro-pr-<PR_NUMBER>`.
- Required secret: `RENDER_API_KEY` and optionally `RENDER_PLAN` and `RENDER_REGION`.

After the Render PR preview deploys, the workflow will wait for `/health` to succeed and run a `/api/ping` smoke test.

The workflow posts a comment on the PR with the preview URL and the health/ping results. When the PR is closed, the preview service will be deleted and the PR will be updated with a comment.

How to set secrets:
1. Go to GitHub repository > Settings > Secrets > Actions.
2. Add `FIREBASE_TOKEN` or `FIREBASE_SERVICE_ACCOUNT` and `FIREBASE_PROJECT_ID`.
3. If you want GitHub Actions to automatically cleanup per-PR GHCR images when PRs are closed, add `GHCR_PAT` as a repository secret. Create a PAT in your GitHub account via: Settings → Developer settings → Personal access tokens → Generate new token, then select `read:packages` and `delete:packages` scopes (optionally `write:packages`), and click Generate token. Save that token as `GHCR_PAT`.

Notes:
- The Firebase workflow expects either a `FIREBASE_TOKEN` or a `FIREBASE_SERVICE_ACCOUNT` (base64-encoded) in repository secrets.
- The Build-and-Push workflow will push the image to ghcr.io. If you prefer to publish to Docker Hub, update the workflow accordingly and add `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets.

Recommended GitHub Workflow pipeline (professional):
1. Pull Request: run tests and lint, build non-pushed artifacts, and optionally run ephemeral preview deployments in Render (staging).
2. Merge to `main`: build and push Docker image to GHCR; deploy Flask app to Render via `render-deploy.yml`; deploy Firebase functions & hosting via `firebase-deploy.yml`.
3. Use `GITHUB_ENV` and `Environments` to approve production deploys; require code review/PR approvals before production.

Set up GitHub environment and approvals:
1. Go to your repository > Settings > Environments.
2. Create an environment named `production` (used by the workflows in this repo).
3. Under Protection rules, set required reviewers (individuals or teams) to approve production deployments.
4. Add environment-level secrets for production if needed (RENDER_API_KEY, FIREBASE_SERVICE_ACCOUNT, FIREBASE_TOKEN, etc.). Environment secrets can be limited to specific environments and are safer than repo secrets for production.
5. Now, any job that declares `environment: production` will pause and require an approval by the configured reviewers before it continues.

Triggering and approving production deploys (manual approval flow):
1. Merge PR into `main` or push a commit to `main`. That will run the `build_and_push` job automatically.
2. Open the Actions tab and locate the workflow run triggered by the push. The `deploy` job will be suspended because it uses `environment: production`.
3. An authorized reviewer (as defined in the Environment protection rules) must approve the environment deployment from the GitHub UI.
4. After approval, the `deploy` job will continue and perform the Render/Firebase production deployment.
5. The workflow will post deploy status and health summary as comments on the commit/PR.

Why this is important:
- This prevents direct pushes from accidentally deploying to production and ensures a human in the loop to validate releases.
- Use this together with PR previews to validate changes prior to production approval.
 # GitHub Actions & required secrets

Two CI/CD workflows were added for this repository:

- `.github/workflows/firebase-deploy.yml` — deploys the Firebase Cloud Functions and frontend located in `dpengeneering-main`.
- `.github/workflows/build-and-push-ghcr.yml` — builds the root Flask app Docker image and pushes it to GitHub Container Registry (GHCR).

Required GitHub Secrets
 
 - `FIREBASE_TOKEN` (optional) — a CI token from `firebase login:ci` that allows deploys without a Service Account file. Recommended if you prefer tokens.
- `FIREBASE_SERVICE_ACCOUNT` (optional) — base64-encoded JSON service account. If provided, the workflow will decode it and use it.
- `FIREBASE_PROJECT_ID` — the id of the Firebase project to deploy to (e.g., `my-project-id`).
 `GITHUB_TOKEN` (provided automatically by GitHub) — used to login to GHCR.
 `GHCR_PAT` (optional) — a Personal Access Token (PAT) that the PR preview workflow can use to delete preview images from GitHub Container Registry after a PR is closed. This token needs the following scopes: `read:packages` and `delete:packages` (and optionally `write:packages` if your workflows require uploading images from the user account). For org-owned repositories you may need `repo` permission depending on your organization policies.
 
 - Optional secret: `GHCR_PAT` — if set, the preview cleanup step will attempt to delete the GHCR package version(s) created for a PR using the GHCR API. Without this, the image tags will remain in the registry and must be manually deleted to reclaim storage.
Render deployment secrets (optional but recommended if you use Render):
- `RENDER_API_KEY` — API key from your Render account (add as a GitHub secret).
- `RENDER_SERVICE_ID` — The Render service ID that will be triggered for deploys.
 - `RENDER_PLAN` — (optional) Render plan for preview services, e.g., `starter`.
 - `RENDER_REGION` — (optional) Render region for preview services, e.g., `oregon`.

How to obtain Render service ID and API key
1. Go to the Render Dashboard → Account → API Keys → Create Key. Save it as a GitHub secret `RENDER_API_KEY`.
2. Go to your Render Service → Settings → General → Service ID (copy it and store as `RENDER_SERVICE_ID`).

This repository also contains a `render-deploy.yml` GitHub Actions workflow that builds the root Docker image, publishes to GHCR, then triggers the Render service to deploy the updated container.

Pull Request preview deployments (Render PR Preview)
- A `render-pr-preview.yml` workflow is included that builds a PR-specific image and creates/updates a Render preview service named `dpro-pr-<PR_NUMBER>`.
- Required secret: `RENDER_API_KEY` and optionally `RENDER_PLAN` and `RENDER_REGION`. The GH Action will create or delete preview services for PRs.
 - After the Render PR preview deploys, the workflow will wait for `/health` to succeed and run a `/api/ping` smoke test.
 - The workflow posts a comment on the PR with the preview URL and the health/ping results. When the PR is closed, the preview service will be deleted and the PR will be updated with a comment.


How to set secrets
1. Go to GitHub repository > Settings > Secrets > Actions.
2. Add `FIREBASE_TOKEN` or `FIREBASE_SERVICE_ACCOUNT` and `FIREBASE_PROJECT_ID`.
3. If you want GitHub Actions to automatically cleanup per-PR GHCR images when PRs are closed, add `GHCR_PAT` as a repository secret. Create a PAT in your GitHub account via: Settings → Developer settings → Personal access tokens → Generate new token, then select `read:packages` and `delete:packages` scopes (optionally `write:packages`), and click Generate token. Save that token as `GHCR_PAT`.

Notes
- The Firebase workflow expects either a `FIREBASE_TOKEN` or a `FIREBASE_SERVICE_ACCOUNT` (base64-encoded) in repository secrets.
- The Build-and-Push workflow will push the image to ghcr.io. If you prefer to publish to Docker Hub, update the workflow accordingly and add `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets.

Recommended GitHub Workflow pipeline (professional):
1. Pull Request: run tests and lint, build non-pushed artifacts, and optionally run ephemeral preview deployments in Render (staging).
2. Merge to `main`: build and push Docker image to GHCR; deploy Flask app to Render via `render-deploy.yml`; deploy Firebase functions & hosting via `firebase-deploy.yml`.
3. Use `GITHUB_ENV` and `Environments` to approve production deploys; require code review/PR approvals before production.

Set up GitHub environment and approvals
1. Go to your repository > Settings > Environments.
2. Create an environment named `production` (used by the workflows in this repo).
3. Under Protection rules, set required reviewers (individuals or teams) to approve production deployments.
4. Add environment-level secrets for production if needed (RENDER_API_KEY, FIREBASE_SERVICE_ACCOUNT, FIREBASE_TOKEN, etc.). Environment secrets can be limited to specific environments and are safer than repo secrets for production.
5. Now, any job that declares `environment: production` will pause and require an approval by the configured reviewers before it continues.

Triggering and approving production deploys (manual approval flow)
1. Merge PR into `main` or push a commit to `main`. That will run the `build_and_push` job automatically.
2. Open the Actions tab and locate the workflow run triggered by the push. The `deploy` job will be suspended because it uses `environment: production`.
3. An authorized reviewer (as defined in the Environment protection rules) must approve the environment deployment from the GitHub UI.
4. After approval, the `deploy` job will continue and perform the Render/Firebase production deployment.
5. The workflow will post deploy status and health summary as comments on the commit/PR.

Why this is important
- This prevents direct pushes from accidentally deploying to production and ensures a human in the loop to validate releases.
- Use this together with PR previews to validate changes prior to production approval.

