---
canvas: VP-A
version: 2
date: "2026-10-20"
title: Bean Box Value Proposition Canvas (example)
segment: People who work from home and drink two or more cups of coffee a day (Seg 1 in customer-segments.md).
summary: The interviews found the pain (running out of good coffee mid-week) in six of eight people. Nobody has shown yet that they would pay a monthly price to stop it. The riskiest box is still G1.
riskiest: G1
riskiest_why: Every other box assumes people want coffee to arrive without thinking about it. The interviews heard it said, which is weak evidence. Experiment 0002 tests whether they act on it.
---

# VP-A · Bean Box Value Proposition Canvas (example)

> **This is a made-up example business.** Type `/get-started` in Claude Code and it is replaced with your
> own, from your answers. To edit by hand instead, keep the header fields and the table columns: the
> dashboard reads them.

> **How this file works**
> - The header above is read by the dashboard. The table below is the canvas: one row per box.
> - IDs: J jobs, P pains, G gains (customer side). S products and services, R pain relievers, C gain creators (your side).
> - **Tag**, customer side: `seen` (observed in real data or reported by a real customer), `signal` (a hint, one voice, or an inference), `assumption` (a belief, never tested). Your side: `live` (built and running), `untested` (exists or is claimed, no proof it helps), `gap` (missing or broken).
> - **Matters** (1–3): how much the business depends on this box being true. 3 = if this is wrong, the product has no reason to exist.
> - **Evidence** (0–3): how much you know either way. 0 = nothing but belief · 1 = a hint or one voice · 2 = seen once in real data, or tried once · 3 = established.
> - The dashboard's assumptions map plots Matters against Evidence. High Matters and low Evidence is the corner to test first.
> - Which experiment tests which box comes from each experiment's own header (`boxes:` in its test card). This file does not repeat it.
> - When a tag or a score changes after a test reads out: edit the row, raise `version`, set `date`, and add a line under **Changes**. Do not copy the file.

## Boxes

| ID | Box | Tag | Matters | Evidence | Source | Note |
|---|---|---|---|---|---|---|
| J1 | Keep good coffee in the house without thinking about it | seen | 3 | 2 | 0001 interviews | 6 of 8 described it unprompted. |
| J2 | Try new beans without buying a full bag that might be bad | signal | 2 | 1 | 0001 interviews | 2 of 8. |
| P1 | Running out mid-week and drinking instant coffee | seen | 3 | 2 | 0001 interviews | |
| P2 | Supermarket beans are stale by the time they are opened | signal | 2 | 1 | 0001 interviews | |
| G1 | Coffee just arrives before it runs out | assumption | 3 | 0 | belief | Riskiest box. 0002 tests it. |
| G2 | Feeling like a small treat in the work-from-home week | assumption | 1 | 0 | belief | |
| S1 | Monthly subscription of freshly roasted beans, posted | untested | 3 | 0 | belief | |
| S2 | A sample pack of three small bags | untested | 2 | 0 | belief | |
| R1 | Delivery timed to how fast each person drinks | gap | 3 | 0 | belief | Not built. Done by hand in a concierge test first. |
| C1 | A note from the roaster in every box | untested | 1 | 0 | belief | |

## Fit, read by pair

| Pair | Read |
|---|---|
| Jobs ⇄ Products and services | J1 is seen; S1 is the answer to it, untested. |
| Pains ⇄ Pain relievers | P1 is seen, and the reliever that answers it (R1) is not built yet. |
| Gains ⇄ Gain creators | Both gains are beliefs. Nothing here is evidence yet. |

## Facts — where the data says fit breaks

| Number | What it says | Source |
|---|---|---|
| 2 of 8 | Two interviewees buy beans from a local café and would not switch. | 0001 learning card |

## Notes

- Example only. Delete this canvas's rows when you start your own.

## Changes

| Version | Date | What changed |
|---|---|---|
| 1 | 2026-10-05 | First draft from the founder's beliefs. |
| 2 | 2026-10-20 | J1 and P1 to seen, Evidence 2, after 0001's interviews. |
