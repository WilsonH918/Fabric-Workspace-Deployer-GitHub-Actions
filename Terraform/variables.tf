variable "capacity_id" {
  description = "Fabric capacity UUID"
  type        = string
}

variable "deployment_admin_object_id" {
  description = "User Object ID for admin access"
  type        = string
}

variable "workspace_configs" {
  description = "List of workspace configurations"
  type = list(object({
    name          = string
    lakehouse     = string
    warehouse     = string
    pipelineStage = string
    folders       = list(object({
      name = string
    }))
  }))
}