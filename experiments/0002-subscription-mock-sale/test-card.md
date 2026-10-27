---
id: "0002"
title: Work-from-home coffee drinkers click "Subscribe" on a priced page
segment: Seg 1 Work-from-home coffee drinkers
theme: viability
method: "#41 Mock Sale"
method_note: "The Subscribe button opens a 'not open yet, leave your email' form; nobody is charged."
boxes: ["RS1", "G1"]
sources: [analytics, email]
status: running
decision: none
bar: 10 of 100 visitors who reach the price click Subscribe within 14 days
result: "Interim, day 2: 4 of 61 visitors who reached the price clicked Subscribe (6.6%); 3 left an email"
read_at: "2026-10-27T09:00+00:00"
score_now: 4
score_target: 10
score_label: visitors who clicked Subscribe
score_parts: [{ n: 61, label: "reached the price" }, { n: 3, label: "left an email" }]
score_caveat: "Day 2 of 14, and 61 is not yet the 100 visitors the bar is set on."
bar_met: null
window_start: "2026-10-26T09:00+00:00"
window_end: "2026-11-09T09:00+00:00"
decided: ""
effort: 2
evidence: 4
waiting_on: ""
next: ""
live_dataset: ""
note: Running, day 2 of 14. 4 clicks so far against a bar of 10.
---
# Test Card

**Experiment ID:** 0002
**Date:** 2026-10-24
**Theme:** Viability
**Method (from METHODS.md):** #41 Mock Sale
**Canvas box tested:** LC-A v2 · RS1 · VP-A v2 · G1 · both assumptions.

- **Hypothesis:** We believe that people who work from home and drink two or more cups a day (Seg 1) will click "Subscribe" on a page that shows a monthly price of 18.
- **Test:** To verify that, we will post one page with the offer and the price in the same two groups as 0001, and count who reaches the price and who clicks Subscribe.
- **Metric:** And measure Subscribe clicks among visitors who scroll to the price.
- **Criteria:** We are right if 10 of the first 100 such visitors click within 14 days.

**Input (effort, 1–5):** 2
**Output (evidence strength, 1–5):** 4

## How we measure (fill before anything goes live)

| Source | What it answers | Exactly how (event, tag, filter or query) | On the dashboard as |
|---|---|---|---|
| Web analytics | visitors who reached the price; Subscribe clicks | events `price_seen` and `subscribe_clicked`, property `c = 0002`; both confirmed in the project before the post | the card's score (or `live-0002`) |
| Email form | who left an email after clicking | the form's own count; the addresses stay in a CSV, never in a `.md` file | a score tile |

Per person (one visitor id each). Baseline: none, the page is new.

## Before going live

- [x] Both events fire on a test visit, and test visits are filtered out
- [x] The page says plainly that the service is not open yet
- [x] The founder's go to post, given 2026-10-26
