output "workspace_ids" {
  description = "Map of workspace name -> id"
  value       = { for k, v in fabric_workspace.ws : k => v.id }
}

output "deployment_pipeline_id" {
  description = "The created deployment pipeline id"
  value       = fabric_deployment_pipeline.deploy_pipeline.id
}