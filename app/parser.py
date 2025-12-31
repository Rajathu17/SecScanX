import logging

logger = logging.getLogger(__name__)

class VulnerabilityParser:
    @staticmethod
    def parse_results(scan_results):
        """
        Parses the raw JSON output from Trivy and aggregates vulnerability counts.
        """
        summary = {
            "image": "", # To be filled if available in metadata, or passed separately
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "unknown": 0
        }

        if not scan_results or "Results" not in scan_results:
            logger.warning("No results found in scan data.")
            return summary

        # Trivy can return multiple targets (e.g. OS packages, language dependencies)
        for result in scan_results.get("Results", []):
            if "Vulnerabilities" in result:
                for vuln in result["Vulnerabilities"]:
                    severity = vuln.get("Severity", "UNKNOWN").upper()
                    summary["total"] += 1
                    
                    if severity == "CRITICAL":
                        summary["critical"] += 1
                    elif severity == "HIGH":
                        summary["high"] += 1
                    elif severity == "MEDIUM":
                        summary["medium"] += 1
                    elif severity == "LOW":
                        summary["low"] += 1
                    else:
                        summary["unknown"] += 1
        
        return summary
