# SecScanX

A robust, Python-based orchestrator for automated container security scanning. It integrates Docker image management, Trivy vulnerability scanning, and Slack notifications into a streamlined workflow suitable for CI/CD pipelines.

## Features

- **Automated Scanning**: Pulls and scans Docker images using Trivy.
- **Smart Parsing**: Aggregates vulnerabilities by severity (Critical, High, Medium, Low).
- **Slack Integration**: Sends color-coded, rich summaries to your Slack channel.
- **CI/CD Ready**: Includes configurations for GitHub Actions and GitLab CI.
- **Security Gates**: Fails the pipeline if Critical or High vulnerabilities are detected.

## Prerequisites

- **Python 3.9+**
- **Docker Engine** (running and accessible)
- **Trivy** (installed and in PATH)
- **Slack Webhook URL** (for notifications)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rajathu17/SecScanX.git
   cd SecScanX
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Scan
Run the orchestrator by providing the image name and your Slack Webhook URL.

```bash
# Using command line argument
python main.py python:3.9-alpine --webhook "https://hooks.slack.com/services/..."

# Using environment variable
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python main.py python:3.9-alpine
```

### Options

| Argument | Description |
|----------|-------------|
| `image` | The Docker image to scan (required). |
| `--webhook` | Slack Incoming Webhook URL. |
| `--cleanup` | Remove the image from the local Docker daemon after scanning. |

### Example Output

Console:
```text
INFO - Pulling image: python:3.9-alpine...
INFO - Successfully pulled image: python:3.9-alpine
INFO - Starting scan for image: python:3.9-alpine
INFO - Scan completed successfully.
INFO - Scan Summary for python:3.9-alpine: {'CRITICAL': 0, 'HIGH': 2, 'MEDIUM': 5, 'LOW': 1, 'UNKNOWN': 0}
INFO - Sending scan report for python:3.9-alpine to Slack...
INFO - Slack notification sent successfully.
ERROR - Security Gate Failed: Critical/High vulnerabilities detected.
```

Slack Notification:
- **Red** if Critical issues found.
- **Orange** if High issues found.
- **Green** if clean.

## CI/CD Integration

### GitHub Actions
A workflow is provided in `.github/workflows/security-scan.yml`. 
1. Add `SLACK_WEBHOOK_URL` to your repository secrets.
2. The workflow runs on push to main or pull requests.

### GitLab CI
Configuration provided in `.gitlab-ci.yml`.
1. Add `SLACK_WEBHOOK_URL` to your CI/CD variables.
2. Ensure your runner has Docker-in-Docker (dind) enabled.

## Project Structure

- `app/main.py`: Entry point for the orchestrator.
- `app/docker_ops.py`: Docker image management.
- `app/scanner.py`: Trivy wrapper and result parsing.
- `app/notifier.py`: Slack notification logic.
