---
name: get-started
description: The kit's first run. Use when the founder types /get-started or says "set me up", "how do I start", "onboard me", or opens a kit that still holds the example business - a short welcome, an optional tour, a few questions about their business, then their own config, segments and two canvases written, the example removed, a clean build, the dashboard created, and one first test proposed.
---

Take a founder from a fresh copy of the kit to their first test card in about fifteen minutes. They
answer questions in plain words; Claude writes every file. Nothing is sent, posted or pushed.

**How to ask.** Two to four questions per message, never a form. Give a one-line example answer
for each, taken from the Bean Box example, so the founder sees the size of answer wanted. "I don't
know" is always a good answer: it becomes an honest `assumption` with Evidence 0. Use
`AskUserQuestion` where the answer is a choice (the weekend, tour or set up now); plain chat
otherwise. Never ask for a customer's name, email or phone number: contact lists come later, in a
CSV.

## 0. Where the kit is

Read `kit.config.json`, `customer-segments.md` and the two headers under `experiments/canvas/`.

- **Not set up yet:** `business` ends with `(example)`, or a canvas title ends with `(example)`.
  Go on.
- **Set up already:** neither holds. Say so in one line, offer `/tour` of their own files and the
  four phrases of step 9, and stop. `/get-started` never overwrites a founder's own canvases. To redo the
  setup, they say "start over", and only then go on.
- **Half done** (for example, the config is theirs but a canvas still says `(example)`): say which
  parts are done and go on from the first part that is not.

## 1. Welcome (one short message)

Say what the kit does in three lines, show the loop, say what they will have at the end, and ask
one question:

```
  Hypothesize → Experiment → Learn → Decide (persevere / pivot / kill)
       ↑                                            │
       └──────────── one next hypothesis ───────────┘
```

At the end they will have their business on two canvases, the riskiest belief picked out, a private
dashboard, and a first test ready for their go. Ask: **see how it works on the example first**
(`/tour`, about five minutes), or **set up my business now**? If they pick the tour, run `/tour`
and come back to step 2 when it ends.

## 2. The questions

Ask in this order, one group per message. Write down each answer with how they know it.

