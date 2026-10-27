---
name: sync-dashboard
description: Push the experiments folder to the founder's live dashboard (a Claude Dashboard artifact with four tabs - Today, Board, Model, Log), creating the dashboard on the first run. Use when the founder says "sync the dashboard", after /new-experiment, /log-experiment or /pull-evidence, or when the Stop hook says a sync is due.
---

The dashboard is a Claude **Dashboard** artifact (Anthropic's built-in type), private to the
founder until they share it. Its link is `dashboard_url` in `kit.config.json`. It reads four
attached data files built from this repo (`experiments`, `canvas`, `canvas-meta`, `events`) and, for
a running card that names one, a live query (`live_dataset`). Its page is
`dashboard/dash-index.html`.

## 1. Build (every run)

In the repo root:

```
python dashboard/build_data.py
python dashboard/build_dash_files.py
```

The first reads every test card header and both canvases, rewrites `experiments/PROGRESS.md` (never
hand-edit it) and writes the bundle. A `PROBLEM:` line means a header or canvas row is malformed: fix
that file and run it again. Nothing is pushed until the build is clean. The second writes
`dashboard/out/experiments.json`, `canvas.json`, `canvas-meta.json`, `events.json` and
`index.doc.json` (the page, with `kit.config.json`'s name, time zone and weekend written into it).

## 2. First run only: create the dashboard (`dashboard_url` is empty)

1. `Artifact` publish with `type_url: "https://claude.ai/artifact/GZLZthZ2sQjn7T16skfdeF"` (the
   Dashboard type), `title` = `"<business> experiments"` from `kit.config.json`, `auto_open:
   "after_first_write"`, and nothing else. The result carries the new dashboard's `url` and the
   type's own instructions: follow those for anything this skill does not say.
2. Write that `url` into `kit.config.json` as `dashboard_url` straight away, so a failure below
   does not create a second dashboard next time.
3. Upload the four data files: `Artifact` with that `url`, `asset: true`, `file_path` = each JSON
   file in `dashboard/out/` except `index.doc.json`, one call per file. Keep each reply's `/_blob/…`
   url.
4. Load `ArtifactData` (`ToolSearch` query `select:ArtifactData`) and write one `batch` on the url:
   - `set` `dash/meta` `{title: "<business> experiments"}`
   - for each of the four files, `set` `datasets/<id>` (`experiments`, `canvas`, `canvas-meta`,
     `events`) with `{title, description, source: {kind: "file", url: "<its /_blob url>", name:
     "<file name>"}, updated: {at: "<now, ISO with the config's utc_offset>", by: "Claude, from the
     experiments repo"}, schedule: "Claude re-syncs it whenever a card changes", staleAfterHours: 168}`.
     Titles: "Experiment board", "Canvas boxes", "Canvas version and riskiest box", "What changed,
     by date". Descriptions: one sentence each on what the file holds, ending "Synced by Claude from
     the repo."
   - `set` `files/index.html` with `file_path` = `dashboard/out/index.doc.json` (it holds `{text}`).
5. **Check**: `ArtifactData` `get` collection `data/users/me`, doc `check`. While it says
   `checking`, read again (5 reads at most). If it says `failed`, fix what it names in
   `dashboard/dash-index.html` (in the repo, so the fix is kept), build, write the page again, and
   check again (2 fixes at most).
6. Tell the founder the link, and that only they can see it until they share it.

## 3. Every later run: point the datasets at new copies

1. Upload the four data files as in 2.3.
2. `ArtifactData` `list` collection `datasets` on the url; note each dataset's `version`.
3. One `batch`: for each of the four, `update` `datasets/<id>` with `if_version` and
   `data: {source: {kind: "file", url: "<new /_blob url>", name: "<file name>"}, updated: {at:
   "<now>", by: "Claude, from the experiments repo"}}`. If `dashboard/dash-index.html` changed since
   the last sync, add `set` `files/index.html` with `file_path` = `dashboard/out/index.doc.json` and
   the `if_version` from a `get` of it. On a version conflict, read the versions again and retry
   once; if it conflicts again, stop and say so.
4. If the page changed, run the check of 2.5.

## 4. Record and report (every run)

After the batch succeeded, run `python dashboard/mark_synced.py`. That stamp is what the Stop hook
(`dashboard/check_sync.py`) checks, so a session cannot end with the dashboard behind the cards
without being told. Then tell the founder in one line: synced, N experiments, the canvas versions,
the link.

Each upload and each batch asks the founder to approve it. A session with nobody to approve (a
scheduled or headless run) cannot sync: say so, and leave it to the founder's next `/sync-dashboard`.
Old uploads are not deleted; the dashboard's Sources panel shows storage and can prune them.
