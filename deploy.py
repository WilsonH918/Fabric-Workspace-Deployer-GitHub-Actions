import json, requests

# 🔐 Replace these with your actual values
client_id = "4973351f-c1f8-473f-a9a7-815f670f48cd"
client_secret = "ibI8Q~4vrBjEPL8oXa-_8iFOVlvCHiJow3A9za-N"
tenant_id = "b38dfeb3-1654-4f43-bc5b-efe2121197f5"

def get_access_token():
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://api.fabric.microsoft.com/.default",
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=payload)
    return response.json()["access_token"]

def create_workspace(token, name):
    url = "https://api.fabric.microsoft.com/v1/workspaces"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"displayName": name}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["id"]

def create_lakehouse(token, workspace_id, lakehouse_name):
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"displayName": lakehouse_name}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 🚀 Run deployment
token = get_access_token()

with open("workspace_config.json") as f:
    config = json.load(f)

for ws in config["workspaces"]:
    print(f"Creating workspace: {ws['name']}")
    workspace_id = create_workspace(token, ws["name"])
    if "lakehouse" in ws:
        print(f"Creating lakehouse: {ws['lakehouse']} in {ws['name']}")
        create_lakehouse(token, workspace_id, ws["lakehouse"])