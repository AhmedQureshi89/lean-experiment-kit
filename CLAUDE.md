# CLAUDE.md — the experiment loop

This repo runs business-idea experiments with the *Testing Business Ideas* method (David J. Bland and
Alexander Osterwalder). One founder, small steps, fast loops. The founder makes the decisions; Claude
runs the loop and keeps the record.

Settings live in `kit.config.json`: the business name, time zone (`timezone`, an IANA name such as
`Europe/London`, and `utc_offset`, such as `+01:00`), the weekend days, the day the week starts, the
GitHub link and the dashboard link. Use the configured offset in every date the cards hold.

## First run
If `kit.config.json`'s `business` ends with `(example)`, the kit has not been set up yet and
everything in it is the made-up Bean Box example. On the founder's first message, whatever it says,
tell them so in one line and offer two starts: `/tour` (see how the loop works on the example, about
five minutes) or `/get-started` (answer a few questions; Claude sets up their own business, about fifteen
minutes). Do not run `/new-experiment`, `/pull-evidence` or `/log-experiment` on the example
business unless they ask to try one on it.

## The loop (repeats every time)
1. **Hypothesize**: state a belief as "We believe that…"
2. **Experiment**: design and run the cheapest test that gives real evidence
3. **Learn**: read the evidence honestly
4. **Decide**: persevere ✅ / pivot 🔄 / kill ❌
5. **Manage**: keep the board and the dashboard current at all times

## Folder layout
```
kit.config.json          ← business name, time zone, weekend, links
customer-segments.md     ← who the customers are (Seg 1, Seg 2 …)
experiments/
  PROGRESS.md            ← the board, GENERATED from the card headers by dashboard/build_data.py.
                            Never hand-edit it; edit the card.
  BOARD-HISTORY.md       ← corrections to the board, word for word
  METHODS.md             ← the 44 method names and numbers, for naming a test
  _template/             ← test-card.md (with the header) and learning-card.md to copy
  canvas/VP-A.md         ← the Value Proposition Canvas: a header and one table, one row per box,
                            with Matters (1–3) and Evidence (0–3) scores; versioned in place
  canvas/LC-A.md         ← the Lean Canvas: the whole business model in nine blocks, the same table
                            and scores, two-letter IDs (CH2, RS1). VP-A details its Problem and Solution
  NNNN-<slug>/           ← one folder per experiment: test-card.md (its YAML header is the record),
                            learning-card.md, run-log.md, daily-evidence-log.md, contact lists (CSV only)
dashboard/               ← build_data.py (cards → board and bundle), build_dash_files.py (bundle → the
                            dashboard's data files), dash-index.html (the dashboard page), check_sync.py
                            (the Stop hook) and mark_synced.py
.claude/skills/          ← the procedures below, one slash command each
docs/WALKTHROUGH.md      ← one experiment from idea to decision, for a founder reading on GitHub
```

## The card header is the record
Every `test-card.md` starts with a YAML block: id, title, segment, theme, method, boxes, status,
decision, bar, result, effort, evidence, note, plus window and date fields (see
`_template/test-card.md`). `result` is the whole read in one sentence. Beside it, six fields say which
of its numbers the dashboard draws as the scoreboard: `read_at` (required while a card is running),
`score_now`, `score_target`, `score_label`, `score_parts` and `score_caveat` (`/pull-evidence` step 4
defines them). `build_data.py` validates the header (status and decision values, method names against
`METHODS.md`, box IDs against the two canvases: one letter for `VP-A`, two for `LC-A`) and refuses to
build on a `PROBLEM:` line. One fact lives in one place: status and result in the header, the reading
in the cards, a box's tag and scores in its canvas table.

## Procedures (slash commands: follow the skill, do not re-derive the steps)
| When the founder says | Run | What it does |
|---|---|---|
| "set me up" / a fresh copy | `/get-started` | the first run: questions about the business, config, segments and both canvases written, the example removed, the dashboard created, one first test proposed |
| "show me how this works" | `/tour` | six stops through a working loop: the example until set up, then the founder's own files |
| "test the idea that X" | `/new-experiment` | next number, folder, test card, canvas link, sync |
| "pull the numbers" / an experiment is Running | `/pull-evidence NNNN` | reads the sources the card names → a dated entry in the daily evidence log, compared with the bar |
| "log NNNN" / shares a result | `/log-experiment NNNN` | learning card, header done + decision, canvas box, one next hypothesis, sync |
| "sync the dashboard" | `/sync-dashboard` | builds the board, uploads the data files, creates the dashboard on the first run |

The Stop hook in `.claude/settings.json` runs `dashboard/check_sync.py`: when any
`experiments/**/*.md` is newer than the last sync, Claude is asked to sync before finishing, or to say
in one line why it is skipping.

## Standing rules
- **Nothing goes out without the founder's go**, for that batch, in that chat. Building a list, a page
  or a draft is fine; sending, posting or publishing is their word.
- **Personal data stays in CSV files only.** Never an email address, phone number or name list in a
  `.md` file: every `.md` syncs to the dashboard. `experiments/**/*.csv` is git-ignored on purpose.
- **Exclude test and internal accounts** from every contact list and every count.
- **Say when a window covers the weekend** (`weekend` in `kit.config.json`).
- **Never mark Persevere without a number.** Interim reads are reads, not decisions; the learning card
  waits for the window to close.
- **A Lean Canvas block is covered only with evidence**: a row at Evidence 2 or more. A planned or
  running test does not count.
- **One hypothesis at a time.** After a Pivot or Kill, propose exactly one next hypothesis.
- **Every test card plans its measurement before anything goes live**: a "How we measure" table
  naming, for each source, what it answers and the exact event, tag, filter or query. A card without
  it is not ready. `sources:` in the header lists the ones used.

## Style rules
- One experiment = one small, falsifiable claim. A hypothesis with "and" in it gets split into two.
- Pick the cheapest experiment that still gives believable evidence. Prefer Discovery methods
  (#1 Customer Interview, #12 Link Tracking, #13 Feature Stub, #14 404 Test) over Validation ones
  (#35 Simple Landing Page is cheap but counts as Validation; #36 Crowdfunding, #38 Presale).
  Write the method as `#NN Name` exactly as in `METHODS.md`; if not in the 44, `Custom (closest: #NN Name)`.
- Priority order for new hypotheses: **Desirability → Feasibility → Viability**, unless the founder says otherwise.
- Replies to the founder stay short, plain and broken into small next steps.

## Customer segments
`customer-segments.md` lists the working segments (Seg 1, Seg 2 …). Name the segment in every
hypothesis, in the choice of who to test on, and when reading a result. Do not assume a real customer
belongs to a segment unless the record says so.