| Group | Ask | Becomes |
|---|---|---|
| **A. The business** | Its name. What it does, for whom, in one sentence. | `business`; the canvas titles and segment lines |
| **B. Where you work** | Your city or time zone. Which days are your weekend. Which day your week starts. A GitHub link for this repo, if you have pushed it (optional). | `timezone` (an IANA name such as `Europe/Berlin`), `utc_offset` (today's offset, such as `+01:00`), `weekend` (`["Sat", "Sun"]`), `week_starts`, `repo_url` |
| **C. Your first customers** | Who exactly you are building for first (Seg 1). Anyone after them (Seg 2, optional). For Seg 1: the job they are trying to get done, the worst part of it today, and what they wish happened instead. | `customer-segments.md`; VP-A `J`, `P`, `G`; LC-A `PR`, `CS` |
| **D. Your offer** | What you sell or will sell. How it takes away that worst part. How it gives them what they wish for. What is already built and working, and what is not. | VP-A `S`, `R`, `C`; LC-A `UV`, `SO` |
| **E. The model** | Where you will find these customers. How you will make money, and roughly what price. Your main costs. The one number that would tell you it is working. Anything that is hard for others to copy ("nothing yet" is fine). | LC-A `CH`, `RS`, `CO`, `KM`, `UA` |

After each answer, ask **"how do you know?"** once for the group, in plain words: *I've seen it in
real data or real customers told me* → `seen`; *one person said it, or I'm inferring it* →
`signal`; *it's my belief* → `assumption`. For the business side of VP-A (`S`, `R`, `C`) and LC-A
(`SO`, `CH`, `CO`, `KM`, `UA`) the tags are `live` (built and running), `untested` (exists or is
claimed, no proof it helps) and `gap` (missing).

## 3. Score it together

Show the rows as one table in chat, with your proposed **Matters** (1–3: how much the business
depends on it; 3 = if this is wrong, there is no business) and **Evidence** (0–3: 0 belief, 1 one
voice or a hint, 2 seen once in real data or tried once, 3 established). Explain the two scales in
one line each, then ask them to correct anything.

Be honest on their behalf: Evidence 2 or more only for something seen in real data or done once,
never for a strong feeling. Most rows of a new business are `assumption`, Evidence 0, and say so
kindly: that is what the experiments are for.

## 4. Confirm before writing

List what will change and ask for a go:

- `kit.config.json`: name, time zone, weekend, week start, repo link. A `dashboard_url` already
  there (from a tour that created the dashboard) is kept: the same dashboard is reused.
- `customer-segments.md`, `experiments/canvas/VP-A.md`, `experiments/canvas/LC-A.md`: rewritten
  with their answers, version 1.
- The example experiments `experiments/0001-work-from-home-interviews/` and
  `experiments/0002-subscription-mock-sale/` deleted. Only delete a folder whose test card is the
  Bean Box example; anything else is the founder's and stays. Git keeps the example if they want it
  back.

## 5. Write the files

Rewrite each file **in place**: keep every header key, the "How this file works" block, every `##`
heading and every table's header row exactly as they are, because the build and the dashboard read
them. Replace the rows. Remove the example banner (the first `>` block that says it is a made-up
example) and the "Example only" note.

- **`kit.config.json`**: the answers from group B. If they gave a city, choose its IANA zone and
  today's offset, and say which you chose.
- **`customer-segments.md`**: one row per segment (`Seg 1`, `Seg 2` …) with Evidence so far ("None
  yet" when it is belief). Keep the "Known limits" section.
- **`experiments/canvas/VP-A.md`**: header `version: 1`, `date` today, `title: <business> Value
  Proposition Canvas`, `segment` (Seg 1 in words), `summary` (two sentences: what is seen, what is
  belief), `riskiest` and `riskiest_why` (step 6). At least one row of each kind: `J`, `P`, `G`
  (customer side), `S`, `R`, `C` (business side), numbered `J1`, `J2` … The **Fit, read by pair**
  table gets one plain line for each of its three pairs. The **Facts** table keeps its header row
  and holds a row only for a real number they gave. **Changes**: `| 1 | <today> | First draft from
  the founder's answers in /get-started. |`
- **`experiments/canvas/LC-A.md`**: the same header keys (keep `kind: lean-canvas` and `zoom_in:
  VP-A`), `title: <business> Lean Canvas`. At least one row in every one of the nine blocks:
  `PR`, `CS`, `UV`, `SO`, `CH`, `RS`, `CO`, `KM`, `UA`. `PR1` is the problem in one line and `SO1`
  the solution in one line: the detail lives in VP-A. Keep the **Read by theme** table's three
  rows naming the blocks (`Desirability (PR, CS, UV)`, `Feasibility (SO, CH, UA)`, `Viability (RS,
  CO, KM)`), with one plain line each, so every row sits in one theme. Same Changes line.
- **Delete** the two example folders.
- Leave `experiments/PROGRESS.md` alone: the build writes it.

## 6. Pick the riskiest box

In each canvas, the riskiest row is the one with **Matters 3 and the lowest Evidence**. On a tie,
take the customer side first (Desirability before Feasibility before Viability), then the row
everything else depends on. Write it to `riskiest`, with `riskiest_why` in one or two plain
sentences. Tell the founder which rows you picked and why, and let them overrule you.

## 7. Build until clean

Run `python dashboard/build_data.py` (`python3` on a Mac). Each `PROBLEM:` line names the file and
the row: fix it and run again until the build prints the canvases with no `PROBLEM:` line. Do not
show the founder the problems you fixed unless one needs their answer.

## 8. The dashboard

Run `/sync-dashboard`. On the first run it creates the founder's private dashboard and writes its
link into `kit.config.json`; later it updates the same one. Tell them to approve the uploads when
asked, give them the link, and suggest they open it on their phone and keep it there. It is
private to them until they share it.

Then commit the setup, naming the files (never `git add -A`): `kit.config.json`,
`customer-segments.md`, `experiments/`. Message: `Set up the kit for <business>`. Push only if they
ask.

## 9. The first test, and the four phrases

Propose **exactly one** first hypothesis against the riskiest box, in the form "We believe that
<Seg 1> <the belief>", with the cheapest method that gives real evidence (usually `#1 Customer
Interview` for a pain or a job nobody has seen yet). Ask: "Shall I write the test card?" On a yes,
run `/new-experiment`.

End with the four things they will say from now on:

| Say | When |
|---|---|
| "test the idea that …" | you have a belief to test |
| "pull the numbers for 0001" | a test is running and you want today's count |
| "log 0001" | its window has closed and you are ready to decide |
| "sync the dashboard" | rarely: Claude does it at the end of each change |

And: `/tour` walks through their own files any time.
