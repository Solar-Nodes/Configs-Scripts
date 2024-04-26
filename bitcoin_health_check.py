import requests
import subprocess
import time
import re

nodes = [
    {'url': 'http://x.x.x.x:8332', 'weight': 1},
    {'url': 'http://y.y.y.y:8332', 'weight': 1},
]

NGINX_CONF_PATH = '/etc/nginx/btc-nodes-upstream.conf'
UPSTREAM_NAME = 'bitcoin_nodes'
RPC_USERNAME = 'username'
RPC_PASSWORD = 'password'

def check_node_health(node):
    try:
        response = requests.post(
            f'{node["url"]}',
            json={
                "jsonrpc": "1.0",
                "id": "curltest",
                "method": "getblockchaininfo",
                "params": []
            },
            auth=(RPC_USERNAME, RPC_PASSWORD),
            timeout=30
        )
        if response.status_code == 200:
            result = response.json().get("result")
            if result and "blocks" in result:
                block_count = result["blocks"]
                print(f'Node {node["url"]} is healthy with block height {block_count}')
                return True
            else:
                print(f'Node {node["url"]} did not return valid blockchain info. Removing from upstream.')
                return False
        else:
            print(f'Node {node["url"]} responded with status code {response.status_code}. Removing from upstream.')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Error while checking node {node["url"]}: {e}. Removing from upstream.')
        return False


def update_nginx_config(nodes):
    # Filter out unhealthy nodes
    healthy_nodes = [node for node in nodes if check_node_health(node)]

    # Generate the new upstream configuration
    upstream_config = f'upstream {UPSTREAM_NAME} {{\n'
    for node in healthy_nodes:
        # Strip the protocol part from the URL
        url_without_protocol = node["url"].split("://")[-1]
        upstream_config += f'    server {url_without_protocol} weight={node["weight"]};\n'
    upstream_config += '}'

    # Read the existing Nginx configuration file
    with open(NGINX_CONF_PATH, 'r') as f:
        nginx_config_lines = f.readlines()

    # Find the line numbers of the upstream block
    start_index = None
    end_index = None
    for i, line in enumerate(nginx_config_lines):
        if re.match(fr'^\s*upstream\s+{UPSTREAM_NAME}\s*{{\s*$', line):
            start_index = i
        elif start_index is not None and line.strip() == '}':
            end_index = i
            break

    if start_index is not None and end_index is not None:
        # Check if the new upstream configuration is different from the existing one
        existing_upstream = ''.join(nginx_config_lines[start_index:end_index + 1])
        if existing_upstream != upstream_config:
            # Update the existing upstream block
            nginx_config_lines[start_index:end_index + 1] = [upstream_config]

            # Write the updated Nginx configuration file
            with open(NGINX_CONF_PATH, 'w') as f:
                f.writelines(nginx_config_lines)

            # Validate the configuration and reload Nginx
            subprocess.run(['nginx', '-t'], check=True)
            subprocess.run(['nginx', '-s', 'reload'])
            print("Nginx configuration updated and reloaded.")
        else:
            print("No changes to Nginx configuration. Skipping reload.")
    else:
        print("Error: Upstream block not found in Nginx configuration.")


def main():
    while True:
        # Update Nginx configuration with the healthy Bitcoin nodes
        update_nginx_config(nodes)

        # Sleep for 60 seconds before checking again
        time.sleep(5)

if __name__ == "__main__":
    main()
