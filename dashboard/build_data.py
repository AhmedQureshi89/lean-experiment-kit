#!/usr/bin/env python3
"""Reads the structured header of every experiment's test card and the canvas file, then
(1) writes experiments/PROGRESS.md (the board, generated: edit the cards, not the board) and
(2) writes dashboard/sync-bundle.json, the documents /sync-dashboard pushes to the live dashboard.

Run:  python dashboard/build_data.py
Exit code 1 and PROBLEM lines when a header or the canvas is malformed. Fix the file, re-run.

Each experiment folder experiments/NNNN-<slug>/ has a test-card.md that starts with a YAML header:
  id, title, segment, theme, method, boxes, status, decision, bar, result, effort, evidence, note
  optional: method_note, bar_met, window_start, window_end, decided, held, waiting_on, next,
            test_card, learning_card (file names when they are not test-card.md / learning-card.md),
            and the scoreboard the dashboard draws over `result`: read_at, score_now, score_target,
            score_label, score_parts, score_caveat (see check_score)
Settings (business name, time zone, repo link) come from kit.config.json at the repo root.
A canvas is experiments/canvas/<name>.md with a YAML header and a "## Boxes" table. `kind:` in the
header picks its rules: value-proposition (the default; VP-A, one-letter IDs J1, C4 …) or lean-canvas
(LC-A, two-letter block IDs CH2, RS1 …). There is one canvas of each kind; an experiment's boxes may
come from either. Files under experiments/canvas/ without a header are old versions and are ignored.
"""
import re, json, sys, pathlib, datetime, subprocess
try:
    import yaml
except ImportError:
    sys.exit('PROBLEM: PyYAML is missing. Run: python -m pip install pyyaml')

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXP = ROOT / 'experiments'


def load_config():
    """kit.config.json at the repo root: the business name, time zone, weekend and repo link. Missing keys fall back."""
    try:
        cfg = json.loads((ROOT / 'kit.config.json').read_text(encoding='utf-8'))
    except FileNotFoundError:
        cfg = {}
    except json.JSONDecodeError as e:
        sys.exit(f'PROBLEM: kit.config.json is not valid JSON ({e})')
    return {'business': 'My business', 'timezone': 'UTC', 'utc_offset': '+00:00', 'weekend': ['Sat', 'Sun'],
            'week_starts': 'Mon', 'repo_url': '', 'dashboard_url': '', **cfg}


def offset_tz(text):
    """'+03:00' -> a fixed-offset timezone."""
    sign = -1 if text.startswith('-') else 1
    hours, _, minutes = text.lstrip('+-').partition(':')
    return datetime.timezone(sign * datetime.timedelta(hours=int(hours), minutes=int(minutes or 0)))


CONFIG = load_config()
TZ = offset_tz(CONFIG['utc_offset'])
GITHUB = CONFIG['repo_url'].rstrip('/') + '/blob/main/' if CONFIG['repo_url'] else ''

STATUS = ['planned', 'running', 'hold', 'done']
DECISION = ['none', 'persevere', 'pivot', 'kill']
THEME = ['desirability', 'feasibility', 'viability']
REQUIRED = ['id', 'title', 'segment', 'theme', 'method', 'boxes', 'status', 'decision', 'bar', 'result', 'effort', 'evidence', 'note']
STATUS_TEXT = {'planned': 'Planned', 'running': 'Running', 'hold': 'On hold ⏸️', 'done': 'Done'}
DECISION_TEXT = {'none': '—', 'persevere': 'Persevere ✅', 'pivot': 'Pivot 🔄', 'kill': 'Kill ❌'}
CUSTOMER, BUSINESS = 'JPG', 'SRC'
# customer side: what people want; business side: what you offer and how you run it
TAGS = {'customer': ('seen', 'signal', 'assumption'), 'business': ('live', 'untested', 'gap')}
# The Lean Canvas: block prefix -> (block name, side). VP-A details Problem (its jobs and pains) and Solution (its S, R, C).
LEAN = {'PR': ('Problem', 'customer'), 'CS': ('Customer Segments', 'customer'), 'UV': ('Unique Value Proposition', 'customer'),
        'SO': ('Solution', 'business'), 'CH': ('Channels', 'business'), 'RS': ('Revenue Streams', 'customer'),
        'CO': ('Cost Structure', 'business'), 'KM': ('Key Metrics', 'business'), 'UA': ('Unfair Advantage', 'business')}
