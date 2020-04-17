#!/bin/bash
set -e

echo "[INFO] Exec entrypoint.d"
chmod +x -R /mnt/custom/entrypoint.d/*
run-parts --regex="^[a-zA-Z0-9._-]+$" --report /mnt/custom/entrypoint.d

exit 0

