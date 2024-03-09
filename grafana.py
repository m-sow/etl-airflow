import requests
import json

# Grafana API endpoint and credentials
grafana_url = 'http://localhost:3000'
username = 'admin'
password = 'admin'

# Define a sample dashboard configuration
dashboard_config = {
    "dashboard": {
        "id": None,  # Set to None for a new dashboard or specify an existing dashboard ID
        "title": "My API Dashboard",
        "refresh": "60s",
        "panels": [
            {
                "id": None,  # Set to None for a new panel or specify an existing panel ID
                "type": "Singlestat",
                "title": "My Graph Panel",
                "datasource": "grafana-postgresql-datasource",
                "targets": [
                    {
                        "expr": "your_metric_query",
                        "legendFormat": "Legend",
                        "refId": "A",
                    }
                ],
            }
        ],
    },
    "folderId": 0,  # Set to the desired folder ID or 0 for the General folder
    "overwrite": True,  # Set to True to overwrite an existing dashboard with the same title
}

# Function to create or update a Grafana dashboard
def create_or_update_dashboard(config):
    url = f'{grafana_url}/api/dashboards/db'
    
    # Create or update the dashboard with HTTP Basic Authentication
    response = requests.post(
        url,
        auth=(username, password),
        headers={'Content-Type': 'application/json'},
        data=json.dumps(config)
    )
    
    if response.status_code == 200:
        print(f"Dashboard '{config['dashboard']['title']}' created/updated successfully.")
    else:
        print(f"Failed to create/update dashboard. Status Code: {response.status_code}, Response: {response.text}")

# Create or update the dashboard using the provided configuration
create_or_update_dashboard(dashboard_config)
