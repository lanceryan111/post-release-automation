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