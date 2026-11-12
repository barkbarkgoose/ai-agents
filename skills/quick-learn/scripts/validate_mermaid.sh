#!/usr/bin/env bash

set -euo pipefail

# Checks the Mermaid diagrams in a Markdown guide (```mermaid blocks) or an HTML file
# (.mermaid elements) with the pinned Mermaid version.
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <guide.md|guide.html>" >&2
  exit 2
fi

guide_file="$1"
skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/quick-learn-mermaid-validator"
mermaid_version="10.9.3"
jsdom_version="24.1.3"

if [[ ! -f "$cache_dir/node_modules/mermaid/dist/mermaid.esm.min.mjs" || ! -d "$cache_dir/node_modules/jsdom" ]]; then
  mkdir -p "$cache_dir"
  npm install --silent --prefix "$cache_dir" \
    "mermaid@$mermaid_version" \
    "jsdom@$jsdom_version"
fi

export MERMAID_VALIDATOR_DEPS="$cache_dir"
node "$skill_dir/scripts/validate_mermaid.mjs" "$guide_file"
