import os
import json
from jinja2 import Environment, FileSystemLoader

def render_config():
    output_path = "workspace_config.json"

    context = {
        "tenant_id": os.getenv("TENANT_ID"),
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "capacity_id": os.getenv("CAPACITY_ID"),
        "workspaces": []
    }


    with open("config/workspaces.json") as f:
        context["workspaces"] = json.load(f)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("workspace_config_template.j2")
    rendered = template.render(**context)

    with open(output_path, "w") as f:
        f.write(rendered)

    print("workspace_config.json rendered successfully.")

if __name__ == "__main__":
    render_config()