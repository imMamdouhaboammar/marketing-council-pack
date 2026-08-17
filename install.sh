#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${1:-generic}"
CUSTOM_DEST="${2:-}"
BUILD="$ROOT/dist/marketing-council"
RELEASE="$ROOT/dist/release"
VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["version"])' "$ROOT/manifest.json")"

build_skill() {
  python3 "$ROOT/scripts/build_dist.py" --output "$BUILD" >/dev/null
}

build_release() {
  python3 "$ROOT/scripts/build_host_packages.py" --output-root "$RELEASE" >/dev/null
}

case "$HOST" in
  generic)
    build_skill
    DEST="${CUSTOM_DEST:-$HOME/.agents/skills}"
    ;;
  claude|claude-skill)
    build_skill
    DEST="${CUSTOM_DEST:-$HOME/.claude/skills}"
    ;;
  copilot)
    build_skill
    DEST="${CUSTOM_DEST:-$HOME/.copilot/skills}"
    ;;
  chatgpt|openai|codex|openai-plugin)
    build_release
    echo "$RELEASE/marketing-council-openai-plugin-v$VERSION.zip"
    exit 0
    ;;
  claude-plugin)
    build_release
    echo "$RELEASE/marketing-council-claude-marketplace-v$VERSION.zip"
    exit 0
    ;;
  release)
    build_release
    echo "$RELEASE"
    exit 0
    ;;
  *)
    echo "Usage: $0 {generic|claude|claude-skill|copilot|chatgpt|openai|codex|openai-plugin|claude-plugin|release} [destination-directory]" >&2
    exit 2
    ;;
esac

mkdir -p "$DEST"
rm -rf "$DEST/marketing-council"
cp -R "$BUILD" "$DEST/marketing-council"
echo "$DEST/marketing-council"
