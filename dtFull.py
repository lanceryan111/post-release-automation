h1. Dynatrace Symbol & Mapping File Uploader — CH08 Post Release

h2. Background & Objective
In the CH08 Post Release process, iOS and Android build artifacts (symbol and mapping files) must be uploaded to Dynatrace for crash analysis and performance tracking.  
This automation eliminates the manual upload process and ensures consistency across environments.

*Objectives:*
* Automate symbol and mapping file upload to Dynatrace.
* Ensure environment-specific routing (dev, pat, prod).
* Reduce manual intervention and improve traceability.

----

h2. Overview
This feature automates the process of uploading iOS symbol files and Android mapping files from Nexus3 to Dynatrace.  
It supports both iOS and Android platforms and integrates directly with the CH08 GitHub Actions workflow.

----

h2. Key Features
* Fetches metadata JSON from Nexus3.  
* Downloads artifacts (symbol or mapping files) from Nexus3.  
* Pre-processes iOS symbol files before upload.  
* Supports both Android and iOS builds.  
* Dynamically determines Dynatrace environment URL.  
* Uploads files using Dynatrace REST API.

----

h2. Prerequisites
# Python ≥ 3.8 installed.
# Required Python packages:
  {code:bash|title=Install Requirements}
  pip install -r requirements.txt
  {code}
  Includes:
  * requests
  * argparse
  * json
  * os
  * subprocess
  * sys
# Access to Nexus3 credentials and Dynatrace API tokens.

----

h2. Usage

h3. Triggering the Job
The upload job runs automatically as part of the CH08 GitHub Actions workflow.  
It can also be triggered manually with the required input parameters.

----

h2. Workflow Inputs

|| *Input Name* || *Description* || *Required* ||
| token | Dynatrace API Token | Yes |
| group-id | Release Artifact Group ID | Yes |
| artifact-id | Release Artifact Artifact ID | Yes |
| version-id | Release Artifact Version ID | Yes |
| nexus-username | Nexus Username | Yes |

----

h2. How It Works

# *Fetch Metadata:* Downloads the `metadata.json` file from Nexus3.  
# *Parse Metadata:* Extracts required fields like `application_id`, `version_code`, `os`, etc.  
# *Fetch Artifact:* Downloads the artifact (symbol or mapping file) from Nexus3.  
# *Upload File:*  
   * iOS → Calls `dynatrace-publish.sh` to pre-process and upload symbol files.  
   * Android → Directly uploads mapping files via Dynatrace API.

----

h2. Script Structure

h3. Classes
# *ProcessMetadata*  
   - Fetches and parses metadata from Nexus3.  
   - Validates required fields.  
# *MappingUploader*  
   - Handles uploading Android mapping files to Dynatrace.  
# *SymbolUploader*  
   - Calls `dynatrace-publish.sh` to pre-process and upload iOS symbol files.

h3. Functions
*main()* — Orchestrates the full execution flow based on provided inputs.

----

h2. Environment-Specific Dynatrace URL
Dynatrace environment URLs are dynamically selected based on the `env` value found in the metadata or input argument.

|| *Environment* || *Dynatrace URL* ||
| dev | https://dev-td-az.live.dynatrace.com |
| pat | https://pat-td-az.live.dynatrace.com |
| prod | https://prod-td-az.live.dynatrace.com |

----

h2. Error Handling
* Validates metadata fields before upload.  
* Ensures API token validity and handles request errors.  
* Logs and surfaces any failure messages for troubleshooting.

----

h2. Architecture & Workflow
{code:none|title=High-Level Workflow (Text Version)}
+-----------------------+
|  GitHub Actions Job   |
|  (Triggered by CI/CD) |
+----------+------------+
           |
           v
+-----------------------+
|  Python Script        |
|  (dynatrace-upload.py)|
+----------+------------+
           |
           v
+-----------------------+
|  Nexus3 Repository    |
|  - Fetch metadata     |
|  - Download artifact  |
+----------+------------+
           |
           v
+-----------------------+
|  Dynatrace API        |
|  - Upload symbol/mapping files |
|  - Environment routing |
+----------+------------+
           |
           v
+-----------------------+
|  Logs & Validation    |
|  (GitHub Console)     |
+-----------------------+
{code}

----

h2. Maintenance & Ownership
* *Repository:* CH08 Post Release Automation  
* *Maintainers:* [Your Team / Owner Name]  
* *Dependencies:* Nexus3, Dynatrace API, GitHub Actions