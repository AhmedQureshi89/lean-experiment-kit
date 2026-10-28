# Walkthrough: one experiment, from idea to decision

This follows a founder through the kit with the example business, **Bean Box**, a made-up coffee
subscription. Every file it mentions is in this repo as it was left at the end, so you can open them
side by side: `experiments/canvas/`, `experiments/0001-work-from-home-interviews/` and
`experiments/0002-subscription-mock-sale/`.

```
 Day 0     /get-started ─────────▶ canvases, riskiest belief, dashboard
 Day 0     "test the idea…" ─▶ test card 0001, waiting on your go
 Days 1–14 you run the test; "pull the numbers" ─▶ dated reads against the bar
 Day 15    "log 0001" ──────▶ learning card, your decision, the canvas moves
 Day 15    one next hypothesis ─▶ test card 0002, and round again
```

You type in plain words. Claude writes the files. You make every decision.

---

## Before you start (five minutes)

1. On GitHub, press **Use this template** → *Create a new repository*. Make it **private**, then
   clone it.
2. Install the one Python package the build needs: `python -m pip install pyyaml`
3. Open Claude Code in the folder. It sees the kit still holds the example, and offers `/tour` or
   `/get-started`.

If you want to see the loop first, type `/tour`. It shows the pieces below one at a time, using
the example, in about five minutes.

## Day 0 · Set up: `/get-started` (about fifteen minutes)

Claude asks a few questions at a time, each with a one-line example. "I don't know" is a good
answer: it becomes an honest belief, scored as having no evidence yet.

> **Claude:** Who exactly are you building for first? *(for example: people who work from home and
> drink two or more cups a day)* What are they trying to get done, and what is the worst part of it
> today?
>
> **Founder:** People working from home. They run out of good coffee mid-week and end up drinking
> instant.
>
> **Claude:** How do you know: have you seen it, has someone told you, or is it your belief?
>
> **Founder:** My belief, mostly. Two friends said it.

From the answers Claude writes:

| File | What it holds |
|---|---|
| `kit.config.json` | the name, your time zone, your weekend, the day your week starts |
| `customer-segments.md` | who the customers are: Seg 1 (work-from-home coffee drinkers), Seg 2 (small offices) |
| `experiments/canvas/VP-A.md` | the **Value Proposition Canvas**: what customers try to do (jobs), what hurts (pains), what they want (gains), and how the offer answers each |
| `experiments/canvas/LC-A.md` | the **Lean Canvas**: the whole business in nine blocks (problem, customers, promise, solution, channels, revenue, costs, key metric, unfair advantage) |

Every row gets two scores, which Claude proposes and you correct:

- **Matters** (1–3): how much the business depends on it. 3 means that if it's wrong, there is no
  business.
- **Evidence** (0–3): how much you know. 0 is belief; 2 is seen once in real data.

The **riskiest box** is the one that matters most and is known least. For Bean Box at the start it
was `J1`, "keep good coffee in the house without thinking about it". Claude then creates your
private **dashboard** on claude.ai and gives you the link. Open it on your phone and keep it there.

## Day 0 · The first test: "test the idea that …"

Claude proposes one first test against the riskiest box. You can also write your own:

> **Founder:** Test the idea that people who work from home run out of good coffee mid-week and
> mind it.

Claude writes `experiments/0001-work-from-home-interviews/test-card.md`. Its header is the record
that the board and the dashboard are built from:

```yaml
title: People who work from home run out of good coffee mid-week and mind it
segment: Seg 1 Work-from-home coffee drinkers
method: "#1 Customer Interview"
boxes: ["J1", "P1", "CS1"]
bar: 5 of 8 interviewees describe running out without being prompted
status: planned
waiting_on: "Your go to start"
```

Below the header the card says why this is the **cheapest test that still gives believable
evidence**: eight 20-minute conversations, no money spent, and never asking about the product, only
about their last week. It also says how each number will be measured, before anything starts.

The bar is set **before** the test. That is what keeps you honest later.

## Days 1–14 · Run it

You run the interviews (or launch the page, or send the emails: whatever the method is). Nothing is
sent or posted without your go. Interviews are counted at the end, so this read comes from the
example's running test, 0002, a page that shows a price. When you want to see where a test stands:

> **Founder:** Pull the numbers for 0002.

Claude reads each source the card names: a connector to your analytics or database if you have one,
or the numbers you paste. It writes a dated entry in the experiment's `daily-evidence-log.md`:

```
2026-10-27 09:00 UTC · interim, day 2 of 14
Visitors who reached the price   61
Clicked Subscribe                4 (6.6%)
Against the bar: 4 of the 10 needed. Interim: no decision.
```

The dashboard's **Today** tab shows the same count against the bar, how far through the window you
are, and a warning when the window covers your weekend. **An interim read never decides
anything.**

## Day 15 · Close it: "log 0001"

When the window has closed:

> **Founder:** Log 0001.

Claude reads the final numbers against the bar and writes the **learning card**:

> **Observation:** 6 of 8 described running out, unprompted. **Bar:** 5 of 8 → met.
> **Insight:** the pain is real for this group. Two people would not leave their local café.
> **Decision:** persevere ✅

The decision is **yours**: persevere (keep going), pivot (change one part) or kill (stop). Claude
never marks persevere without a number that clears the bar.

Then the canvas moves. `J1` and `P1` go from belief to **seen**, Evidence 0 → 2, and the canvas
version goes up with a line saying why. The riskiest box is now the next unknown: `G1`, "coffee just
arrives before it runs out", which nobody has shown they would pay for.

Claude proposes **exactly one** next hypothesis. Here it was 0002: will people click "Subscribe" on a
page that shows a monthly price? That is the running test in this repo.

## What is yours and what is Claude's

| You | Claude |
|---|---|
| say what to test | writes the test card, the method and the measurement plan |
| set or accept the bar | checks the card against the rules before it can start |
| give the go to start, send or post | records when it went live and the window |
| run the test | reads the numbers, writes dated entries |
| decide: persevere, pivot or kill | writes the learning card, moves the canvas, proposes one next test |
| read the dashboard | keeps the board and the dashboard current |

## When something looks wrong

| You see | What it means |
|---|---|
| `PROBLEM:` lines | a card header or canvas row breaks a rule (an unknown method, a box that isn't in any canvas). Claude fixes it, or asks you if it needs your answer. |
| Claude asks to sync before it finishes | the cards changed since the dashboard last updated. Say yes, or tell it why not. |
| `python` is not found (Mac) | use `python3`, and change `python` to `python3` in `.claude/settings.json`. |
| No connector for your tools | paste the numbers in chat; `/pull-evidence` takes them from there. |
| "No Dashboard type on this account" | Claude Dashboards are a claude.ai feature. Without it, the board in `experiments/PROGRESS.md` still works. |
| You want the example back | it is in git: `git checkout <first commit> -- experiments`. |
