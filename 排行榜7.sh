#!/usr/bin/env bash

set -uo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

failed=0

echo "[$(date --iso-8601=seconds)] [1/3] 正在抓取天瓏 7 日排行榜..."
if ! "$SCRIPT_DIR/天瓏7.sh"; then
    echo "[$(date --iso-8601=seconds)] 天瓏排行榜失敗。" >&2
    failed=1
fi

echo "[$(date --iso-8601=seconds)] [2/3] 正在抓取博客來 7 日排行榜..."
if ! "$SCRIPT_DIR/博客來7.sh"; then
    echo "[$(date --iso-8601=seconds)] 博客來排行榜失敗。" >&2
    failed=1
fi

if (( failed )); then
    echo "[$(date --iso-8601=seconds)] 至少一個排行榜失敗，不寄送郵件。" >&2
    exit 1
fi

echo "[$(date --iso-8601=seconds)] [3/3] 正在寄送最新排行榜 Excel..."
uv run send_excel_email.py "$SCRIPT_DIR"

echo "[$(date --iso-8601=seconds)] 7 日排行榜抓取與寄送完成。"
