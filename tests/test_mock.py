import unittest
from unittest.mock import MagicMock, patch
import json
import sys
import os

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.scanner import TrivyScanner
from app.parser import VulnerabilityParser
from app.slack import SlackNotifier

class TestSecureScan(unittest.TestCase):

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_scanner_success(self, mock_run, mock_which):
        # Mock trivy existing
        mock_which.return_value = "/usr/bin/trivy"
        
        # Mock subprocess output
        mock_output = {
            "Results": [{
                "Vulnerabilities": [
                    {"Severity": "CRITICAL"},
                    {"Severity": "HIGH"},
                    {"Severity": "LOW"}
                ]
            }]
        }
        mock_run.return_value = MagicMock(stdout=json.dumps(mock_output), returncode=0)

        scanner = TrivyScanner()
        result = scanner.scan_image("test-image")
        
        self.assertEqual(result, mock_output)
        mock_run.assert_called_once()

    def test_parser_logic(self):
        sample_data = {
            "Results": [{
                "Vulnerabilities": [
                    {"Severity": "CRITICAL"},
                    {"Severity": "CRITICAL"},
                    {"Severity": "MEDIUM"}
                ]
            }]
        }
        summary = VulnerabilityParser.parse_results(sample_data)
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["critical"], 2)
        self.assertEqual(summary["medium"], 1)
        self.assertEqual(summary["high"], 0)

    @patch('requests.post')
    def test_slack_notification(self, mock_post):
        mock_post.return_value.status_code = 200
        
        notifier = SlackNotifier("http://fake-webhook")
        summary = {"total": 5, "critical": 1, "high": 2, "medium": 1, "low": 1, "unknown": 0}
        
        notifier.send_summary("test-image", summary)
        
        mock_post.assert_called_once()
        # Verify payload structure roughly
        args, kwargs = mock_post.call_args
        self.assertIn("blocks", kwargs['json']['attachments'][0])
        self.assertIn("Critical", str(kwargs['json']))

if __name__ == '__main__':
    unittest.main()