ZOOM = {'PR': 'JP', 'SO': 'SRC'}
ID_RE = {'value-proposition': re.compile(r'^[JPGSRC]\d{1,2}$'), 'lean-canvas': re.compile(r'^(?:' + '|'.join(LEAN) + r')\d{1,2}$')}
BOX_TOKEN = re.compile(r'^(~?)((?:[JPGSRC]|' + '|'.join(LEAN) + r')\d{1,2})$')
READ = 2   # a box or row at Evidence 2 or more has been read: seen once in real data, or tried once

problems = []
def problem(msg): problems.append(msg)
def read(p): return pathlib.Path(p).read_text(encoding='utf-8')
def cells(line): return [c.strip() for c in line.strip().strip('|').split('|')]
def s(v): return '' if v is None else str(v).strip()

def front_matter(path):
    """-> (meta dict, body text). meta is {} when the file has no header."""
    text = read(path)
    if not text.startswith('---\n'): return {}, text
    end = text.find('\n---', 4)
    if end == -1: problem(f'{path.name}: header has no closing ---'); return {}, text
    try:
        meta = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as e:
        problem(f'{path.name}: header is not valid YAML ({e})'); meta = {}
    return meta, text[end + 4:].lstrip('\n')

def table(body, heading):
    """Rows of the first markdown table under '## <heading>' as dicts keyed by lower-cased header."""
    m = re.search(r'^## ' + re.escape(heading) + r'\s*$', body, re.M)
    if not m: return []
    rows, header = [], None
    for line in body[m.end():].split('\n'):
        if line.startswith('## '): break
        if not line.startswith('|'): continue
        if re.match(r'^\|\s*:?-{2,}', line): continue
        c = cells(line)
        if header is None: header = [x.lower() for x in c]; continue
        rows.append(dict(zip(header, c)))
    return rows

# ---------- methods (METHODS.md, for checking names only) ----------
def method_names():
    names = {}
    for line in read(EXP / 'METHODS.md').split('\n'):
        if line.startswith('|'):
            c = cells(line)
            if c[0].isdigit() and len(c) >= 2: names[int(c[0])] = c[1]
    return names

def check_method(exp_id, text, names):
    m = re.match(r'^#(\d+) (.+)$', text) or re.match(r'^Custom \(closest: #(\d+) (.+)\)$', text)
    if not m: problem(f'{exp_id}: method "{text}" must be "#NN Name" or "Custom (closest: #NN Name)"'); return None
    n, name = int(m.group(1)), m.group(2).strip()
    if names.get(n) != name: problem(f'{exp_id}: method #{n} is "{names.get(n)}" in METHODS.md, not "{name}"')
    return {'n': n, 'name': name, 'custom': text.startswith('Custom')}

# The dashboard draws the last read as a scoreboard rather than as the one sentence in `result`:
# `result` stays the record, and these say which of its numbers is the headline.
SCORE_SEPS = ('|', '·')   # build_dash_files.py joins the tiles with these, so no tile may hold one

