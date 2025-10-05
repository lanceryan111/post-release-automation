import subprocess
from pathlib import Path

class DynatraceSymbolPublisher:
    """
    A Python wrapper to call the existing shell script for Dynatrace symbol upload.
    Keeps all shell logic intact but allows structured Python integration.
    """

    def __init__(self, script_path="publish-symbols.sh"):
        self.script_path = Path(script_path).resolve()
        if not self.script_path.exists():
            raise FileNotFoundError(f"Script not found: {self.script_path}")

    def _run_script(self, *args):
        """Internal helper to run the shell script with arguments."""
        cmd = ["bash", str(self.script_path)] + list(args)
        print(f"🟢 Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True)
            print(result.stdout)
            if result.stderr.strip():
                print(f"⚠️ stderr:\n{result.stderr}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Script failed with exit code {e.returncode}")
            print(f"stderr:\n{e.stderr}")
            raise

    def select_xcode(self):
        """Invoke the part of the shell script that selects Xcode."""
        return self._run_script("select_xcode")

    def install(self):
        """Invoke the shell script to download/install Dynatrace tool."""
        return self._run_script("install")

    def upload_symbols(self):
        """Invoke the shell script to upload symbols to Dynatrace."""
        return self._run_script("upload_symbols")

    def run_full_pipeline(self):
        """Example combined workflow."""
        self.select_xcode()
        self.install()
        self.upload_symbols()
        
from dynatrace_symbols import DynatraceSymbolPublisher

if __name__ == "__main__":
    publisher = DynatraceSymbolPublisher("publish-symbols.sh")
    publisher.run_full_pipeline()
    
publisher.select_xcode()
publisher.install()

#!/bin/bash
set -e

COMMAND=$1
APPLICATION_ID=$2
VERSION_ID=$3
CLIENT_VERSION=$4

# Default values (for backward compatibility)
APPLICATION_ID=${APPLICATION_ID:-"default-app-id"}
VERSION_ID=${VERSION_ID:-"1.0.0"}
CLIENT_VERSION=${CLIENT_VERSION:-"8.287.2.1009"}

echo "🔧 Running command: $COMMAND"
echo "📦 Application ID: $APPLICATION_ID"
echo "🧩 Version ID: $VERSION_ID"
echo "🧰 Client Version: $CLIENT_VERSION"

# Example: run only a specific section
case "$COMMAND" in
  select_xcode)
    select_xcode
    ;;
  install)
    install
    ;;
  upload_symbols)
    upload_symbols
    ;;
  all|run_full_pipeline)
    select_xcode
    install
    upload_symbols
    ;;
  *)
    echo "Usage: $0 {select_xcode|install|upload_symbols|all} [application_id] [version_id] [client_version]"
    exit 1
    ;;
esac

import subprocess
from pathlib import Path

class DynatraceSymbolPublisher:
    """
    A Python wrapper to call the existing shell script for Dynatrace symbol upload,
    passing in dynamic parameters like application_id, version_id, and client_version.
    """

    def __init__(self, script_path="publish-symbols.sh"):
        self.script_path = Path(script_path).resolve()
        if not self.script_path.exists():
            raise FileNotFoundError(f"Script not found: {self.script_path}")

    def _run_script(self, command, application_id, version_id, client_version):
        """Internal helper to run the shell script with arguments."""
        cmd = [
            "bash",
            str(self.script_path),
            command,
            application_id,
            version_id,
            client_version
        ]
        print(f"🟢 Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True)
            if result.stdout.strip():
                print(result.stdout)
            if result.stderr.strip():
                print(f"⚠️ stderr:\n{result.stderr}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Script failed with exit code {e.returncode}")
            print(f"stderr:\n{e.stderr}")
            raise

    def select_xcode(self, application_id, version_id, client_version):
        """Call 'select_xcode' section in the shell script."""
        return self._run_script("select_xcode", application_id, version_id, client_version)

    def install(self, application_id, version_id, client_version):
        """Call 'install' section in the shell script."""
        return self._run_script("install", application_id, version_id, client_version)

    def upload_symbols(self, application_id, version_id, client_version):
        """Call 'upload_symbols' section in the shell script."""
        return self._run_script("upload_symbols", application_id, version_id, client_version)

    def run_full_pipeline(self, application_id, version_id, client_version):
        """Run the full sequence in one go."""
        return self._run_script("all", application_id, version_id, client_version)
        
from dynatrace_symbols import DynatraceSymbolPublisher

publisher = DynatraceSymbolPublisher("publish-symbols.sh")

# 示例：传参数进入 shell
publisher.run_full_pipeline(
    application_id="eab451f3-5208-4c52-b06a-df09f86c2cb3",
    version_id="8.287.2.1009",
    client_version="8.287.2.1009"
)