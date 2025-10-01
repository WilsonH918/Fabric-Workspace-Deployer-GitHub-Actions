# 🚀 Fabric Workspace Deployer

A production-grade automation framework for deploying Microsoft Fabric workspaces and lakehouses using **GitHub Actions**, **Python**, and **Jinja2 templating**. Designed for **data engineers** and **data architects** to streamline environment provisioning across clients and projects.

---

## 🧠 Architecture Overview

This solution follows a modular and secure architecture:
<img width="468" height="224" alt="image" src="https://github.com/user-attachments/assets/1a758672-4236-4d37-b4c6-4be1761301b1" />

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

```
git clone https://github.com/your-org/fabric-workspace-deployer.git
cd fabric-workspace-deployer
```

### 2. Define Secrets in GitHub

Go to **Settings → Secrets and variables → Actions** and add:

- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `CAPACITY_ID`

### 3. Define Workspace Structure

Create or edit `config/workspaces.json`:

```json
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
```

---

## 🚀 Usage

### Manual Trigger via GitHub Actions

To manually deploy Fabric workspaces:

1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Deploy Fabric Workspaces** workflow.
3. Click **Run workflow**.

#### This will:

- Load secrets and workspace definitions.
- Render `workspace_config.json` using Jinja2.
- Deploy workspaces and lakehouses via the Fabric API.

---

## 🛠️ Customization

- **Multiple Clients**  
  Create separate workspace definition files (e.g. `clientA_workspaces.json`) and modify `render_config.py` to load based on input.

- **Environment Support**  
  Use a matrix strategy in GitHub Actions to deploy to `dev`, `staging`, and `prod`.

- **Logging**  
  Extend `deploy.py` with logging to a file or external monitoring tools.

---

## ✅ Best Practices

- Use version-controlled workspace definitions for auditability.
- Rotate secrets regularly and use GitHub environments for separation.
- Validate workspace names to avoid duplicates or naming conflicts.
- Modularize Python scripts for easier testing and extension.

---

## 📁 Project Structure

The repository is organized as follows:

```json
{
  "fabric-workspace-deployer": {
    ".github": {
      "description": "GitHub-specific files",
      "workflows": {
        "main.yaml": "GitHub Actions workflow definition"
      }
    },
    "config": {
      "description": "Workspace configuration files",
      "workspaces.json": "Workspace definitions"
    },
    "scripts": {
      "description": "Python scripts for deployment",
      "deploy.py": "Deployment logic",
      "render_config.py": "Jinja2 rendering logic"
    },
    "templates": {
      "description": "Jinja2 templates",
      "workspace_config_template.j2": "Template for workspace config"
    },
    "README.md": "Project documentation"
  }
}
```
---

## 👥 Maintainers

Built by and for data engineers and architects who value automation, reproducibility, and clean infrastructure-as-code practices.






