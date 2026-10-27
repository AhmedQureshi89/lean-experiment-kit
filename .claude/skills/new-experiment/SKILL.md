---
name: new-experiment
description: Start a new experiment when the founder says "test the idea that X" - allocate the next number, create the folder, fill the test card with its structured header, then sync the dashboard (which regenerates the board).
---

Create one experiment for the idea the founder gave. One hypothesis, one test, one metric. A
hypothesis with "and" in it is two experiments: say so and ask which one first.

1. **Number and folder.** The next ID is the highest `NNNN-` folder under `experiments/` + 1, four
   digits. Create `experiments/NNNN-<slug>/` (slug: 2-4 words, kebab-case).
2. **Who it is about.** Read `customer-segments.md` and name the segment (Seg N) in the hypothesis.
   If no real customer has been placed in a segment yet, write "nobody tagged to a segment" in the
   header's `segment` rather than guessing.
3. **Test card.** Copy `experiments/_template/test-card.md` into the folder as `test-card.md` and
   fill both parts:
   - **The header** (the YAML block between the `---` lines; the dashboard and the board are built
     from it): `id`, `title` (one line, no version notes), `segment`, `theme`, `method` written
     exactly as `#NN Name` from `experiments/METHODS.md` or `Custom (closest: #NN Name)`, `boxes`
     (box IDs from either canvas: `experiments/canvas/VP-A.md` for the value side, one letter, J1,
     C4; `experiments/canvas/LC-A.md` for the business model, two letters, CH2, RS1; prefix `~` for
     the nearest box when there is no exact one), `status: planned`, `decision: none`, `bar` (the
     number that makes it a win), `result: not started`, `effort` and `evidence` (1-5),
     `waiting_on` (usually "Your go to start"), `note` (one line: where we are).
   - **Which canvas.** A job, pain, gain, product, pain reliever or gain creator is a `VP-A` box.
     Reach, retention, price, cost, a partner or supplier, a regulator, a key metric or an unfair
     advantage is an `LC-A` row. `theme` stays the card's own call: the Lean Canvas fixes no theme
     by block.
   - **The card body**: Hypothesis ("We believe that ...", segment named), Test, Metric, Criteria,
     and why this is the cheapest believable test. Prefer cheap Discovery methods (#1 Customer
     Interview, #12 Link Tracking, #13 Feature Stub, #14 404 Test) unless the idea is already
     de-risked. If the test contacts people, add a "Before going live" checklist (per-person
     tracking, test and internal accounts excluded, usable addresses, a pool not used by an earlier
     experiment). Contact lists go in a CSV in the folder, never in the card: every `.md` file is
     synced to the dashboard.
4. **How we measure.** Fill the card's "How we measure" table before anything else is planned
   around the test: for each source the test uses (the founder's own tools: an email service, a
   database, web analytics, a form, interview notes), what it answers, the exact event, tag, filter
   or query, whether the count is per person or overall, the baseline in a normal week, and the
   dashboard dataset it becomes (`live-NNNN` when it is a live query). If a connector for that tool
   is available in this session, check each source once now: the query runs, the events exist.
   Set `sources:` in the header to the sources the table uses.
5. **Canvas.** If the box the test attacks is not in the canvas it belongs to (step 3), add a row
   for it there (raise `version`, set `date`, add a Changes line). A new `LC-A` row also goes into
   one theme of that file's "Read by theme" table, or the build stops with a `PROBLEM:` line. Do not
   edit `PROGRESS.md`: it is generated.
6. **Sync.** Run `/sync-dashboard`. The build fails with a `PROBLEM:` line if the header is wrong.
7. **Report to the founder** in plain language: the hypothesis, the method and why it is the
   cheapest believable test, the bar, and what is their call before it starts (usually: the go).
