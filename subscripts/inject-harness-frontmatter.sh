#!/usr/bin/env bash
# inject-harness-frontmatter.sh
# Builds harness-specific frontmatter from JSON config and writes it as the
# ONLY YAML frontmatter block in each agent file. The agent body is assumed
# to contain no leading YAML frontmatter of its own; this script is the
# single source of frontmatter.
#
# Only agent files that have a matching JSON config in agent-frontmatter/ are
# touched. Anything else in the destination directory is left alone.
#
# Usage: ./inject-harness-frontmatter.sh <harness> <dest-agents-dir>

set -euo pipefail

HARNESS="${1:?Usage: $0 <harness> <dest-agents-dir>}"
DEST_DIR="${2:?Usage: $0 <harness> <dest-agents-dir>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTMATTER_DIR="$SCRIPT_DIR/../agent-frontmatter"

if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is required. Install with: brew install jq"
  exit 1
fi

shopt -s nullglob
config_files=("$FRONTMATTER_DIR"/*.json)

[[ ${#config_files[@]} -eq 0 ]] && exit 0

echo "    -> Injecting $HARNESS frontmatter..."
for config in "${config_files[@]}"; do
  agent_name=$(basename "$config" .json)
  dest_file="$DEST_DIR/${agent_name}.md"

  if [[ ! -f "$dest_file" ]]; then
    continue
  fi

  frontmatter=$(jq -r \
    --arg h "$HARNESS" '
    (.defaults // {}) * (.harnesses[$h] // {}) | with_entries(select(.value != null)) | to_entries[] |
      .key as $k | .value |
      if type == "array" then
        $k + ":\n" + ([.[] | "  - \(.)"] | join("\n"))
      elif type == "object" then
        $k + ":\n" + ([to_entries[] | "  \(.key): \(.value)"] | join("\n"))
      else
        $k + ": " + (. | tostring)
      end
    ' "$config")

  [[ -z "$frontmatter" ]] && continue

  {
    printf -- "---\n%s\n---\n" "$frontmatter"
    cat "$dest_file"
  } > "${dest_file}.tmp" && mv "${dest_file}.tmp" "$dest_file"
  echo "      -> $agent_name"
done