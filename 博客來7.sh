#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/pre_process.sh"
cd "$SCRIPT_DIR"
if [[ "$(uname -s)" == "Linux" && "$(uname -m)" =~ ^(aarch64|arm64)$ ]]; then
    uv run books_selenium.py books 7 -x -u chrome
else
    uv run books_selenium.py books 7 -x
fi
