#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ensure_homebrew() {
    if command -v brew >/dev/null 2>&1; then
        return
    fi

    echo "找不到 Homebrew。請先依照 https://brew.sh/ 的說明安裝 Homebrew。" >&2
    exit 1
}

install_with_brew() {
    local package="$1"

    ensure_homebrew
    echo "正在用 Homebrew 安裝 ${package}..."
    brew install "$package"
}

if ! command -v uv >/dev/null 2>&1; then
    install_with_brew uv
fi

if ! command -v git >/dev/null 2>&1; then
    install_with_brew git
fi