def check_score(exp_id, meta, running):
    """-> the scoreboard fields, checked. All are optional, but score_now, score_target and
    score_label go together, because the page draws one bar from the three. A running experiment
    that has a result must say when that read was taken."""
    read_at = s(meta.get('read_at'))
    if read_at:
        try: datetime.datetime.fromisoformat(read_at)
        except ValueError: problem(f'{exp_id}: read_at "{read_at}" is not an ISO date and time (2026-10-22T09:04{CONFIG["utc_offset"]})')
    elif running and s(meta.get('result')) not in ('', 'not started'):
        problem(f'{exp_id}: it is running and has a result, so read_at must say when that read was taken')
    nums = {}
    for k in ('score_now', 'score_target'):
        v = meta.get(k)
        if v is None or s(v) == '': continue
        if isinstance(v, bool) or not isinstance(v, (int, float)): problem(f'{exp_id}: {k} must be a number, not "{v}"')
        else: nums[k] = v
    if len(nums) == 1: problem(f'{exp_id}: score_now and score_target go together — the dashboard draws the bar from both')
    if nums.get('score_target') is not None and nums['score_target'] <= 0: problem(f'{exp_id}: score_target must be more than 0')
    if nums.get('score_now') is not None and nums['score_now'] < 0: problem(f'{exp_id}: score_now cannot be negative')
    label = s(meta.get('score_label'))
    if nums and not label: problem(f'{exp_id}: a score needs score_label, what the two numbers count')
    parts, raw = [], meta.get('score_parts') or []
    if not isinstance(raw, list):
        problem(f'{exp_id}: score_parts must be a list of {{ n: <count>, label: "what it counts" }}')
    else:
        for p in raw:
            if not isinstance(p, dict) or p.get('n') is None or not s(p.get('label')):
                problem(f'{exp_id}: each score_parts entry is {{ n: <count>, label: "what it counts" }}, not "{p}"'); continue
            n, lab = s(p['n']), s(p['label'])
            if len(n) > 12: problem(f'{exp_id}: score_parts n "{n}" is longer than a tile holds (12 characters)')
            elif any(c in n + lab for c in SCORE_SEPS): problem(f'{exp_id}: score_parts "{n} {lab}" may not hold | or ·')
            else: parts.append({'n': n, 'label': lab})
    return {'readAt': read_at, 'scoreNow': nums.get('score_now'), 'scoreTarget': nums.get('score_target'),
            'scoreLabel': label, 'scoreParts': parts, 'scoreCaveat': s(meta.get('score_caveat'))}

# ---------- experiments ----------
def ts(path): return datetime.datetime.fromtimestamp(path.stat().st_mtime, TZ).isoformat(timespec='seconds')

