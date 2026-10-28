---
canvas: LC-A
kind: lean-canvas
zoom_in: VP-A
version: 2
date: "2026-10-20"
title: Bean Box Lean Canvas (example)
segment: The whole business. The first customers are people who work from home (Seg 1); offices (Seg 2) come later.
summary: 12 rows, 9 at Evidence 0. Two of nine blocks are covered by real evidence (Problem through VP-A, and Customer Segments). Nobody has paid yet, so Revenue Streams is the riskiest block.
riskiest: RS1
riskiest_why: Every other block rests on people paying a monthly price. No one has been asked to pay yet. 0002 is the first test that asks for money.
---

# LC-A · Bean Box Lean Canvas (example)

> **This is a made-up example business.** Type `/get-started` in Claude Code and it is replaced with your
> own, from your answers. To edit by hand instead, keep the header fields, the table columns and the
> "Read by theme" table: the dashboard reads them.

> **How this file works**
> - The header above is read by the dashboard. The table below is the canvas: one row per hypothesis, grouped by block.
> - IDs: two letters for the block, then a number. `PR` Problem · `CS` Customer Segments · `UV` Unique Value Proposition · `SO` Solution · `CH` Channels · `RS` Revenue Streams · `CO` Cost Structure · `KM` Key Metrics · `UA` Unfair Advantage. They cannot collide with VP-A's one-letter IDs.
> - **The zoom-in rule:** jobs, pains, gains, products, pain relievers and gain creators live in `VP-A.md`, which details the Problem and Solution blocks. A row here is a claim that canvas cannot hold.
> - **Tag**, customer side (`PR`, `CS`, `UV`, `RS`): `seen`, `signal`, `assumption`. Your side (`SO`, `CH`, `CO`, `KM`, `UA`): `live`, `untested`, `gap`. The same meanings as in `VP-A.md`.
> - **Matters** (1–3) and **Evidence** (0–3): the same scales as in `VP-A.md`.
> - A block counts as **covered** only when at least one of its rows (or, for Problem and Solution, a VP-A box) is at Evidence 2 or more. A planned or running test does not count.
> - Every row sits in exactly one theme of the **Read by theme** table, or the build stops.
> - When a tag or a score changes after a test reads out: edit the row, raise `version`, set `date`, and add a line under **Changes**. Do not copy the file.

## Boxes

| ID | Box | Tag | Matters | Evidence | Source | Note |
|---|---|---|---|---|---|---|
| PR1 | People who work from home run out of good coffee mid-week | seen | 3 | 2 | 0001 interviews | The model-side face of VP-A P1. |
| CS1 | People who work from home and drink 2+ cups a day | seen | 3 | 2 | 0001 interviews | 8 recruited in a week from two local groups. |
| CS2 | Small offices of 5–20 people | assumption | 1 | 0 | belief | Later. |
| UV1 | Fresh coffee that arrives before you run out | assumption | 3 | 0 | belief | |
| SO1 | A monthly bean subscription, timed by hand at first | untested | 3 | 0 | belief | |
| CH1 | Local work-from-home groups online | untested | 2 | 1 | 0001 recruiting | Where the 8 interviewees came from. |
| RS1 | People pay a monthly price for it | assumption | 3 | 0 | belief | Riskiest row. 0002 tests it. |
| RS2 | A one-off sample pack sells as a first step | assumption | 2 | 0 | belief | |
| CO1 | Beans and posting cost under half of the price | untested | 2 | 0 | belief | |
| KM1 | Share of subscribers still subscribed after three months | gap | 2 | 0 | belief | No way to count it yet. |
| UA1 | A partnership with one local roaster | gap | 1 | 0 | belief | |
| UA2 | Knowing each customer's drinking pace | untested | 1 | 0 | belief | |

## Read by theme

| Theme | Read |
|---|---|
| Desirability (PR, CS, UV) | The problem and the people are seen. Whether the promise appeals is untested. |
| Feasibility (SO, CH, UA) | Nothing built yet; the first version is done by hand. |
| Viability (RS, CO, KM) | Nobody has paid. Everything here is belief. |

## Facts — where the data says the model breaks

| Number | What it says | Source |
|---|---|---|
| 2 of 8 | Two interviewees would not leave their local café. | 0001 learning card |

## Notes

- Example only. Delete this canvas's rows when you start your own.

## Changes

| Version | Date | What changed |
|---|---|---|
| 1 | 2026-10-05 | First draft from the founder's beliefs. |
| 2 | 2026-10-20 | PR1 and CS1 to seen, Evidence 2, after 0001. |
