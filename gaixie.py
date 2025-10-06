import os
import subprocess
import zipfile
import urllib.request
import plistlib
from pathlib import Path


class DynatraceSymbolManager:
    def __init__(self, client_version: str, signature: str = "Dynatrace Installer", verbose: bool = True):
        self.client_version = client_version
        self.signature = signature
        self.verbose = verbose
        self.base_build_dir = Path(f"build/Dynatrace/{client_version}")

    # ----------------------------
    # Helper methods
    # ----------------------------

    def _log(self, message: str):
        if self.verbose:
            print(message)

    def _run_cmd(self, cmd: str) -> str:
        """Run shell command and return output"""
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
        return result.stdout.strip()

    # ----------------------------
    # Core methods
    # ----------------------------

    def _get_dynatrace_xcode_version(self) -> str:
        """Read DTPlatformBuild from Info.plist"""
        plist_path = self.base_build_dir / "ios" / "agent" / "Dynatrace.framework" / "Info.plist"
        with plist_path.open("rb") as f:
            info = plistlib.load(f)
        return info.get("DTPlatformBuild")

    def _list_all_xcodes(self) -> list[str]:
        """Find all installed Xcodes"""
        cmd = "mdfind 'kMDItemCFBundleIdentifier == com.apple.dt.Xcode'"
        return self._run_cmd(cmd).splitlines()

    def _get_xcode_build_version(self, xcode_path: str) -> str:
        """Get Xcode build version"""
        cmd = f"{xcode_path}/Contents/Developer/usr/bin/xcodebuild -version"
        output = self._run_cmd(cmd)
        for line in output.splitlines():
            if "Build version" in line:
                return line.split()[-1]
        return ""

    # ----------------------------
    # Public functions
    # ----------------------------

    def select_xcode(self) -> str:
        """Find local Xcode matching Dynatrace DTPlatformBuild"""
        dynatrace_xcode = self._get_dynatrace_xcode_version()
        self._log(f"Dynatrace DTPlatformBuild: {dynatrace_xcode}")

        for xcode in self._list_all_xcodes():
            build = self._get_xcode_build_version(xcode)
            self._log(f"Checking {xcode} (Build {build})")
            if build == dynatrace_xcode:
                developer_dir = f"{xcode}/Contents/Developer"
                self._log(f"✅ Found matching Xcode: {xcode}")
                return developer_dir

        self._log("⚠️ No exact Xcode match found.")
        fallback = self._run_cmd("xcode-select -p")
        self._log(f"Using fallback Xcode from xcode-select: {fallback}")
        return fallback

    def _fetch_file(self, url: str, dest: Path):
        """Download file"""
        self._log(f"⬇️  Downloading {url} -> {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest)
        self._log("✅ Download complete.")

    def _unzip_file(self, zip_path: Path, target_dir: Path):
        """Unzip file"""
        self._log(f"📦 Unzipping {zip_path} -> {target_dir}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_dir)
        self._log("✅ Unzip complete.")

    def install_client(self) -> str:
        """Install Dynatrace Symbol Service Client and fix LLDB symlink"""
        client_script = self.base_build_dir / "ios" / "agent" / "Dynatrace.framework" / "Info.plist"

        # Download if missing
        if client_script.exists():
            self._log("✅ Dynatrace symbol service client already installed.")
        else:
            self._log(f"{self.signature}: Installing symbol service client...")
            client_file = Path("SymbolServiceClient.zip")
            client_url = (
                f"https://mobileagent.downloads.dynatrace.com/ios/"
                f"{self.client_version}/dynatrace-mobile-agent-ios-{self.client_version}.zip"
            )
            self._fetch_file(client_url, client_file)
            self._unzip_file(client_file, self.base_build_dir)
            client_file.unlink(missing_ok=True)

        # Match Xcode
        developer_dir = self.select_xcode()

        # Fix LLDB.framework link
        self._log("🔗 Fixing LLDB.framework symlink...")
        lldb_framework = Path(developer_dir.replace("/Developer", "/SharedFrameworks/LLDB.framework"))
        target_softlink = client_script.parent.parent / "LLDB.framework"

        if target_softlink.exists() or target_softlink.is_symlink():
            target_softlink.unlink()

        os.symlink(lldb_framework, target_softlink)
        self._log(f"✅ Linked {lldb_framework} -> {target_softlink}")

        return developer_dir

    # ----------------------------
    # Optional: upload placeholder
    # ----------------------------

    def upload_symbols(self):
        """Placeholder for uploading logic"""
        self._log("📤 Uploading symbols to Dynatrace (TODO: implement)...")


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    manager = DynatraceSymbolManager(client_version="25.04.1")
    dev_dir = manager.install_client()
    print(f"✅ Installation complete. DEVELOPER_DIR: {dev_dir}")