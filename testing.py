import subprocess
import json


def git_leaks_scan(repo_path="."):
    try:
        command = [
            "gitleaks",
            "detect",
            "--source", ".",
            "--no-git",
            "--report-format", "json",
            "--report-path", "gitleaks-report.json",
            "--no-banner",
        ]

        result = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=repo_path,
        )

        stdout, stderr = result.communicate()

        if result.returncode == 0:
            print("Scan completed. No leaks found.")

        elif result.returncode == 1:
            print("Scan completed. Leaks found.")

        else:
            print("Gitleaks execution failed.")
            print(stderr)
            return None

        report_path = f"{repo_path}/gitleaks-report.json"

        with open(report_path, "r", encoding="utf-8") as file:
            report = json.load(file)

        print(f"Report saved to: {report_path}")

        for finding in report:
            print(f"File: {finding.get('File', 'N/A')}")
            print(f"Rule: {finding.get('RuleID', 'N/A')}")
            print(f"Line: {finding.get('StartLine', 'N/A')}")
            print(f"Commit: {finding.get('Commit', 'N/A')}")

            # Don't print the actual secret in a real security scanner.
            # print(f"Secret found: {finding.get('Secret', 'N/A')}")

        return report

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    report = git_leaks_scan(".")