def load_experiments(names):
    exps = []
    for d in sorted(EXP.iterdir()):
        if not (d.is_dir() and re.match(r'^\d{4}-', d.name)): continue
        card = d / 'test-card.md'
        if not card.exists(): problem(f'{d.name}: no test-card.md'); continue
        meta, _ = front_matter(card)
        if not meta: problem(f'{d.name}/test-card.md: no header (the YAML block between --- lines)'); continue
        eid = s(meta.get('id'))
        for k in REQUIRED:
            if k not in meta or meta[k] is None and k != 'decision': problem(f'{eid or d.name}: header is missing "{k}"')
        if eid != d.name[:4]: problem(f'{d.name}: id "{eid}" does not match the folder')
        if s(meta.get('status')) not in STATUS: problem(f'{eid}: status must be one of {STATUS}')
        dec = s(meta.get('decision')) or 'none'
        if dec not in DECISION: problem(f'{eid}: decision must be one of {DECISION}')
        if s(meta.get('status')) == 'done' and dec == 'none': problem(f'{eid}: Done needs a decision')
        if s(meta.get('status')) != 'done' and dec != 'none': problem(f'{eid}: a decision needs status done')
        if s(meta.get('theme')) not in THEME: problem(f'{eid}: theme must be one of {THEME}')
        for k in ('effort', 'evidence'):
            v = meta.get(k)
            if not (isinstance(v, int) and 0 <= v <= 5): problem(f'{eid}: {k} must be a whole number 0–5')
        boxes = []
        for tok in (meta.get('boxes') or []):
            m = BOX_TOKEN.match(s(tok))
            if m: boxes.append({'id': m.group(2), 'role': 'closest' if m.group(1) else 'main'})
            else: problem(f'{eid}: "{tok}" in boxes is not a box ID (J1, C4, ~G3 from VP-A; CH2, RS1 from LC-A)')
        method = check_method(eid, s(meta.get('method')), names)
        score = check_score(eid, meta, s(meta.get('status')) == 'running')
        test_file = s(meta.get('test_card')) or 'test-card.md'
        learn_file = s(meta.get('learning_card')) or 'learning-card.md'
        if not (d / test_file).exists(): problem(f'{eid}: test_card "{test_file}" does not exist')
        if s(meta.get('learning_card')) and not (d / learn_file).exists(): problem(f'{eid}: learning_card "{learn_file}" does not exist')
        files = sorted(f.name for f in d.glob('*.md'))
        exps.append({
            'id': eid, 'folder': d.name, 'title': s(meta.get('title')), 'segment': s(meta.get('segment')),
            'theme': s(meta.get('theme')), 'method': s(meta.get('method')), 'methodInfo': method,
            'methodNote': s(meta.get('method_note')), 'boxes': boxes,
            'status': s(meta.get('status')), 'decision': dec,
            'bar': s(meta.get('bar')), 'result': s(meta.get('result')), 'barMet': meta.get('bar_met'),
            **score,
            'windowStart': s(meta.get('window_start')), 'windowEnd': s(meta.get('window_end')),
            'decided': s(meta.get('decided')), 'held': s(meta.get('held')),
            'effort': meta.get('effort'), 'evidence': meta.get('evidence'),
            'waitingOn': s(meta.get('waiting_on')), 'next': s(meta.get('next')), 'note': s(meta.get('note')),
            'liveDataset': s(meta.get('live_dataset')), 'countsDataset': s(meta.get('counts_dataset')),
            'sources': [s(x) for x in (meta.get('sources') or [])],
            'testCard': test_file, 'learningCard': learn_file if (d / learn_file).exists() else None,
            'files': files, 'url': GITHUB + 'experiments/' + d.name if GITHUB else '',
        })
    ids = [e['id'] for e in exps]
    for e in exps:
        if e['next'] and e['next'] not in ids: problem(f'{e["id"]}: next "{e["next"]}" is not an experiment')
    return exps

