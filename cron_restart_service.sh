#!/bin/bash

# the container should be restarted every night to prevent all sorts of issues
# wanted side effect: all user uploaded files are deleted

# make executable with `chmod +x /path/to/restart_container.sh``
# add to crontab with `crontab -e`
# 0 0 * * * /path/to/restart_container.sh


# Restart the Docker container
docker compose -f /path/to/your/docker-compose.yaml restart ocr-my-pdf-flask

