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

## Usage

Manual Trigger via GitHub Actions

To manually deploy Fabric workspaces:

1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Deploy Fabric Workspaces** workflow.
3. Click **Run workflow**.

### This will:

- Load secrets and workspace definitions.
- Render `workspace_config.json` using Jinja2.
- Deploy workspaces and lakehouses via the Fabric API.

---

## Customization

- **Multiple Clients**  
  Create separate workspace definition files (e.g. `clientA_workspaces.json`) and modify `render_config.py` to load based on input.

- **Environment Support**  
  Use a matrix strategy in GitHub Actions to deploy to `dev`, `staging`, and `prod`.

- **Logging**  
  Extend `deploy.py` with logging to a file or external monitoring tools.

---

## Best Practices

- Use version-controlled workspace definitions for auditability.
- Rotate secrets regularly and use GitHub environments for separation.
- Validate workspace names to avoid duplicates or naming conflicts.
- Modularize Python scripts for easier testing and extension.

---


## Project Structure
The repository is organized as follows:


graph TD
  A[fabric-workspace-deployer/]
  A --> B[.github/]
  B --> B1[workflows/]
  B1 --> B2[main.yaml<br>GitHub Actions workflow definition]

  A --> C[config/]
  C --> C1[workspaces.json<br>Workspace definitions]

  A --> D[scripts/]
  D --> D1[deploy.py<br>Deployment logic]
  D --> D2[render_config.py<br>Jinja2 rendering logic]

  A --> E[templates/]
  E --> E1[workspace_config_template.j2<br>Jinja2 template]

  A --> F[README.md<br>Project documentation]



---

## Maintainers

Built by and for data engineers and architects who value automation, reproducibility, and clean infrastructure-as-code practices.




