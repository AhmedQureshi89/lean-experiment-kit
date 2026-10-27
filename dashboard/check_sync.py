#!/usr/bin/env python3
"""Stop hook: do not let a session end while experiments/ is newer than the last dashboard sync.

Reads the hook payload on stdin. Prints a JSON decision when a sync is due, nothing otherwise.
The stamp dashboard/.last-sync is written by mark_synced.py at the end of /sync-dashboard.
Only .md files count: CSV send lists never sync (they hold recipient data).
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXP = ROOT / 'experiments'
STAMP = ROOT / 'dashboard' / '.last-sync'

try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}
if payload.get('stop_hook_active'):      # already continuing because of this hook: never loop
    sys.exit(0)

newest, newest_path = 0.0, None
for p in EXP.rglob('*.md'):
    m = p.stat().st_mtime
    if m > newest:
        newest, newest_path = m, p
last = STAMP.stat().st_mtime if STAMP.exists() else 0.0
if newest_path is not None and newest > last:
    rel = newest_path.relative_to(ROOT).as_posix()
    print(json.dumps({
        'decision': 'block',
        'reason': (f'{rel} changed after the last dashboard sync. Run /sync-dashboard before finishing, '
                   'or tell the founder in one line why the sync is being skipped this time.'),
    }))
sys.exit(0)
