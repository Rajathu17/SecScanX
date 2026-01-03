# Deployment Guide

This document explains how to deploy and automate **SecScanX** completely for **FREE** using GitHub Actions.

## Overview
We will use **GitHub Actions** as our CI/CD runner. It provides a free tier for public repositories (and 2000 free minutes/month for private ones), which is sufficient for weekly or commit-based security scans.

## Deployment Steps

### 1. Push Code to GitHub
Ensure your code is pushed to a GitHub repository.
```bash
git init
git add .
git commit -m "Initial commit of SecScanX"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/SecScanX.git
git push -u origin main
```

### 2. Configure Secrets
To allow the GitHub Action to send notifications to your Slack channel, you must save your Webhook URL as a "Secret". Do **not** commit it to code.

1. Go to your repository on GitHub.
2. Click **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. **Name**: `SLACK_WEBHOOK_URL`
5. **Value**: Paste your Slack Webhook URL (e.g., `https://hooks.slack.com/services/...`).
6. Click **Add secret**.

### 3. Verify the Workflow
The project already includes a workflow file at `.github/workflows/security-scan.yml`. This workflow is configured to:
- Run on every `push` to `main`.
- Run on `pull_request` to `main`.
- **Run regularly on a Schedule** (Weekly on Sundays).

**What happens automatically:**
1. GitHub spins up a standard Ubuntu runner.
2. Checks out your code.
3. Installs **Python 3.9**.
4. Installs **Trivy** (Security Scanner).
5. Installs Python dependencies (`requests`, `docker`).
6. Runs `main.py` using the `SLACK_WEBHOOK_URL` secret.

### 4. Triggering specific Image Scans
By default, the workflow scans a demo image (`python:3.9-alpine`). To scan your own built images, you would modify `.github/workflows/security-scan.yml` to first build your image, then pass that image name to `main.py`.

Example modification for `security-scan.yml`:
```yaml
    - name: Build Docker Image
      run: docker build -t my-app:latest .

    - name: Run Security Scan
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
      run: |
        python main.py my-app:latest --webhook "$SLACK_WEBHOOK_URL"
```

## Running Locally (Docker)
You can also deploy this orchestrator itself as a Docker container, but this requires a machine to run it (like a VPS). Using GitHub Actions (above) is the true "Serverless/Free" approach.

If you ever need to run it inside a Docker container:
```bash
# Build the orchestrator image
docker build -t secscanx .

# Run it (Mounting Docker socket is required to scan other containers!)
docker run -v /var/run/docker.sock:/var/run/docker.sock \
           -e SLACK_WEBHOOK_URL="your_url" \
           secscanx \
           python main.py target-image:latest
```
*Note: Installing Trivy inside the Docker image would be required for this fully self-contained Docker approach.*
