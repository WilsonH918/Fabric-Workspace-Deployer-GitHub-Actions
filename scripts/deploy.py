import json, requests, os
from collections import defaultdict


# Get access token from Microsoft Entra ID
def get_access_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://api.fabric.microsoft.com/.default",
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

# Get existing workspace names
def get_existing_workspaces(token):
    url = "https://api.fabric.microsoft.com/v1/workspaces"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [ws["displayName"] for ws in response.json().get("value", [])]
    else:
        print("Failed to fetch existing workspaces:", response.text)
        return []

# Create a new workspace
def create_workspace(token, name, capacity_id):
    url = "https://api.fabric.microsoft.com/v1/workspaces"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "displayName": name,
        "capacityId": capacity_id
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        return response.json()["id"]
    elif response.status_code == 400 and "already exists" in response.text:
        print(f"Workspace '{name}' already exists. Skipping.")
        return None
    else:
        print(f"Error creating workspace '{name}':", response.text)
        return None

# Create a lakehouse in a workspace
def create_lakehouse(token, workspace_id, lakehouse_name):
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"displayName": lakehouse_name}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Lakehouse '{lakehouse_name}' created successfully.")
    else:
        print(f"Error creating lakehouse '{lakehouse_name}':", response.text)


# Create a warehouse in a workspace
def create_warehouse(token, workspace_id, warehouse_name):
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"displayName": warehouse_name}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Warehouse '{warehouse_name}' created successfully.")
    else:
        print(f"Error creating warehouse '{warehouse_name}':", response.text)

# Create deployment pipeline
def create_deployment_pipeline(token, name, description, stages):
    url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "displayName": name,
        "description": description,
        "stages": [{"displayName": stage, "description": f"{stage} stage", "isPublic": False} for stage in stages]
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        pipeline = response.json()
        print(f"Deployment pipeline '{name}' created successfully.")
        return pipeline["id"], {s["displayName"]: s["id"] for s in pipeline["stages"]}
    else:
        print(f"Error creating deployment pipeline '{name}':", response.text)
        return None, {}

# Assign workspace to pipeline stage
def assign_workspace_to_stage(token, pipeline_id, stage_id, workspace_id):
    url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{pipeline_id}/stages/{stage_id}/assignWorkspace"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"workspaceId": workspace_id}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Workspace assigned to stage '{stage_id}' in pipeline '{pipeline_id}'.")
    else:
        print(f"Error assigning workspace to stage: {response.text}")


# Main execution
def main():
    with open("workspace_config.json") as f:
        config = json.load(f)

    capacity_id = config.get("capacityId")
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")
    tenant_id = config.get("tenant_id")

    token = get_access_token(tenant_id, client_id, client_secret)

    if not capacity_id:
        print("No capacityId found in config. Exiting.")
        return

    existing_workspaces = get_existing_workspaces(token)
    workspace_ids = {}

    # Group workspaces by pipelineStage
    pipeline_workspaces = defaultdict(list)
    for ws in config["workspaces"]:
        stage = ws.get("pipelineStage")
        if stage:
            pipeline_workspaces[stage].append(ws)

    # Create deployment pipeline if needed
    if pipeline_workspaces:
        pipeline_name = "Auto Deployment Pipeline"
        pipeline_description = "Generated from config"
        stage_names = list(pipeline_workspaces.keys())
        pipeline_id, stage_id_map = create_deployment_pipeline(token, pipeline_name, pipeline_description, stage_names)
    else:
        pipeline_id = None
        stage_id_map = {}

    # Create all workspaces
    for ws in config["workspaces"]:
        name = ws["name"]
        workspace_id = existing_workspaces.get(name)

        if workspace_id:
            print(f"Workspace '{name}' already exists. Using existing ID.")
        else:
            print(f"Creating workspace: {name}")
            workspace_id = create_workspace(token, name, capacity_id)

        if not workspace_id:
            continue

        workspace_ids[name] = workspace_id

        if "lakehouse" in ws:
            create_lakehouse(token, workspace_id, ws["lakehouse"])

        if "warehouse" in ws:
            create_warehouse(token, workspace_id, ws["warehouse"])

        # Assign to pipeline stage if applicable
        stage_name = ws.get("pipelineStage")
        if pipeline_id and stage_name and stage_name in stage_id_map:
            assign_workspace_to_stage(token, pipeline_id, stage_id_map[stage_name], workspace_id)

if __name__ == "__main__":
    main()
