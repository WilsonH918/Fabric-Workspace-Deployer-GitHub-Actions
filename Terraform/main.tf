locals {
  configs = { for w in var.workspace_configs : w.name => w }
  pipeline_stages = distinct([for w in var.workspace_configs : w.pipelineStage if w.pipelineStage != ""])
  stage_to_workspace = {for w in var.workspace_configs : w.pipelineStage => w.name if w.pipelineStage != ""}

  # Flatten folders into a map with unique keys
  flat_folders = {
    for f in flatten([
      for ws in var.workspace_configs : [
        for folder in ws.folders : {
          workspace_name = ws.name
          display_name   = folder.name
        }
      ]
    ]) :
    "${f.workspace_name}-${f.display_name}" => f
  }
}


# --------------------
# Workspaces
# --------------------
resource "fabric_workspace" "ws" {
  for_each     = local.configs
  display_name = each.key
  description  = "Created by Terraform: ${each.key}"
  capacity_id  = var.capacity_id
}

# --------------------
# Lakehouses
# --------------------
resource "fabric_lakehouse" "lake" {
  for_each     = { for k, v in local.configs : k => v if v.lakehouse != "" }
  display_name = each.value.lakehouse
  workspace_id = fabric_workspace.ws[each.key].id
}

# --------------------
# Warehouses
# --------------------
resource "fabric_warehouse" "wh" {
  for_each     = { for k, v in local.configs : k => v if v.warehouse != "" }
  display_name = each.value.warehouse
  workspace_id = fabric_workspace.ws[each.key].id
}

# --------------------
# Workspace Admin Role Assignment
# --------------------
resource "fabric_workspace_role_assignment" "admin" {
  for_each    = local.configs
  workspace_id = fabric_workspace.ws[each.key].id

  principal = {
    id   = var.deployment_admin_object_id
    type = "User"
  }

  role = "Admin"
}

# --------------------
# Folders
# --------------------
resource "fabric_folder" "folders" {
  for_each = local.flat_folders

  display_name = each.value.display_name
  workspace_id  = fabric_workspace.ws[each.value.workspace_name].id
}

# --------------------
# Deployment Pipeline
# --------------------
resource "fabric_deployment_pipeline" "deploy_pipeline" {
  display_name = "Terraform_demo_DE_Deployment_Pipeline"
  description  = "Created by Terraform: Terraform_demo_DE_Deployment_Pipeline"

  stages = [
    for stage_name in local.pipeline_stages : {
      display_name = stage_name
      description  = "Stage ${stage_name} for Terraform deployment"
      workspace_id = fabric_workspace.ws[ local.stage_to_workspace[stage_name] ].id
      is_public    = false
    }
  ]
}

# --------------------
# Deployment Pipeline Admin
# --------------------
resource "fabric_deployment_pipeline_role_assignment" "pipeline_admin" {
  deployment_pipeline_id = fabric_deployment_pipeline.deploy_pipeline.id

  principal = {
    id   = var.deployment_admin_object_id
    type = "User"
  }

  role = "Admin"
}