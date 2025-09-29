import json, requests, os

# Get access token from Microsoft Entra ID
def get_access_token():
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

# Main execution
def main():
    
    with open("workspace_config.json") as f:
        config = json.load(f)

    capacity_id = config.get("capacityId")
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")
    tenant_id = config.get("tenant_id")

    token = get_access_token()
    if not capacity_id:
        print("No capacityId found in config. Exiting.")
        return

    existing = get_existing_workspaces(token)

    for ws in config["workspaces"]:
        name = ws["name"]
        if name in existing:
            print(f"Workspace '{name}' already exists. Skipping.")
            continue

        print(f"Creating workspace: {name}")
        workspace_id = create_workspace(token, name, capacity_id)

        if workspace_id and "lakehouse" in ws:
            print(f"Creating lakehouse: {ws['lakehouse']} in workspace '{name}'")
            create_lakehouse(token, workspace_id, ws["lakehouse"])

if __name__ == "__main__":
    main()