# 🚀 Fabric Workspace Deployer

A production-grade automation framework for deploying Microsoft Fabric workspaces and lakehouses using **GitHub Actions**, **Python**, and **Jinja2 templating**. Designed for **data engineers** and **data architects** to streamline environment provisioning across clients and projects.

---

## 🧠 Architecture Overview

This solution follows a modular and secure architecture:

- **GitHub Actions**: Orchestrates the deployment pipeline triggered manually or on code changes.
- **Python Scripts**:
  - `render_config.py`: Renders workspace configuration from Jinja2 templates and environment variables.
  - `deploy.py`: Authenticates with Microsoft Entra ID and deploys workspaces and lakehouses via Fabric API.
- **Jinja2 Templates**: Dynamically generate `workspace_config.json` from secrets and workspace definitions.
- **GitHub Secrets**: Securely store credentials and deployment parameters.
- **Workspace Definitions**: Stored in `config/workspaces.json` for version control and easy customization.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
git clone https://github.com/your-org/fabric-workspace-deployer.git
cd fabric-workspace-deployer

### 2. Define Secrets in GitHub
Go to Settings → Secrets and variables → Actions and add:

TENANT_ID
CLIENT_ID
CLIENT_SECRET
CAPACITY_ID

### 3. Define Workspace Structure

Create or edit `config/workspaces.json`:


[
  {
    "name": "Data Engineer Dev",
    "lakehouse": "DE_Dev_Lakehouse"
  },
  {
    "name": "Data Engineer Prod",
    "lakehouse": "DE_Prod_Lakehouse"
  },
  {
    "name": "Report Workspace"
  }
]

Usage
Manual Trigger via GitHub Actions

Go to the Actions tab.
Select Deploy Fabric Workspaces workflow.
Click Run workflow.

This will:

Load secrets and workspace definitions.
Render workspace_config.json using Jinja2.
Deploy workspaces and lakehouses via Fabric API.


Customization

Multiple Clients: Create separate workspace definition files (e.g. clientA_workspaces.json) and modify render_config.py to load based on input.
Environment Support: Use matrix strategy in GitHub Actions to deploy to dev, staging, prod.
Logging: Extend deploy.py with logging to file or external monitoring tools.



Best Practices

Use version-controlled workspace definitions for auditability.
Rotate secrets regularly and use GitHub environments for separation.
Validate workspace names to avoid duplicates or naming conflicts.
Modularize Python scripts for easier testing and extension.

Project Structure
fabric-workspace-deployer/
├── .github/
│   └── workflows/
│       └── main.yaml
├── config/
│   └── workspaces.json
├── scripts/
│   ├── deploy.py
│   └── render_config.py
├── templates/
│   └── workspace_config_template.j2
└── README.md


Maintainers
Built by and for data engineers and architects who value automation, reproducibility, and clean infrastructure-as-code practices.