# ---------- canvas ----------
def load_canvas(path):
    meta, body = front_matter(path)
    if not meta: return None
    kind = s(meta.get('kind')) or 'value-proposition'
    if kind not in ID_RE: problem(f'{path.name}: kind "{kind}" should be one of {", ".join(ID_RE)}'); return None
    lean = kind == 'lean-canvas'
    cv = {'id': path.stem, 'name': s(meta.get('canvas')) or path.stem, 'kind': kind, 'zoomIn': s(meta.get('zoom_in')),
          'version': meta.get('version'), 'date': s(meta.get('date')), 'title': s(meta.get('title')), 'segment': s(meta.get('segment')),
          'summary': s(meta.get('summary')), 'riskiest': s(meta.get('riskiest')), 'riskiestWhy': s(meta.get('riskiest_why')),
          'boxes': [], 'fit': [], 'themes': [], 'coverage': [], 'facts': [], 'changes': [], 'notes': []}
    if not isinstance(cv['version'], int): problem(f'{path.name}: version must be a whole number')
    try: datetime.date.fromisoformat(cv['date'])
    except ValueError: problem(f'{path.name}: date "{cv["date"]}" should look like 2026-10-11')
    seen = set()
    for row in table(body, 'Boxes'):
        bid = s(row.get('id'))
        if not ID_RE[kind].match(bid): problem(f'{path.name}: "{bid}" is not a {kind} box ID'); continue
        if bid in seen: problem(f'{path.name}: {bid} is listed twice')
        seen.add(bid)
        if lean: k = bid[:2]; block, side = LEAN[k]
        else: k = bid[0]; block, side = '', 'customer' if k in CUSTOMER else 'business'
        tag, _, tag_note = s(row.get('tag')).partition('·')
        tag, tag_note = tag.strip().lower(), tag_note.strip()
        if tag not in TAGS[side]: problem(f'{path.name}: {bid} tag "{tag}" should be one of {", ".join(TAGS[side])}')
        def score(col, lo, hi):
            v = s(row.get(col))
            if not (v.isdigit() and lo <= int(v) <= hi): problem(f'{path.name}: {bid} {col} must be {lo}–{hi}'); return None
            return int(v)
        cv['boxes'].append({'id': bid, 'canvas': cv['name'], 'side': side, 'kind': k, 'block': block, 'theme': '',
                            'text': s(row.get('box')), 'tag': tag, 'tagNote': tag_note,
                            'matters': score('matters', 1, 3), 'evidence': score('evidence', 0, 3),
                            'source': s(row.get('source')), 'note': s(row.get('note'))})
    if cv['riskiest'] and cv['riskiest'] not in seen: problem(f'{path.name}: riskiest box {cv["riskiest"]} is not in the Boxes table')
    for k in (LEAN if lean else 'JPGSRC'):
        if not any(b['kind'] == k for b in cv['boxes']): problem(f'{path.name}: no {k} box')
    if lean: read_themes(path, cv, body)
    else: cv['fit'] = [{'pair': s(r.get('pair')), 'read': s(r.get('read'))} for r in table(body, 'Fit, read by pair')]
    facts = table(body, 'Facts — where the data says the model breaks' if lean else 'Facts — where the data says fit breaks')
    cv['facts'] = [{'n': s(r.get('number')), 't': s(r.get('what it says')), 'src': s(r.get('source'))} for r in facts]
    cv['changes'] = [{'version': s(r.get('version')), 'date': s(r.get('date')), 'what': s(r.get('what changed'))} for r in table(body, 'Changes')]
    m = re.search(r'^## Notes\s*$(.*?)(?=^## |\Z)', body, re.M | re.S)
    if m: cv['notes'] = [l[2:].strip() for l in m.group(1).split('\n') if l.startswith('- ')]
    return cv

def read_themes(path, cv, body):
    """The Lean Canvas's '## Read by theme' table: 'Desirability (PR, CS, CO2 …)' names whole blocks or single
    rows. Every row gets exactly one theme, so the page can read the canvas by theme."""
    rows = {b['id']: b for b in cv['boxes']}
    for r in table(body, 'Read by theme'):
        m = re.match(r'^(\w+)\s*\(([^)]*)\)$', s(r.get('theme')))
        theme = m.group(1).lower() if m else ''
        if theme not in THEME: problem(f'{path.name}: Read by theme "{s(r.get("theme"))}" should look like "Viability (RS, CO1)"'); continue
        for tok in (t.strip() for t in m.group(2).split(',') if t.strip()):
            if tok not in LEAN and tok not in rows: problem(f'{path.name}: Read by theme names "{tok}", which is neither a block nor a row'); continue
            ids = [b['id'] for b in cv['boxes'] if b['kind'] == tok] if tok in LEAN else [tok]
            for i in ids:
                if rows[i]['theme']: problem(f'{path.name}: {i} is read under both {rows[i]["theme"]} and {theme}')
                rows[i]['theme'] = theme
        cv['themes'].append({'theme': theme, 'read': s(r.get('read'))})
    for b in cv['boxes']:
        if not b['theme']: problem(f'{path.name}: {b["id"]} is in no theme of the Read by theme table')

def coverage(cv, zoom, exps):
    """Per Lean Canvas block: its rows, the rows read (Evidence 2+), the rows a planned or running test aims at,
    and whether the block is covered: one of its rows read, or, for Problem and Solution, one of the
    zoom-in canvas's boxes that detail it. A planned or running test does not count: only evidence covers a block."""
    active = {b['id'] for e in exps if e['status'] in ('planned', 'running') for b in e['boxes'] if b['role'] == 'main'}
    out = []
    for k, (name, _) in LEAN.items():
        rows = [b for b in cv['boxes'] if b['kind'] == k]
        read = [b['id'] for b in rows if (b['evidence'] or 0) >= READ]
        via = [b['id'] for b in (zoom['boxes'] if zoom else []) if b['kind'] in ZOOM.get(k, '') and (b['evidence'] or 0) >= READ]
        out.append({'block': k, 'name': name, 'rows': len(rows), 'read': read, 'via': via,
                    'testing': [b['id'] for b in rows if b['id'] in active], 'covered': bool(read or via)})
    return out

