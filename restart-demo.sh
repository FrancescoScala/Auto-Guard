#!/bin/bash
set -e

podman build -t ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/example_app:rc1 ./example_app/

podman build -t ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/symphony_provider:rc1 ./symphony_provider/

source /workspaces/shift2sdv/stop-demo.sh

source /workspaces/shift2sdv/start-demo.sh