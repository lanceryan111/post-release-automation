import subprocess
import json
from pathlib import Path

class DynatraceFastlaneUploader:
    """
    Wrapper class for the fastlane-plugin-dynatrace.
    Handles preprocessing and uploading of dSYM/symbol files to Dynatrace.
    """

    def __init__(self, fastlane_path="fastlane", project_dir="."):
        self.fastlane_path = fastlane_path
        self.project_dir = Path(project_dir).resolve()

    def process_symbols(
        self,
        app_id: str,
        api_token: str,
        dtx_client_path: str,
        symbol_file: str,
        bundle_name: str,
        version_str: str,
        version: str,
        os_type: str = "ios",
        server_url: str = "https://dynatrace-managed.com/e/your-environment-id",
        debug_mode: bool = True
    ):
        """
        Run Fastlane dynatrace_process_symbols with all parameters.

        Args:
            app_id: Dynatrace application ID
            api_token: Dynatrace API token
            dtx_client_path: Path to DTXDssClient binary
            symbol_file: Path to .app.dSYM or .zip file
            bundle_name: iOS bundle name (e.g., "com.company.myapp")
            version_str: App version string (e.g., "1.0.0")
            version: App build version (e.g., "100")
            os_type: 'ios' or 'android'
            server_url: Dynatrace server endpoint
            debug_mode: Enable detailed output
        """

        params = {
            "dtxDssClientPath": dtx_client_path,
            "appId": app_id,
            "apitoken": api_token,
            "os": os_type,
            "bundleName": bundle_name,
            "versionStr": version_str,
            "version": version,
            "symbolIsFile": symbol_file,
            "server": server_url,
            "debugMode": str(debug_mode).lower()
        }

        print("🟢 Running fastlane dynatrace_process_symbols...")
        print(json.dumps(params, indent=2))

        # Construct Fastlane command
        cmd = [
            self.fastlane_path,
            "run",
            "dynatrace_process_symbols"
        ] + [f"{k}:{v}" for k, v in params.items()]

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_dir,
                text=True,
                capture_output=True,
                check=True
            )
            print("✅ Fastlane completed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("❌ Fastlane failed:")
            print(e.stderr)
            raise