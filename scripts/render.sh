#!/usr/bin/env bash
set -euo pipefail
: "${TAG:?TAG is required}"
: "${DOCKER_USER:?DOCKER_USER is required}"

for f in k8s/deploy-blue.yaml k8s/deploy-green.yaml; do
  sed "s/{{TAG}}/${TAG}/g; s/DOCKER_USER/${DOCKER_USER}/g" "$f" > "/tmp/$(basename "$f")"
done
cp k8s/service.yaml /tmp/service.yaml
echo "Rendered to /tmp/deploy-blue.yaml, /tmp/deploy-green.yaml, /tmp/service.yaml"
