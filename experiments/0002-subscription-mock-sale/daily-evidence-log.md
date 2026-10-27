# 0002 · Daily evidence log

## 2026-10-27 09:00 UTC · interim, day 2 of 14

| Step | Count |
|---|---|
| Visitors who reached the price | 61 |
| Clicked Subscribe | 4 (6.6%) |
| Left an email | 3 |

Against the bar: 4 of the 10 needed, with 61 of the 100 visitors the bar is set on. Interim: no
decision. The window covers two weekends (31 Oct–1 Nov and 7–8 Nov).

Query used (web analytics, test visits excluded):

```sql
select countIf(event = 'price_seen') as reached_price,
       countIf(event = 'subscribe_clicked') as clicked
from events
where properties.c = '0002' and timestamp >= '2026-10-26 09:00:00'
```
