---
name: tour
description: Walk the founder through how the kit works, one piece at a time - the loop, the two canvases, a test card, a running test's evidence log, a closed test's learning card, the board and the dashboard. Uses the Bean Box example until the kit is set up, then the founder's own files. Use when the founder types /tour or says "show me how this works", "walk me through it", "what is all this".
---

A guided look at a working loop, about five minutes. Six stops. At each stop: read the file, show
**a few real lines from it** (a header excerpt or three table rows, never the whole file), say in two
or three plain sentences what it is for, and name the phrase the founder says to Claude to make or
change it. Then ask "next?" and wait: they may have a question first. Keep each stop under fifteen
lines in chat.

**Which files.** If `kit.config.json`'s `business` ends with `(example)`, tour the Bean Box example
and say once, at the start, that it is a made-up coffee subscription. Otherwise tour the founder's
own files, and skip a stop with nothing to show yet (say so in one line: "no test has closed yet, so
there is no learning card to show").

## The stops

1. **The loop, and who does what.** Show the loop (hypothesize → experiment → learn → decide →
   one next hypothesis). The founder decides when a test goes live, whether a bar is right, and
   every persevere, pivot or kill. Claude writes the cards, reads the numbers and keeps the board
   and the dashboard current.
2. **The two canvases.** From `experiments/canvas/VP-A.md`, show the `J1`, `P1` and `G1` rows with
   their Tag, Matters and Evidence. Matters is how much the business depends on the box; Evidence is
   how much is known. The riskiest box (`riskiest` in the header) is high Matters, low Evidence:
   that is what to test next. Then one line on `LC-A.md`: the whole business model in nine blocks,
   and a block is only "covered" once a row reaches Evidence 2.
3. **A test card.** From the running experiment's `test-card.md` (in the example, `0002`), show the
   header lines `title`, `method`, `boxes`, `bar` and `status`, then the "How we measure" table's
   first row. One small claim, the cheapest believable method, a bar set before it starts, and the
   measurement planned before anything goes live. Phrase: "test the idea that …".
4. **While it runs.** From its `daily-evidence-log.md`, show the latest entry's first lines. A read
   is dated and compared with the bar, and an interim read never decides anything. Phrase: "pull
   the numbers for 0002".
5. **Closing a test.** From a closed experiment's `learning-card.md` (in the example, `0001`), show
   the observation, the decision and the canvas change. The result is read against the bar, the
   founder makes the call, the canvas box moves (in the example, `J1` from belief to `seen`,
   Evidence 2), and Claude proposes exactly one next hypothesis. Phrase: "log 0001".
6. **The board and the dashboard.** Show the first two rows of `experiments/PROGRESS.md`: it is
   built from the card headers and never edited by hand. The dashboard is a private page on
   claude.ai with four tabs: **Today** (what is running and what waits on the founder), **Board**,
   **Model** (the riskiest boxes and the assumptions map) and **Log**. If `kit.config.json` has a
   `dashboard_url`, give the link. If it is empty, offer to create it now with `/sync-dashboard`
   so they can see it on their phone; `/get-started` reuses the same dashboard later.

## The end

If the kit still holds the example, close with one line: "`/get-started` sets up your own business:
about fifteen minutes of questions, and Claude writes the files." If `/get-started` sent the founder here,
go back to its step 2.
