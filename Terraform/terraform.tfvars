capacity_id ="your_capacity_id"
deployment_admin_object_id="your_admin_user_object_id"

workspace_configs = [
  {
    name         = "Terraform_demo_DE_Dev"
    lakehouse    = "Terraform_demo_Fabric_Lakehouse"
    warehouse    = "Terraform_demo_Fabric_Warehouse"
    pipelineStage = "Development"
    folders      = [
      { name = "Notebooks" },
      { name = "Pipelines" },
      { name = "Reports" }
    ]
  },
  {
    name         = "Terraform_demo_DE_Prod"
    lakehouse    = ""          # add empty string
    warehouse    = ""          # add empty string
    pipelineStage = "Production"
    folders      = [
      { name = "Notebooks" },
      { name = "Pipelines" }
    ]
  },
  {
    name         = "Terraform_demo_Report"
    lakehouse    = ""          # add empty string
    warehouse    = ""          # add empty string
    pipelineStage = ""         # add empty string
    folders      = []          # add empty list
  }
]
