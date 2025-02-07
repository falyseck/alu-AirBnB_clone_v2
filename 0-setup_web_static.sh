#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# Create required directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link (force if exists)
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration if not already configured
CONFIG_FILE="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$CONFIG_FILE"; then
  sudo sed -i '/server_name _;/a\\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n        index index.html;\n    }\n' "$CONFIG_FILE"
fi

# Restart Nginx
sudo systemctl restart nginx
