import argparse
import logging
import sys
import os

# Ensure the app directory is in path (if running directly from root)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scanner import TrivyScanner
from app.parser import VulnerabilityParser
from app.slack import SlackNotifier

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="SecureScan-Orchestrator: Trivy wrapper with Slack notifications.")
    parser.add_argument("image", help="Docker image name to scan (e.g., alpine:latest)")
    parser.add_argument("--webhook", help="Slack Incoming Webhook URL", required=False)
    
    args = parser.parse_args()

    # Get Webhook from arg or env var
    webhook_url = args.webhook or os.environ.get("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.error("Slack Webhook URL is required. Provide it via --webhook argument or SLACK_WEBHOOK_URL environment variable.")
        sys.exit(1)

    try:
        # 1. Scan
        scanner = TrivyScanner()
        scan_results = scanner.scan_image(args.image)

        # 2. Parse
        parser_logic = VulnerabilityParser()
        summary = parser_logic.parse_results(scan_results)
        
        # Log summary to console
        logger.info(f"Scan Summary for {args.image}: {summary}")

        # 3. Notify
        notifier = SlackNotifier(webhook_url)
        notifier.send_summary(args.image, summary)

    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
