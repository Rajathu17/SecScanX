import requests
import logging
import json
from typing import Dict

logger = logging.getLogger(__name__)

class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        if not self.webhook_url:
            raise ValueError("Slack Webhook URL is required.")

    def send_report(self, image_name: str, scan_summary: Dict[str, int]):
        """
        Sends a formatted summary to Slack.
        """
        logger.info(f"Sending scan report for {image_name} to Slack...")
        
        # Determine color based on severity
        color = "#36a64f" # Green
        if scan_summary.get("CRITICAL", 0) > 0:
            color = "#ff0000" # Red
            status_text = "FAILED: Critical Vulnerabilities Found"
        elif scan_summary.get("HIGH", 0) > 0:
            color = "#ff9900" # Orange
            status_text = "WARNING: High Severity Vulnerabilities Found"
        else:
            status_text = "PASSED: No High/Critical Vulnerabilities"

        # Build payload
        payload = {
            "text": f"Security Scan Report: {image_name}",
            "attachments": [
                {
                    "color": color,
                    "title": f"Scan Results: {image_name}",
                    "text": status_text,
                    "fields": [
                        {
                            "title": "Critical",
                            "value": str(scan_summary.get("CRITICAL", 0)),
                            "short": True
                        },
                        {
                            "title": "High",
                            "value": str(scan_summary.get("HIGH", 0)),
                            "short": True
                        },
                        {
                            "title": "Medium",
                            "value": str(scan_summary.get("MEDIUM", 0)),
                            "short": True
                        },
                        {
                            "title": "Low",
                            "value": str(scan_summary.get("LOW", 0)),
                            "short": True
                        }
                    ],
                    "footer": "SecScanX Orchestrator",
                    "footer_icon": "https://img.icons8.com/color/48/000000/security-checked--v1.png"
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            logger.info("Slack notification sent successfully.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Slack notification: {e}")
            raise RuntimeError("Failed to send report to Slack.") from e
