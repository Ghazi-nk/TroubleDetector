import json
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Default constants
PROJECT_DIR = "project"
REPORTS_DIR = "reports"
REPORT_FILE = "report.json"
OUTPUT_PATH = Path(REPORTS_DIR) / REPORT_FILE

load_dotenv()  # Load environment variables from .env file
SEMGREP_TOKEN = os.getenv("SEMGREP_APP_TOKEN")

def run_semgrep_scan(
    target_dir: str = PROJECT_DIR,
    output_path: Path = OUTPUT_PATH,
):
    semgrep_cmd = [
        "semgrep", "scan",
        "--config", "auto",
        "--json",
        "--output", str(output_path.resolve())
    ]

    # Set environment variables (including token if needed later)
    env = os.environ.copy()

    try:
        subprocess.run(semgrep_cmd, cwd=target_dir, check=True, env=env)
        print(f"✅ Semgrep scan completed. Report saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print("❌ Semgrep scan failed:")
        print(e)

def get_semgrep_report(output_path: Path=OUTPUT_PATH):
    if not output_path.exists():
        raise FileNotFoundError(f"Report file not found: {output_path}")

    with output_path.open("r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise ValueError(f"Report file {output_path} is empty!")
        report_json = json.loads(content)

    if "results" not in report_json:
        raise ValueError("No 'results' key found in Semgrep report.")

    summary = []
    for result in report_json["results"]:
        summary.append({
            "check_id": result.get("check_id"),
            "message": result.get("extra", {}).get("message"),
            "severity": result.get("extra", {}).get("severity"),
            "path": result.get("path"),
            "line": result.get("start", {}).get("line"),
            "cwe": result.get("extra", {}).get("metadata", {}).get("cwe", []),
            "owasp": result.get("extra", {}).get("metadata", {}).get("owasp", [])
        })

    return json.dumps(summary, indent=2)

if __name__ == "__main__":
    run_semgrep_scan()
