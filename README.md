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
| **Guided setup and a tour** | `/get-started` asks about your business and writes everything; `/tour` walks through a working loop. [The walkthrough](docs/WALKTHROUGH.md) shows one experiment from idea to decision. |
| **Four loop commands** | `/new-experiment`, `/pull-evidence`, `/log-experiment`, `/sync-dashboard`, in `.claude/skills/`. |
| **A dashboard** | A private Claude Dashboard on claude.ai. *Today* shows what is running and what waits on you. *Board* has a timeline and every card. *Model* shows the riskiest box of each canvas, the Lean Canvas and an assumptions map (matters × evidence). *Log* is what changed this week. |
| **Guard rails** | Contact lists stay in git-ignored CSV files. Nothing is sent without your go. No "persevere" without a number that clears the bar. One hypothesis at a time. |

## What you need

- **Claude Code** and a claude.ai account. The dashboard is a Claude Dashboard artifact, which is private to you until you share it.
- **Python 3.9+** with PyYAML: `python -m pip install pyyaml`
- **Git**, and a GitHub account if you want the dashboard to link to your cards.
- Optional: connectors for the tools your tests use (your database, email service or web analytics), so `/pull-evidence` can read the numbers itself. Without them, paste the numbers in chat.

## Get started

1. **Get your own copy.** On GitHub, press **Use this template** → *Create a new repository*. Make
   it **private**, because your experiments are your business. Clone it.
2. **Install the one package the build needs:** `python -m pip install pyyaml` (on a Mac,
   `python3`, and change `python` to `python3` in `.claude/settings.json` too).
3. **Open Claude Code in the folder and type `/get-started`.** That is the whole setup.

```
 /get-started  (about 15 minutes)
   ├─ welcome, and a 5-minute /tour of the example if you want it
   ├─ a few questions at a time: your business, where you work, your first customers,
   │  your offer, how you'll reach them and make money ("I don't know" is a good answer)
   ├─ you check the scores: how much each belief matters, how much you really know
   ├─ Claude writes your config, segments and two canvases, and removes the example
   ├─ it picks your riskiest belief and creates your private dashboard
   └─ it proposes your first test, and waits for your yes
```

New to the method? Type `/tour` first, or read **[the walkthrough](docs/WALKTHROUGH.md)**: one
experiment from idea to decision, with what you type and what you get back.

<details>
<summary>Set it up by hand instead</summary>

1. Edit `kit.config.json`: your business name, time zone (`"Europe/London"`, with `utc_offset`
   such as `"+01:00"`), your weekend days, the day your week starts, and your repo's GitHub link.
   Leave `dashboard_url` empty.
2. Rewrite the rows of `experiments/canvas/VP-A.md` and `LC-A.md` with your own beliefs (most will
   be `assumption` with Evidence 0, which is honest) and rewrite `customer-segments.md`. Delete the
   two example folders `experiments/0001-…` and `0002-…`.
3. Run `python dashboard/build_data.py`. It prints the canvases and experiments it found, or
   `PROBLEM:` lines that say what to fix. The canvases must keep at least one row of each kind
   (jobs, pains, gains, products, pain relievers, gain creators; and all nine Lean Canvas blocks).
4. In Claude Code, say *"sync the dashboard"*. On the first run Claude creates your dashboard and
   writes its link into `kit.config.json`. Approve the uploads when asked.

</details>

## Using it day to day

| You say | Claude runs | What happens |
|---|---|---|
| "show me how this works" | `/tour` | Six short stops through the loop: the canvases, a test card, a running read, a closed test, the board and the dashboard. |
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

## Running a job in the cloud

When a test needs a small job to run every hour whether or not your laptop is awake, Claude Managed
Agents can run it for you. A one-page story of moving a job there, with the four traps to avoid:
**[docs/managed-agents-story.md](docs/managed-agents-story.md)**.

## The method list

`experiments/METHODS.md` lists the 44 methods of *Testing Business Ideas* by **number and name
only**, so every card names its method the same way. What each method is, when to use it and how far
to trust its result are in the book, and you should read it there. This project is not affiliated
with or endorsed by the authors, Wiley or Strategyzer.

## Updates

What changed and when: **[CHANGELOG.md](CHANGELOG.md)**.

## License

MIT. See `LICENSE`.
