#!/bin/bash
# Two-row Claude Code status line:
#   TID | PROVIDER | CONTEXT | SESSION | WEEK | PROJECT | GIT
# Reads the statusline JSON from stdin (see https://code.claude.com/docs/en/statusline.md)

input=$(cat)

# ---- extract fields -------------------------------------------------------
sid=$(jq -r '.session_id // ""' <<<"$input")
tid="${sid:---}"

model=$(jq -r '.model.display_name // .model.id // "--"' <<<"$input")

ctx_pct=$(jq -r '.context_window.used_percentage // empty' <<<"$input")
ctx_used=$(jq -r '.context_window.total_input_tokens // empty' <<<"$input")
ctx_size=$(jq -r '.context_window.context_window_size // empty' <<<"$input")

fmt_tokens() {
  local n=$1
  if [ -z "$n" ]; then echo "?"; return; fi
  if [ "$n" -ge 1000000 ]; then
    if [ $((n % 1000000)) -eq 0 ]; then echo "$((n / 1000000))M"
    else printf '%.1fM\n' "$(bc -l <<<"$n/1000000")"; fi
  elif [ "$n" -ge 1000 ]; then echo "$((n / 1000))k"
  else echo "$n"; fi
}

if [ -n "$ctx_pct" ] && [ -n "$ctx_size" ]; then
  context="$(printf '%.0f' "$ctx_pct")% ($(fmt_tokens "${ctx_used:-0}")/$(fmt_tokens "$ctx_size"))"
else
  context="--"
fi

session="--"
sess_pct=$(jq -r '.rate_limits.five_hour.used_percentage // empty' <<<"$input")
sess_reset=$(jq -r '.rate_limits.five_hour.resets_at // empty' <<<"$input")
if [ -n "$sess_pct" ]; then
  session="$(printf '%.0f' "$sess_pct")%"
  [ -n "$sess_reset" ] && session="$session @$(date -r "$sess_reset" +%H:%M 2>/dev/null)"
fi

week="--"
week_pct=$(jq -r '.rate_limits.seven_day.used_percentage // empty' <<<"$input")
week_reset=$(jq -r '.rate_limits.seven_day.resets_at // empty' <<<"$input")
if [ -n "$week_pct" ]; then
  week="$(printf '%.0f' "$week_pct")%"
  [ -n "$week_reset" ] && week="$week @$(date -r "$week_reset" +%m/%d 2>/dev/null)"
fi

proj_dir=$(jq -r '.workspace.project_dir // .cwd // ""' <<<"$input")
project=$(basename "${proj_dir:-?}")

# ---- git segment ----------------------------------------------------------
git_seg="--"
cwd=$(jq -r '.workspace.current_dir // .cwd // ""' <<<"$input")
if [ -n "$cwd" ] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --short HEAD 2>/dev/null)
  added=0 changed=0 deleted=0
  while IFS= read -r line; do
    xy="${line:0:2}"
    case "$xy" in
      \?\?|A?|?A) added=$((added + 1)) ;;
      *D*)        deleted=$((deleted + 1)) ;;
      *)          changed=$((changed + 1)) ;;
    esac
  done < <(git -C "$cwd" status --porcelain 2>/dev/null)
  git_seg="$branch +$added ~$changed -$deleted"
fi

# ---- layout ---------------------------------------------------------------
# Pad plain text to column width first, then colorize, so ANSI codes
# don't break the alignment between the header and value rows.
DIM=$'\033[2;37m'; RST=$'\033[0m'
C_TID=$'\033[0;37m'      # gray
C_PROV=$'\033[1;36m'     # cyan
C_CTX=$'\033[1;32m'      # green
C_SESS=$'\033[1;33m'     # yellow
C_WEEK=$'\033[1;34m'     # blue
C_PROJ=$'\033[1;35m'     # magenta
C_GIT=$'\033[0;32m'      # green

# Renders one header row + one value row from the global H/V/C arrays.
render_group() {
  local row1="" row2="" i h v w hp vp n=${#H[@]}
  for i in "${!H[@]}"; do
    h=${H[$i]}; v=${V[$i]}
    w=${#h}; [ ${#v} -gt "$w" ] && w=${#v}
    hp=$(printf '%-*s' "$w" "$h")
    vp=$(printf '%-*s' "$w" "$v")
    row1+="${DIM}${hp}${RST}"
    row2+="${C[$i]}${vp}${RST}"
    if [ "$i" -lt $((n - 1)) ]; then
      row1+=" ${DIM}|${RST} "
      row2+=" ${DIM}|${RST} "
    fi
  done
  printf '%s\n%s\n' "$row1" "$row2"
}

H=(PROJECT GIT)
V=("$project" "$git_seg")
C=("$C_PROJ" "$C_GIT")
render_group

H=(TID MODEL CONTEXT SESSION WEEK)
V=("$tid" "$model" "$context" "$session" "$week")
C=("$C_TID" "$C_PROV" "$C_CTX" "$C_SESS" "$C_WEEK")
render_group
