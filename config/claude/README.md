# Claude Code config

Reference copies of Claude Code user-level configuration. These are applied
**manually** — nothing in `sync.sh` touches them. Copy/merge what you want on
each machine.

Claude Code's user-level config root is `~/.claude/`. The main file is
`~/.claude/settings.json`.

## Files in this folder

| File | Goes to | How |
|------|---------|-----|
| `statusline.sh` | `~/.claude/statusline.sh` | copy whole file, keep executable |
| `settings.snippet.json` | `~/.claude/settings.json` | merge into existing file (see below) |

## statusline.sh

Custom two-group status line (PROJECT/GIT on top, TID/MODEL/CONTEXT/SESSION/WEEK
below). Requires `jq` (`brew install jq`).

```bash
cp statusline.sh ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
```

Then make sure `settings.json` points at it — that's what the snippet does.

## settings.snippet.json

A *fragment* of `settings.json`, not a full replacement. It contains only the
keys this repo manages (currently just `statusLine`). Never copy it over your
whole `settings.json` — that file also holds machine-local settings
(`model`, `permissions`, `effortLevel`, etc.) that intentionally differ per
device and are not synced.

### Applying it by hand

Open `~/.claude/settings.json` and add/replace the top-level keys from the
snippet. For the status line that means:

```json
"statusLine": {
  "type": "command",
  "command": "~/.claude/statusline.sh"
}
```

### Applying it with jq

`jq` can do the merge for you. The `*` operator deep-merges two objects:
right-hand side wins wherever keys collide, everything else in the left-hand
object is preserved.

```bash
jq -s '.[0] * .[1]' ~/.claude/settings.json settings.snippet.json > /tmp/settings.json \
  && mv /tmp/settings.json ~/.claude/settings.json
```

How that works:

- `-s` (slurp) reads both files into a single array: `[.settings, .snippet]`.
- `.[0] * .[1]` merges the snippet (`.[1]`) into your settings (`.[0]`).
  Because the snippet is on the right, its keys win — but only the keys it
  declares. Your `model`, `permissions`, etc. pass through untouched.
- Output goes to a temp file first; jq can't write in place, and redirecting
  straight onto the input file would truncate it before jq reads it.

Caveats:

- `*` deep-merges **objects** but replaces **arrays wholesale**. If a snippet
  ever contains an array (e.g. `permissions.allow`), the merge overwrites the
  machine's array rather than unioning it. Fine for `statusLine`; be careful
  if you add list-valued settings here.
- jq requires strict JSON — it will fail loudly (good) if either file has
  trailing commas or comments.

Verify afterwards with `jq . ~/.claude/settings.json` (parses = valid), then
restart Claude Code or start a new session to pick up the change.
