import json
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

PROJECT_DIR = "project"
REPORTS_DIR = "reports"
REPORT_FILE = "report.json"
OUTPUT_PATH = os.path.join(REPORTS_DIR, REPORT_FILE)
SEMGREP_TOKEN = os.getenv("SEMGREP_APP_TOKEN")

load_dotenv()  # Load environment variables from .env file
def run_semgrep_scan(target_dir: str, output_path: str, semgrep_token: str = None):
    # Build the Semgrep command
    semgrep_cmd = [
    "semgrep", "scan",
    "--config", "auto",
    "--json",
    "--output", "reports/report.json"
]

    # Set environment variables
    env = os.environ.copy()

    try:
        subprocess.run(semgrep_cmd, cwd=target_dir, check=True, env=env)
        print(f"✅ Semgrep scan completed. Report saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print("❌ Semgrep scan failed:")
        print(e)

def get_semgrep_report():
    run_semgrep_scan(PROJECT_DIR, OUTPUT_PATH, SEMGREP_TOKEN)
    report_path = Path("reports/report.json")
    if not report_path.exists():
        raise FileNotFoundError(f"Report file not found: {report_path}")

    with report_path.open("r", encoding="utf-8") as f:
        report_json = json.load(f)
    return json.dumps(report_json, indent=2)

if __name__ == "__main__":
    run_semgrep_scan(PROJECT_DIR, OUTPUT_PATH, SEMGREP_TOKEN)