# ---------- events (the "since last review" feed) ----------
def events(exps):
    ev = []
    for e in exps:
        if e['windowStart']: ev.append({'date': e['windowStart'][:10], 'exp': e['id'], 'what': 'window opened (sent)'})
        if e['windowEnd'] and e['status'] != 'running': ev.append({'date': e['windowEnd'][:10], 'exp': e['id'], 'what': 'window closed'})
        if e['decided']: ev.append({'date': e['decided'][:10], 'exp': e['id'], 'what': f'logged: {DECISION_TEXT[e["decision"]]}'})
        if e['held']: ev.append({'date': e['held'][:10], 'exp': e['id'], 'what': 'put on hold'})
    try:
        out = subprocess.run(['git', 'log', '--since=60 days', '--format=%H%x1f%ad%x1f%s', '--date=short', '--name-only', '--', 'experiments'],
                             cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=15).stdout
        for block in out.strip().split('\n\n'):
            lines = [l for l in block.split('\n') if l]
            if not lines or '\x1f' not in lines[0]: continue
            _, date, subject = lines[0].split('\x1f')
            ids = sorted({l.split('/')[1][:4] for l in lines[1:] if l.startswith('experiments/') and re.match(r'experiments/\d{4}-', l)})
            ev.append({'date': date, 'exp': ', '.join(ids) if ids else '', 'what': 'commit: ' + subject})
    except Exception:
        pass
    ev.sort(key=lambda x: (x['date'], x['exp']), reverse=True)
    return ev

# ---------- PROGRESS.md ----------
def write_progress(exps, canvases, now):
    files = ' and '.join(f'`canvas/{c["id"]}.md`' for c in canvases)
    L = ['# 📊 Experiment Board', '',
         'The single source of truth. Check here before starting anything new.', '',
         f'> **Generated** by `dashboard/build_data.py` on {now[:16].replace("T", " ")} from the header at the top of each',
         '> experiment\'s `test-card.md`. **Edit the card, not this file.** Corrections to the board are recorded in',
         f'> `BOARD-HISTORY.md`; the canvases are {files}; the method library is `METHODS.md`.', '',
         '| ID | Hypothesis (short) | Theme | Method | Boxes | Bar → Result | In | Out | Status | Decision |',
         '|----|---------------------|-------|--------|-------|--------------|----|-----|--------|----------|']
    for e in exps:
        boxes = ', '.join(('≈' if b['role'] == 'closest' else '') + b['id'] for b in e['boxes'])
        bar = e['bar'] + (' → **' + e['result'] + '**' if e['result'] else '')
        L.append(f"| {e['id']} | {e['title']} | {e['theme'].capitalize()} | {e['method']} | {boxes} | {bar} | {e['effort']} | {e['evidence']} | {STATUS_TEXT[e['status']]} | {DECISION_TEXT[e['decision']]} |")
    L += ['',
          '**Status values:** Planned → Running → Done (or **On hold ⏸️** — paused with a reason, resumes to Running)',
          '**Decision values (once Done):** Persevere ✅ / Pivot 🔄 / Kill ❌',
          '**In / Out:** effort to run (1–5) / strength of the evidence it gives (1–5). **Boxes:** the canvas boxes it tests (one letter: VP-A; two letters: LC-A); ≈ means the nearest box, not an exact match.', '',
          '## 📝 Status notes (one line each — details live in the experiment folder)',
          '| ID | Where we are | Details |', '|----|--------------|---------|']
    for e in exps:
        detail = f"`{e['folder']}/{e['learningCard'] or e['testCard']}`"
        L.append(f"| {e['id']} | {STATUS_TEXT[e['status']]}{', ' + DECISION_TEXT[e['decision']] if e['decision'] != 'none' else ''} — {e['note']} | {detail} |")
    L += ['', '**History:** board-level corrections and the board\'s older standing notes are in `BOARD-HISTORY.md`.', '']
    (EXP / 'PROGRESS.md').write_text('\n'.join(L), encoding='utf-8')

