#!/bin/bash
# Claude Code Stop hook: if this turn left uncommitted code changes without the docs they need,
# block the stop once (exit 2) and show Claude the findings. Silent in repos without a docs index
# (docs/README.md or docs/MAP.md). Only change-related findings count, never old structure errors.
input=$(cat)
active=$(printf '%s' "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("stop_hook_active", False))' 2>/dev/null)
[ "$active" = "True" ] && exit 0                       # already continued once for a stop hook: never loop
cwd=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("cwd", ""))' 2>/dev/null)
root=$(git -C "${cwd:-${CLAUDE_PROJECT_DIR:-.}}" rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$root/docs/README.md" ] || [ -f "$root/docs/MAP.md" ] || exit 0   # repo does not use the docs system
[ -n "$(git -C "$root" status --porcelain)" ] || exit 0  # nothing uncommitted to check
out=$(python3 - "$root" "$(dirname "$0")" <<'EOF'
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[2])
import docs_audit
try:
    found = docs_audit.changed(Path(sys.argv[1]), "HEAD")
except ValueError:
    sys.exit(0)  # no HEAD yet (empty repo): nothing to compare
# an out-of-date knowledge map is regenerated, never reported; a missing one is left for setup
if any(f[2].startswith("stale") for f in docs_audit.map_findings(Path(sys.argv[1]))):
    docs_audit.write_map(Path(sys.argv[1]))
for level, path, msg in found:
    if level != "INFO":
        print("%-5s %s: %s" % (level, path, msg))
sys.exit(1 if any(f[0] == "ERROR" for f in found) else 0)
EOF
)
[ $? -eq 1 ] || exit 0                                 # warnings alone never block
{ echo "Docs check failed for $root (docs-system). Update the docs below, or tell the user why none are needed:"
  printf '%s\n' "$out"; } >&2
exit 2
