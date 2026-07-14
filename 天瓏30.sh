#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/pre_process.sh"
cd "$SCRIPT_DIR"
uv run best_seller.py tenlong 30 -x
