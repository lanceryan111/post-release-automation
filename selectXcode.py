import subprocess
import plistlib
import os
import re

def select_xcode(client_version: str) -> str:
    """
    Try to find the local Xcode that matches the build version used by Dynatrace.

    Args:
        client_version (str): Dynatrace client version (e.g., '8.287.2.1009')

    Returns:
        str: Path to the matching Xcode's Developer directory, or None if not found.
    """

    # Step 1: Get Dynatrace Xcode build version from Info.plist
    info_plist_path = f"build/Dynatrace/{client_version}/ios/agent/Dynatrace.framework/Info.plist"
    try:
        with open(info_plist_path, "rb") as f:
            plist_data = plistlib.load(f)
            dynatrace_xcode = plist_data.get("DTPlatformBuild", None)
    except Exception as e:
        print(f"❌ Failed to read Info.plist: {e}")
        return None

    if not dynatrace_xcode:
        print("❌ DTPlatformBuild not found in Info.plist.")
        return None

    print(f"✅ Dynatrace built with Xcode build version: {dynatrace_xcode}")

    # Step 2: Find all Xcode installations
    try:
        result = subprocess.run(
            ["mdfind", "kMDItemCFBundleIdentifier=com.apple.dt.Xcode"],
            capture_output=True,
            text=True,
            check=True
        )
        all_xcodes = result.stdout.strip().splitlines()
    except subprocess.CalledProcessError:
        print("❌ Failed to find Xcode installations via mdfind.")
        return None

    # Step 3: Compare each Xcode build version
    for xcode in all_xcodes:
        xcodebuild_path = os.path.join(xcode, "Contents/Developer/usr/bin/xcodebuild")

        if not os.path.exists(xcodebuild_path):
            continue

        try:
            version_output = subprocess.run(
                [xcodebuild_path, "-version"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            match = re.search(r"Build version ([A-Za-z0-9]+)", version_output)
            if match:
                xcode_build = match.group(1)
                print(f"🔍 Checking {xcode} (Build {xcode_build})")

                if xcode_build == dynatrace_xcode:
                    developer_dir = os.path.join(xcode, "Contents/Developer")
                    print(f"✅ Found exact Xcode match: {developer_dir}")
                    return developer_dir

        except subprocess.CalledProcessError:
            continue

    # Step 4: If no match found
    print(f"⚠️ No exact match of Xcode found for Dynatrace build {dynatrace_xcode}.")
    print("ℹ️ Try choosing a local Xcode that matches the ABI of Dynatrace:")
    print("   https://xcodereleases.com/")

    # fallback to xcode-select -p
    try:
        default_dir = subprocess.run(["xcode-select", "-p"], capture_output=True, text=True, check=True).stdout.strip()
        print(f"Using current default Xcode at {default_dir}")
        return default_dir
    except subprocess.CalledProcessError:
        print("❌ Failed to get current Xcode via xcode-select.")
        return None