# ---------- main ----------
def main():
    names = method_names()
    exps = load_experiments(names)
    canvases = [c for c in (load_canvas(f) for f in sorted((EXP / 'canvas').glob('*.md'))) if c]
    canvases.sort(key=lambda c: list(ID_RE).index(c['kind']))   # the value proposition canvas first: the page reads row 0
    for k in ID_RE:
        n = sum(c['kind'] == k for c in canvases)
        if n > 1: problem(f'{n} canvases of kind {k} under experiments/canvas/; there is one of each')
    if not any(c['kind'] == 'value-proposition' for c in canvases): problem('no value-proposition canvas (VP-A) with a header under experiments/canvas/')
    by_name = {c['name']: c for c in canvases}
    for c in canvases:
        if c['zoomIn'] and c['zoomIn'] not in by_name: problem(f'{c["id"]}.md: zoom_in "{c["zoomIn"]}" is not a canvas')
        if c['kind'] == 'lean-canvas': c['coverage'] = coverage(c, by_name.get(c['zoomIn']), exps)
    known = {b['id'] for c in canvases for b in c['boxes']}
    for e in exps:
        for b in e['boxes']:
            if b['id'] not in known: problem(f'{e["id"]}: box {b["id"]} is not in any canvas under experiments/canvas/')
    now = datetime.datetime.now(TZ).isoformat(timespec='seconds')
    for p in problems: print('PROBLEM:', p)
    if problems: sys.exit(1)
    write_progress(exps, canvases, now)
    ev = events(exps)
    writes = [{'collection': 'board', 'doc_id': 'main', 'data': {
        'syncedAt': now, 'experiments': exps, 'canvas': canvases[0], 'canvases': canvases, 'events': ev,
        'repo': GITHUB, 'methodsUrl': GITHUB + 'experiments/METHODS.md' if GITHUB else '', 'config': CONFIG}}]
    for e in exps:
        d = EXP / e['folder']
        doc = {'id': e['id'], 'folder': e['folder'],
               'testCard': {'file': e['testCard'], 'markdown': front_matter(d / e['testCard'])[1], 'updatedAt': ts(d / e['testCard'])},
               'learningCard': ({'file': e['learningCard'], 'markdown': read(d / e['learningCard']), 'updatedAt': ts(d / e['learningCard'])}
                                if e['learningCard'] else None),
               'files': [{'name': f, 'url': e['url'] + '/' + f if e['url'] else ''} for f in e['files']]}
        writes.append({'collection': 'cards', 'doc_id': e['id'], 'data': doc})
    out = ROOT / 'dashboard' / 'sync-bundle.json'
    out.write_text(json.dumps({'generatedAt': now, 'writes': writes}, ensure_ascii=False), encoding='utf-8')
    for c in canvases:
        cov = f" | {sum(b['covered'] for b in c['coverage'])} of {len(c['coverage'])} blocks covered" if c['coverage'] else ''
        print('canvas:', c['name'], 'v' + str(c['version']), f"({c['kind']}) |", len(c['boxes']), 'boxes' + cov)
    print('experiments:', len(exps), '|', len(ev), 'events')
    print('bundle KB:', round(out.stat().st_size / 1024, 1), '| writes:', len(writes), '| PROGRESS.md rewritten')
    for e in exps:
        print(e['id'], e['status'].ljust(7), e['decision'].ljust(9), e['method'], '|', [b['id'] for b in e['boxes']], '|', e['result'])

if __name__ == '__main__':
    main()
