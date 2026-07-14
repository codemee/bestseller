#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/3] 正在抓取天瓏 7 日排行榜..."
"$SCRIPT_DIR/天瓏7.sh"

echo "[2/3] 正在抓取博客來 7 日排行榜..."
"$SCRIPT_DIR/博客來7.sh"

echo "[3/3] 正在寄送最新排行榜 Excel..."
uv run send_excel_email.py "$SCRIPT_DIR"

echo "7 日排行榜抓取與寄送完成。"
