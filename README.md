# SecureScan-Orchestrator

A Python-based automation tool designed to perform security vulnerability scanning on Docker container images using Trivy, and report results to Slack.

## Features
- **Automated Scanning**: Wraps Trivy to scan Docker images.
- **Vulnerability parsing**: Aggregates results by severity (Critical, High, Medium, Low).
- **Slack Notifications**: Sends a color-coded summary to a Slack channel.
- **CI/CD Ready**: Designed to be integrated into CI pipelines.

## Prerequisites
- Python 3.9+
- [Trivy](https://aquasecurity.github.io/trivy/v0.18.3/installation/) installed and in PATH.
- A Slack account and [Incoming Webhook URL](https://api.slack.com/messaging/webhooks).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Rajathu17/SecScanX.git
   cd SecScanX
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run Locally

```bash
# Set your Slack Webhook URL
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Run the scanner
python main.py <image_name>
```

Example:
```bash
python main.py python:3.9-alpine
```

### Docker Usage

Build the image:
```bash
docker build -t secscanx .
```

Run the container (Docker-in-Docker or mounting socket might be needed if scanning local images, but for public images just run):
```bash
docker run --rm -e SLACK_WEBHOOK_URL="your_webhook_url" secscanx python:3.9-alpine
```

## Configuration
- `SLACK_WEBHOOK_URL`: Environment variable for the Slack Webhook. Alternatively, pass via `--webhook` argument.
