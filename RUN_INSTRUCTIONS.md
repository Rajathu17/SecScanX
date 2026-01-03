# How to Run SecScanX

This guide provides step-by-step instructions to set up and run the **SecScanX** orchestrator locally.

## Prerequisites

Ensure you have the following installed on your system:
1.  **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
2.  **Docker Engine**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) (Must be running)
3.  **Trivy**: [Installation Guide](https://aquasecurity.github.io/trivy/v0.18.3/installation/)
    - **Windows (Chocolatey)**: `choco install trivy`
    - **Mac (Homebrew)**: `brew install aquasecurity/trivy/trivy`
    - **Linux**: See the official guide.

## Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Rajathu17/SecScanX.git
    cd SecScanX
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Orchestrator

The orchestrator requires a **Docker image name** to scan. You can optionally provide a **Slack Webhook URL** for notifications.

### 1. Basic Scan (No Notification)
If you don't have a Slack Webhook yet, the script will error if not provided, but you can see the help:
```bash
python main.py --help
```
*Note: The current implementation enforces a Slack Webhook. See section below to set it up.*

### 2. Full Scan with Slack Notification

**Option A: Using Command Line Argument**
```bash
python main.py python:3.9-alpine --webhook "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Option B: Using Environment Variable**
```bash
# Windows (PowerShell)
$env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
python main.py python:3.9-alpine

# Mac/Linux
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
python main.py python:3.9-alpine
```

### 3. Automatic Cleanup
To remove the pulled Docker image from your local system after the scan completes, use the `--cleanup` flag:
```bash
python main.py nginx:latest --webhook "..." --cleanup
```

## Troubleshooting

- **Docker not found?** Ensure Docker Desktop is running.
- **Trivy not found?** Ensure `trivy` is in your system PATH. Test by running `trivy --version` in your terminal.
- **Slack Error?** Verify your Webhook URL is correct and active.
