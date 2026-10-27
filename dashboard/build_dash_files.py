#!/usr/bin/env python3
"""Turns dashboard/sync-bundle.json into the data files the Claude Dashboard reads, under dashboard/out/:
  experiments.json   one row per experiment (header fields, flat, plus the current card texts)
  canvas.json        one row per box of every canvas (VP-A first; `canvas`, `block` and `theme` say where it sits)
  canvas-meta.json   one row per canvas header, VP-A first (the page reads row 0 as the value proposition canvas)
  events.json        one row per dated change
and index.doc.json = {"text": <dashboard/dash-index.html>} for the page document, with kit.config.json
(business name, time zone, weekend, week start, repo link) written into it.
Run after build_data.py:  python dashboard/build_dash_files.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'dashboard' / 'out'
OUT.mkdir(exist_ok=True)
bundle = json.loads((ROOT / 'dashboard' / 'sync-bundle.json').read_text(encoding='utf-8'))
board = next(w['data'] for w in bundle['writes'] if w['collection'] == 'board')
cards = {w['doc_id']: w['data'] for w in bundle['writes'] if w['collection'] == 'cards'}

def dump(name, rows):
    p = OUT / name
    p.write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8')
    print(name, len(rows), 'rows,', round(p.stat().st_size / 1024, 1), 'KB')

exps = []
for e in board['experiments']:
    c = cards.get(e['id'], {})
    exps.append({
        'id': e['id'], 'title': e['title'], 'segment': e['segment'], 'theme': e['theme'],
        'method': e['method'], 'method_note': e['methodNote'],
        'boxes': ', '.join(('~' if b['role'] == 'closest' else '') + b['id'] for b in e['boxes']),
        'status': e['status'], 'decision': e['decision'], 'bar': e['bar'], 'result': e['result'],
        'read_at': e.get('readAt', ''), 'score_now': e.get('scoreNow'), 'score_target': e.get('scoreTarget'),
        'score_label': e.get('scoreLabel', ''), 'score_caveat': e.get('scoreCaveat', ''),
        # the tiles flattened into one cell, because a dashboard dataset holds no lists: n and label
        # joined by ·, the tiles by |, neither of which a tile may hold (build_data.SCORE_SEPS)
        'score_parts': '|'.join(p['n'] + '·' + p['label'] for p in (e.get('scoreParts') or [])),
        'bar_met': e['barMet'], 'window_start': e['windowStart'], 'window_end': e['windowEnd'],
        'decided': e['decided'], 'held': e['held'], 'effort': e['effort'], 'evidence': e['evidence'],
        'waiting_on': e['waitingOn'], 'next': e['next'], 'note': e['note'], 'folder': e['folder'], 'url': e['url'],
        'live_dataset': e.get('liveDataset', ''),
        'files': ', '.join(e['files']),
        'test_card_text': (c.get('testCard') or {}).get('markdown', ''),
        'learning_card_text': (c.get('learningCard') or {}).get('markdown', '') if c.get('learningCard') else '',
    })
dump('experiments.json', exps)

canvases = board.get('canvases') or [board['canvas']]
dump('canvas.json', [{'id': b['id'], 'canvas': cv['name'], 'block': b.get('block', ''), 'theme': b.get('theme', ''),
                      'side': b['side'], 'kind': b['kind'], 'text': b['text'], 'tag': b['tag'], 'tag_note': b['tagNote'],
                      'matters': b['matters'], 'evidence': b['evidence'], 'source': b['source'], 'note': b['note']}
                     for cv in canvases for b in cv['boxes']])
meta = []
for cv in canvases:
    fit = {f['pair']: f['read'] for f in cv['fit']}
    themes = {t['theme']: t['read'] for t in cv.get('themes', [])}
    cov = cv.get('coverage', [])
    meta.append({'name': cv['name'], 'kind': cv.get('kind', 'value-proposition'), 'zoom_in': cv.get('zoomIn', ''),
                 'version': cv['version'], 'date': cv['date'], 'title': cv['title'], 'segment': cv['segment'],
                 'summary': cv['summary'], 'riskiest': cv['riskiest'], 'riskiest_why': cv['riskiestWhy'],
                 'fit_jobs': fit.get('Jobs ⇄ Products and services', ''), 'fit_pains': fit.get('Pains ⇄ Pain relievers', ''),
                 'fit_gains': fit.get('Gains ⇄ Gain creators', ''),
                 'theme_desirability': themes.get('desirability', ''), 'theme_feasibility': themes.get('feasibility', ''),
                 'theme_viability': themes.get('viability', ''), 'boxes': len(cv['boxes']),
                 'blocks_covered': sum(c['covered'] for c in cov), 'blocks_total': len(cov),
                 'covered': ', '.join(c['block'] for c in cov if c['covered']),
                 'not_covered': ', '.join(c['block'] for c in cov if not c['covered'])})
dump('canvas-meta.json', meta)
dump('events.json', board['events'])
page = (ROOT / 'dashboard' / 'dash-index.html').read_text(encoding='utf-8')
# The page cannot read the repo, so the settings it needs travel inside it: the placeholder object in
# dash-index.html is replaced by the config's page-facing keys.
cfg = board.get('config') or {}
page_cfg = {k: cfg.get(k) for k in ('business', 'timezone', 'utc_offset', 'weekend', 'week_starts', 'repo_url')}
marker = '/*KIT_CONFIG*/'
if marker not in page: raise SystemExit('PROBLEM: dash-index.html has lost its /*KIT_CONFIG*/ marker')
head, _, rest = page.partition(marker)
page = head + json.dumps(page_cfg, ensure_ascii=False) + rest[rest.index(';'):]
(OUT / 'index.doc.json').write_text(json.dumps({'text': page}, ensure_ascii=False), encoding='utf-8')
print('index.doc.json', round(len(page) / 1024, 1), 'KB of page')
