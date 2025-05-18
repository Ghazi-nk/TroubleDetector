import os
import subprocess

PROJECT_DIR = "../project"
REPORTS_DIR = "./reports"
REPORT_FILE_NAME = "report.json"

def scan_with_semgrep(repo_path, report_output_path):
    print(f"🔍 Running Semgrep on: {repo_path}")
    print(f"📝 Output path: {report_output_path}")

    os.makedirs(os.path.dirname(report_output_path), exist_ok=True)

    result = subprocess.run([
        "semgrep",
        "--config", "auto",
        "--json",
        repo_path
    ], capture_output=True, text=True)

    if result.returncode == 0:
        with open(report_output_path, "w") as f:
            f.write(result.stdout)
        print(f"✅ Report saved: {report_output_path}")
    else:
        print(f"❌ Semgrep error. Return code: {result.returncode}")
        print(f"STDERR:\n{result.stderr}")


def main():
    if not os.path.exists(PROJECT_DIR):
        print("❗ No project folder found.")
        return

    for item in os.listdir(PROJECT_DIR):
        repo_path = os.path.join(PROJECT_DIR, item)
        if os.path.isdir(repo_path):
            report_output_path = os.path.join(REPORTS_DIR, f"{item}_{REPORT_FILE_NAME}")
            scan_with_semgrep(repo_path, report_output_path)

if __name__ == "__main__":
    main()
