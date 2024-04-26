SolarRPC - Solar-Powered Bitcoin RPC Service

Welcome to SolarRPC, your one-stop solution for a sustainable Bitcoin RPC service powered entirely by solar energy. This project aims to provide reliable RPC access while minimizing carbon footprint through innovative solar technology.
Overview

SolarRPC leverages renewable solar energy to run its Bitcoin RPC service, promoting sustainability and environmental responsibility. The service is designed for reliability, security, and scalability, making it an ideal choice for those seeking a greener alternative to traditional RPC providers.
Features

    Secure and reliable Bitcoin RPC access
    Utilizes renewable solar energy for operation
    Efficient load balancing and health checks through Nginx
    Rate limiting and authentication via Kong server

Configuration

The config directory contains the following configuration files:

    bitcoin_health_check.py: Python script that checks the nodes and ensures they are available for load-balancing.
    btc-nodes-upstream.conf: Is a sample Nginx upstream config, which will be used to distribute load between the healthy nodes.
    btc-nodes.conf: Is the config that listens and then sends it to the upstream nodes.

Feel free to modify these configurations according to your requirements.

If you have any questions, feedback, or suggestions, please don't hesitate to reach out by contacting us. Your contributions are also welcome! Feel free to submit pull requests or open issues if you encounter any issues or have ideas for improvement.

Some more details here : https://solarrpc.xyz
