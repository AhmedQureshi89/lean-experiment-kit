---
name: log-experiment
description: Close an experiment when the founder says "log NNNN" or shares its result - write the learning card, set the card header to done with the decision, update the canvas box, propose exactly one next hypothesis, sync the dashboard.
---

Log the result of experiment NNNN (the argument). Honest reading first, decision second.

1. **Context.** Read `experiments/NNNN-*/test-card.md` (the header, the bar and the How we measure
   table), and the `run-log.md` and `daily-evidence-log.md` if they exist.
2. **Final numbers.** If the measurement window has not closed, stop: write an interim entry
   through `/pull-evidence NNNN` instead and tell the founder when the final read is due. A learning
   card needs the closed window unless the founder explicitly says "log it now".
3. **Learning card.** Copy `experiments/_template/learning-card.md` into the folder and fill it:
   - Observation: what happened, with the numbers and any verbatim quotes (no personal data)
   - Bar: met / not met. People: N, test and internal accounts left out. Per person: matched or not
   - Insight: what it means, with the caveats (a weekend in the window, untracked links, small N)
   - Decision: Persevere only with a number that clears the bar; otherwise Pivot or Kill
   - What happened to the box: new tag and source for the canvas box row
4. **Header.** In the test card's header set `status: done`, `decision: persevere|pivot|kill`,
   `result` (the whole read in one sentence), the scoreboard fields `/pull-evidence` step 4 lists
   (`read_at`, `score_now`, `score_target`, `score_label`, `score_parts`, `score_caveat`) for the
   final read, `bar_met: true|false` (`null` when there was no usable read), `decided: "YYYY-MM-DD"`,
   `next` (the next experiment's ID, once it exists), clear `waiting_on`, and rewrite `note` (one
   line: the number against the bar and what comes next). If the learning card has a different file
   name, set `learning_card`. Do not edit `PROGRESS.md`: it is generated. If a board fact is
   *corrected* rather than updated, record the correction in `BOARD-HISTORY.md`.
5. **Canvas.** In the canvas the box belongs to (`experiments/canvas/VP-A.md` for one-letter IDs,
   `experiments/canvas/LC-A.md` for two-letter IDs) change the box's Tag, Evidence and Source cells,
   raise `version`, set `date`, and add a line under Changes. Do not copy the file. A Lean Canvas
   block counts as covered only once a row reaches Evidence 2.
6. **Next hypothesis.** If Pivot or Kill: propose exactly ONE next hypothesis, in the priority order
   Desirability -> Feasibility -> Viability, across both canvases (the dashboard's Model tab shows
   the riskiest box of each). Do not create its folder until the founder says to test it.
7. **Sync.** Run `/sync-dashboard`.
8. **Report to the founder**: the number against the bar, the decision and why, the one proposed
   next hypothesis, and what is their call.
