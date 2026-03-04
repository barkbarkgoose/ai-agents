#!/usr/bin/env bash
# inject-harness-frontmatter.sh
# Builds harness-specific frontmatter from JSON config and prepends it to agent files.
#
# Usage: ./inject-harness-frontmatter.sh <harness> <dest-agents-dir>

set -euo pipefail

HARNESS="${1:?Usage: $0 <harness> <dest-agents-dir>}"
DEST_DIR="${2:?Usage: $0 <harness> <dest-agents-dir>}"
FRONTMATTER_DIR="$(cd "$(dirname "$0")/.." && pwd)/agent-frontmatter"

if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is required. Install with: brew install jq"
  exit 1
fi

shopt -s nullglob
agent_files=("$DEST_DIR"/*.md)

[[ ${#agent_files[@]} -eq 0 ]] && exit 0

echo "    -> Injecting $HARNESS frontmatter..."
for dest_file in "${agent_files[@]}"; do
  agent_name=$(basename "$dest_file" .md)
  config="$FRONTMATTER_DIR/${agent_name}.json"

  [[ ! -f "$config" ]] && continue

  frontmatter=$(jq -r \
    '(.defaults // {}) * (.harnesses[$h] // {}) | with_entries(select(.value != null)) | to_entries[] |
     if (.value | type) == "array" then
       "\(.key):\n" + (.value[] | "  - \(.)") 
     else
       "\(.key): \(.value)"
     end' \
    --arg h "$HARNESS" "$config")

  [[ -z "$frontmatter" ]] && continue

  printf -- "---\n%s\n---\n" "$frontmatter" | cat - "$dest_file" > "${dest_file}.tmp" && mv "${dest_file}.tmp" "$dest_file"
  echo "      -> $agent_name"
done
