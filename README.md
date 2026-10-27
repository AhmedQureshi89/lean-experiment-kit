# Lean Experiment Kit

Run business-idea experiments with [Claude Code](https://claude.com/claude-code), one small test at a
time, and track the whole business model on a live dashboard you can read on your phone.

It follows the method in **_Testing Business Ideas_** by David J. Bland and Alexander Osterwalder.
You say *"test the idea that…"*, Claude writes the test card. You run the test. Claude reads the
numbers, writes what you learned, updates your canvases and keeps the dashboard current. You make
every decision.

```
  ┌────────────────┐    ┌──────────────┐    ┌──────────┐    ┌───────────────────────┐
  │ 1. Hypothesize │ →  │ 2. Experiment│ →  │ 3. Learn │ →  │ 4. Decide             │
  │ "We believe…"  │    │ cheapest     │    │ read the │    │ persevere / pivot /   │
  │ /new-experiment│    │ real test    │    │ numbers  │    │ kill  /log-experiment │
  └────────────────┘    └──────────────┘    └──────────┘    └───────────┬───────────┘
          ↑                                  /pull-evidence             │
          └────────────── one next hypothesis ──────────────────────────┘
                     5. Manage: the board and the dashboard stay current (/sync-dashboard)
```

It started as one solo founder's working setup for a real startup's experiments, with everything
specific to that business taken out. The example inside is a made-up coffee subscription, **Bean Box**, so the
board and the dashboard have something to show on day one.

## What you get

| Part | What it is |
|---|---|
| **Test cards** | One folder per experiment. Each card starts with a small YAML header (hypothesis, method, bar, result, status, decision) that is the record. |
| **Two canvases** | A Value Proposition Canvas (`VP-A.md`) and a Lean Canvas (`LC-A.md`). Every box has a tag and two scores: how much it **matters** (1–3) and how much **evidence** you have (0–3). |
| **The board** | `experiments/PROGRESS.md`, generated from the card headers. It is never edited by hand. |
| **A validator** | `dashboard/build_data.py` refuses to build when a header is wrong: an unknown method, a box that is in no canvas, a decision with no result. |
| **Four slash commands** | `/new-experiment`, `/pull-evidence`, `/log-experiment`, `/sync-dashboard`, in `.claude/skills/`. |
| **A dashboard** | A private Claude Dashboard on claude.ai. *Today* shows what is running and what waits on you. *Board* has a timeline and every card. *Model* shows the riskiest box of each canvas, the Lean Canvas and an assumptions map (matters × evidence). *Log* is what changed this week. |
| **Guard rails** | Contact lists stay in git-ignored CSV files. Nothing is sent without your go. No "persevere" without a number that clears the bar. One hypothesis at a time. |

## What you need

- **Claude Code** and a claude.ai account. The dashboard is a Claude Dashboard artifact, which is private to you until you share it.
- **Python 3.9+** with PyYAML: `python -m pip install pyyaml`
- **Git**, and a GitHub account if you want the dashboard to link to your cards.
- Optional: connectors for the tools your tests use (your database, email service or web analytics), so `/pull-evidence` can read the numbers itself. Without them, paste the numbers in chat.

## Start in five steps

1. **Get your own copy.** On GitHub, press **Use this template** → *Create a new repository*. Make
   it **private**, because your experiments are your business. Clone it.
2. **Set it up.** Edit `kit.config.json`: your business name, time zone (`"Europe/London"`, with
   `utc_offset` such as `"+01:00"`), your weekend days, the day your week starts, and your repo's
   GitHub link. Leave `dashboard_url` empty.
3. **Check it builds.** In the repo folder:
   ```
   python -m pip install pyyaml
   python dashboard/build_data.py
   ```
   It prints the canvases and experiments it found, or `PROBLEM:` lines that say what to fix. (On a
   Mac, use `python3`, and change `python` to `python3` in `.claude/settings.json` too.)
4. **Open Claude Code in the folder** and say *"sync the dashboard"*. On the first run Claude
   creates your dashboard, uploads the example and writes the link into `kit.config.json`. Approve
   the uploads when asked.
5. **Make it yours.** Rewrite the rows of `experiments/canvas/VP-A.md` and `LC-A.md` with your own
   beliefs (most will be `assumption` with Evidence 0, which is honest). Rewrite
   `customer-segments.md`. Delete the two example folders `experiments/0001-…` and `0002-…`. Then
   say *"test the idea that …"*.

> The canvases must keep at least one row of each kind (jobs, pains, gains, products, pain
> relievers, gain creators; and all nine Lean Canvas blocks), or the build stops and names the
> missing one. Replace rows rather than deleting them all.

## Using it day to day

| You say | Claude runs | What happens |
|---|---|---|
| "test the idea that people will pay for X" | `/new-experiment` | Picks the next number, writes the test card (the cheapest believable method, a bar, a *How we measure* table), links it to a canvas box, syncs. |
| "pull the numbers for 0003" | `/pull-evidence 0003` | Reads each source the card names, writes a dated entry, puts the count against the bar on the dashboard. Interim reads never decide anything. |
| "log 0003" | `/log-experiment 0003` | Once the window has closed: writes the learning card, records persevere, pivot or kill, moves the canvas box, proposes one next hypothesis. |
| "sync the dashboard" | `/sync-dashboard` | Rebuilds the board and pushes it. A Stop hook reminds Claude when the cards have changed since the last sync. |

You decide when a test goes live, whether a bar is right, and every persevere, pivot or kill.
Claude keeps the record.

## How the pieces fit

```
 experiments/NNNN-*/test-card.md  ─┐
 experiments/canvas/VP-A.md        ├─▶ build_data.py ──▶ PROGRESS.md (the board)
 experiments/canvas/LC-A.md       ─┘        │
 kit.config.json ───────────────────────────┤
                                            ▼
                                   build_dash_files.py ──▶ dashboard/out/*.json + the page
                                            │
                                            ▼
                         /sync-dashboard ──▶ your Claude Dashboard (private, on claude.ai)
```

Everything is plain Markdown and YAML in git. The dashboard is a view of the repo, never the
record. A running card can also name a live query (`live_dataset`), which the dashboard runs on every
open. See `.claude/skills/pull-evidence/SKILL.md`.

## The method list

`experiments/METHODS.md` lists the 44 methods of *Testing Business Ideas* by **number and name
only**, so every card names its method the same way. What each method is, when to use it and how far
to trust its result are in the book, and you should read it there. This project is not affiliated
with or endorsed by the authors, Wiley or Strategyzer.

## License

MIT. See `LICENSE`.
