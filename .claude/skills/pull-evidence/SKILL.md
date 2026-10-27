---
name: pull-evidence
description: Pull the current numbers for a Running experiment from the sources its test card names and append a dated entry to its daily-evidence-log.md, compared with the bar. Reads only; never decides, never sends. Use when the founder says "pull the numbers" or during a measurement window.
---

Pull the evidence for experiment NNNN (the argument). This is a read, not a decision: the learning
card and the board decision belong to `/log-experiment`, and only after the window closes.

## Rules
- Exclude test and internal accounts from every count. The test card names them; if it does not,
  ask the founder once and write the answer into the card.
- Say when a window overlaps the weekend (`weekend` in `kit.config.json`).
- Personal data (email addresses, phone numbers, names) never goes into a `.md` file: every `.md`
  syncs to the dashboard. Refer to people by count or by an internal id.
- An interim read is labelled interim. A read after the window closes is labelled final, and still
  makes no decision.
- Without per-person tracking the count covers the whole site or product, not the people the test
  reached. Say so.
- Read only. Never run a query that changes data, and never send anything.

## Steps
1. **Context.** Read `experiments/NNNN-*/test-card.md`: the metric, the window, the bar, the
   exclusions, and the "How we measure" table, which names each source and the exact query, event
   or tag. Read the last entry of `daily-evidence-log.md` so this entry continues it (reuse its
   query when it has one).
2. **Read each source the table names**, with whatever this session can reach:
   - a connected tool (a database, an email service, web analytics) through its connector: load it
     with `ToolSearch`, run the exact query or filter from the card, SELECT only;
   - a script in the repo the card names, run as the card writes it;
   - numbers the founder pastes in chat (interviews, a form's export, a payment page).
   If a source cannot be reached, say which and why, and write the entry with what you have.
   On the first pull for an experiment, write the exact query into the log entry so later pulls
   reuse it.
3. **Write the entry.** Append to `experiments/NNNN-*/daily-evidence-log.md` (create it if missing):
   a heading with the date and time, the window and how much of it has elapsed, a table of the
   counts, the count against the bar ("N of M needed"), interim or final, the caveats, and the
   queries used.
4. **Update the card header** so the dashboard shows the read. `result` stays the record in words
   (the whole read in one sentence), and six fields beside it are what the dashboard draws as a
   scoreboard, so fill them in the same edit:

   | Field | What goes in it |
   |---|---|
   | `read_at` | when this read was taken, ISO with the `utc_offset` from `kit.config.json`. **Required while the card is running**: `build_data.py` refuses to build without it. |
   | `score_now` | the one count that answers the bar, as a plain number |
   | `score_target` | the bar as a plain number, so the page can draw how far there is left to go |
   | `score_label` | what those two numbers count, in a few words (`"visitors who clicked Subscribe"`) |
   | `score_parts` | the counts behind it, each `{ n: <number or short string>, label: "what it counts" }`. At most 12 characters in `n`, never a `\|` or a `·`. Leave out any count the page already shows live (`live_dataset`). |
   | `score_caveat` | one line: what not to trust about this read |

   `score_now` and `score_target` must be comparable: where the bar is a share, convert it to a head
   count. Where a read has no number against the bar yet, leave the `score_*` fields empty and still
   set `read_at`. Check `status` matches reality (`running` while the window is open; `done` only
   after a learning card, which is `/log-experiment`'s job). Set `window_start` and `window_end` if
   they are missing.
5. **Sync.** Run `/sync-dashboard`.
6. **Tell the founder** in three lines: the count against the bar, interim or final, and when the
   next read is due. If the window has closed, say that `/log-experiment NNNN` is the next step and
   wait for their word.

## A live count on the dashboard (optional)
When a source has a connector the Dashboard can query by itself (for example a SQL database), the
page can show the count fresh on every open: write the window-count query, run it once, then
`ArtifactData` `set` collection `datasets`, doc `live-NNNN` on the dashboard URL with
`{title, description, source: {kind: "query", connector: "<connector name>", tool: "<its query
tool>", args: {<the tool's arguments, with the query as run>}}}`, and put `live_dataset: live-NNNN`
in the card header. Every column of the query's first row becomes a tile on the running card.
