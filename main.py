import argparse
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scanner import TrivyScanner
from app.notifier import SlackNotifier
from app import docker_ops

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="SecScanX Orchestrator")
    parser.add_argument("image", help="Docker image name to scan (e.g., python:3.9-alpine)")
    parser.add_argument("--webhook", help="Slack Incoming Webhook URL", required=False)
    parser.add_argument("--cleanup", action="store_true", help="Remove image after scan")
    
    args = parser.parse_args()

    # Get Webhook from arg or env var
    webhook_url = args.webhook or os.environ.get("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.error("Slack Webhook URL is required. Provide it via --webhook argument or SLACK_WEBHOOK_URL environment variable.")
        sys.exit(1)

    try:
        # 1. Pull Image via Docker SDK
        docker_ops.pull_image(args.image)

        # 2. Scan using Trivy
        # Note: Assumes 'trivy' is installed (or inside the container if running via Docker)
        scanner = TrivyScanner()
        scan_data = scanner.scan_image(args.image)
        
        # 3. Parse Results
        summary = scanner.parse_results(scan_data)
        logger.info(f"Scan Summary for {args.image}: {summary}")

        # 4. Notify Slack
        notifier = SlackNotifier(webhook_url)
        notifier.send_report(args.image, summary)

        # 5. Cleanup (Optional)
        if args.cleanup:
            docker_ops.cleanup_image(args.image)

        # 6. Exit with Failure if Critical/High found (for CI/CD gating)
        if summary.get("CRITICAL", 0) > 0 or summary.get("HIGH", 0) > 0:
            logger.error("Security Gate Failed: Critical/High vulnerabilities detected.")
            sys.exit(1)
        
        logger.info("Security Scan Passed.")

    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
