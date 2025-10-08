h1. Nexus3 Promote and Cleanup Automation

h2. Background & Objective
In the CH08 Post Release process, manual management of Nexus3 artifacts — including promoting releases from the staging repository and cleaning up outdated versions — was time-consuming and error-prone.  

To improve efficiency and ensure consistency across releases, this automation was developed to:
* Simplify the promotion of artifacts from *staging* to *release* repositories.  
* Automatically clean up unused or obsolete artifacts.  
* Enable combined execution of promotion and cleanup operations in a single workflow run.

----

h2. Overview
This automation streamlines the process of *publishing* and *cleaning up* Nexus3 Release artifacts.  
It supports both individual and combined operations for artifact promotion and cleanup in a single execution.

----

h2. Architecture & Workflow

h3. High-Level Design
The automation is implemented as a *GitHub Actions* workflow that interacts with *Nexus3 REST APIs*.  
The process can be triggered manually via *workflow_dispatch* or integrated into a CI/CD pipeline.

Below is a high-level representation of the automation flow:

{code:none|title=Workflow Diagram (Text Version)}
+-----------------------+
|  Developer / CI Job   |
|  (triggers workflow)  |
+----------+------------+
           |
           v
+-----------------------+
|  GitHub Actions       |
|  (Python-based logic) |
+----------+------------+
           |
           v
+-----------------------+
|  Nexus3 REST API      |
|  - Promote artifact   |
|  - Cleanup old builds |
+----------+------------+
           |
           v
+-----------------------+
|  Logs & Status Output |
|  (to GitHub console)  |
+-----------------------+
{code}

h3. Workflow Behavior
* *Promote Action*: Moves a specified artifact from the staging repository to the release repository.
* *Cleanup Action*: Deletes outdated or unused versions from the staging repository.
* *Promote & Cleanup Combined*: Executes both actions sequentially in one run.

----

h2. Key Features
* *Artifact Promotion* — Promotes artifacts from the *staging* repository to the *release* repository in Nexus3.
* *Cleanup of Old Artifacts* — Cleans up outdated or unused artifacts from the staging repository.
* *Combined Execution Support* — Allows promoting and cleaning up artifacts within the same workflow execution.

----

h2. Prerequisites
To use this automation, ensure the following requirements are met:

# *Access*  
  - Valid credentials with appropriate permissions to Nexus3.
# *Environment Setup*  
  - Python installed (≥ 3.8 recommended)
  - Required Python packages:
  {code:bash|title=Install requirements}
  pip install -r requirements.txt
  {code}
  Required libraries include:
  * requests
  * argparse
  * sys

----

h2. Usage

h3. Triggering the Workflow
You can manually trigger the workflow using the *workflow_dispatch* event.  
Provide the required inputs as described below.

----

h2. Workflow Inputs

|| *Input Name* || *Description* || *Required* || *Default Value* || *Options* ||
| action | Action to perform (promote, cleanup, or promote&cleanup) | Yes | None | promote, cleanup, promote&cleanup |
| groupID | Nexus3 Group ID of the target artifact | Yes | None | N/A |
| versionID | Nexus3 Version ID of the target artifact | Yes | None | N/A |

----

h3. Example Usage
{code:yaml|title=GitHub Workflow Example}
on:
  workflow_dispatch:
    inputs:
      action:
        description: 'Action to perform'
        required: true
        default: 'promote'
        options:
          - promote
          - cleanup
          - promote&cleanup
      groupID:
        description: 'Nexus3 Group ID'
        required: true
      versionID:
        description: 'Nexus3 Version ID'
        required: true
{code}

----

h2. Output
* Confirmation logs indicating the success or failure of promotion and cleanup actions.
* Error messages with detailed API responses from Nexus3 for troubleshooting.

----

h2. Maintenance & Ownership
* *Repository:* CH08 Post Release Automation  
* *Maintainers:* [Your Team / Owner Name]  
* *Dependencies:* Nexus3 Repository Manager, GitHub Actions