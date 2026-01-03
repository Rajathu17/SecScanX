import subprocess
import json
import logging
import shutil

logger = logging.getLogger(__name__)

class TrivyScanner:
    def __init__(self, trivy_path="trivy"):
        self.trivy_path = trivy_path
        if not shutil.which(self.trivy_path):
            raise FileNotFoundError(f"Trivy executable not found at '{self.trivy_path}'. Please ensure it is installed and in your PATH.")

    def scan_image(self, image_name):
        """
        Runs trivy image scan and returns the JSON result.
        """
        logger.info(f"Starting scan for image: {image_name}")
        cmd = [
            self.trivy_path, "image",
            "--format", "json",
            "--quiet", # Suppress progress bar
            "--scanners", "vuln", # Only scan for vulnerabilities for now
            image_name
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("Scan completed successfully.")
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Trivy scan failed: {e.stderr}")
            raise RuntimeError(f"Trivy scan failed with exit code {e.returncode}: {e.stderr}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Trivy output: {e}")
            raise RuntimeError("Failed to parse Trivy JSON output.")

    def parse_results(self, scan_data: dict) -> dict:
        """
        Parses Trivy JSON output and aggregates vulnerability counts by severity.
        Returns a dict like: {'CRITICAL': 0, 'HIGH': 2, 'MEDIUM': 5, 'LOW': 1, 'UNKNOWN': 0}
        """
        summary = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "UNKNOWN": 0
        }

        if "Results" not in scan_data:
            logger.warning("No results found in Trivy scan output.")
            return summary

        for result in scan_data["Results"]:
            if "Vulnerabilities" in result:
                for vuln in result["Vulnerabilities"]:
                    severity = vuln.get("Severity", "UNKNOWN").upper()
                    if severity in summary:
                        summary[severity] += 1
                    else:
                        summary["UNKNOWN"] += 1
        
        return summary
