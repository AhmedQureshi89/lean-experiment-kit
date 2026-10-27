---
id: "NNNN"
title: One line, the claim in plain words, no version notes
segment: Seg N name, or "nobody tagged to a segment"
theme: desirability            # desirability | feasibility | viability
method: "#NN Name"              # exactly as in METHODS.md, or "Custom (closest: #NN Name)"
method_note: ""                 # optional: how it differs from the book's method
boxes: ["J1"]                   # box IDs from canvas/VP-A.md (J1, C4) or canvas/LC-A.md (CH2, RS1); "~C4" = nearest box, not exact
sources: [email, database, analytics]   # the sources the "How we measure" table uses (name your own tools)
status: planned                 # planned | running | hold | done
decision: none                  # none | persevere | pivot | kill  (only once done)
bar: the number that makes it a win, with its window
result: not started             # the whole read in words, the record; set by /pull-evidence (interim) and /log-experiment (final)
read_at: ""                     # "2026-10-22T09:04+00:00" (your utc_offset), when that read was taken; required once status is running
score_now: null                 # the one count that answers the bar, as a number
score_target: null              # the bar as a number, so the dashboard can draw how far there is to go
score_label: ""                 # what those two numbers count, e.g. "attributed signups"
score_parts: []                 # the counts behind it, each { n: <number or short string>, label: "what it counts" }
score_caveat: ""                # one line: what not to trust about this read
bar_met: null                   # true | false | null
window_start: ""                # "2026-10-07T18:43+00:00", set when the test goes live
window_end: ""                  # "2026-10-09T18:43+00:00"
decided: ""                     # "YYYY-MM-DD", set by /log-experiment
effort: 2                       # 1-5, how hard to run
evidence: 3                     # 1-5, how strong the result will be
waiting_on: "Your go to start"   # what waits on you; empty when nothing does
next: ""                        # the next experiment's ID, once it exists
live_dataset: ""                # set at send time: the dashboard dataset holding the live window count (live-NNNN)
note: One line, where we are. Becomes the board's status note.
---
# Test Card

**Experiment ID:**
**Date:**
**Theme:** Desirability / Feasibility / Viability
**Method (from METHODS.md):**
**Canvas box tested:** canvas and version · box ID(s), e.g. VP-A v3 · J1 or LC-A v4 · RS1 · tag now (❓ Assumption / 🟡 Signal / ✅ Seen / 🟢 Live / ⚪ Untested / 🔴 Gap). The header's `boxes:` is the link; the canvas does not repeat it.

- **Hypothesis:** We believe that …
- **Test:** To verify that, we will …
- **Metric:** And measure …
- **Criteria:** We are right if …

**Input (effort, 1–5):**
**Output (evidence strength, 1–5):**

## How we measure (fill before anything goes live)

| Source | What it answers | Exactly how (event, tag, filter or query) | On the dashboard as |
|---|---|---|---|
| e.g. your email tool | sent, delivered, opened, clicked, per batch | the tag or campaign name every send in this test carries | `live-NNNN-email` |
| e.g. your database | who did the thing the bar counts, after the test started; test and internal accounts excluded | the query, written out here and run once before the test starts | `live-NNNN` |
| e.g. your web analytics | visits and clicks on the page the test points to | the event names and the campaign property; confirm they exist first | `live-NNNN-web` |

Delete the rows you do not use. Per person or overall? Say which. Baseline: what these numbers look like in a normal week.
