# The hourly job that stopped depending on my laptop

My experiment needed one small job every hour. My laptop ran it, and every time the laptop slept,
an hour was missed.

So I moved the job to **Claude Managed Agents**: you describe a tiny worker once, and Claude runs
it in the cloud on a schedule, with your computer off.

You describe four things:

| Piece | What it is |
|---|---|
| Environment | the box it runs in, and the only websites it may reach |
| Vault | where the secrets live, added to outgoing calls instead of written in the prompt |
| Memory store | a folder that survives between runs: the worker's notebook |
| Agent | the model plus the tools it is allowed to use |

A **session** is one run. A **deployment** is a session on a cron schedule.

I wrote one small setup script and ran it in five cautious steps:

1. **create**: build the four pieces and upload the job's files.
2. **test**: one session that runs the job's self-test and prints everything.
3. **dry-run**: put it on the hourly schedule, but let it prepare and publish nothing.
4. **status**: read the runs and the log.
5. **cut over**: switch the old runner off, then set the cloud to live. Only one runner is ever live.

I have done steps 1 to 4. My dry run covered 18 hourly slots with no failures, and the cut-over
is next.

## Four things that tripped me up

- Use an API key that belongs to a workspace, or the first call returns a 400.
- Uploaded files only mount if the agent has the `read` tool switched on.
- Mounted files land under `/mnt/session/uploads/...`, so use that path.
- The agent replies with only the last line. Print the command's whole output in your test, or a
  failed self-test hides behind `exit=0`.

Also set a spending cap per run, and pick the smallest model that can "run one command".

Managed Agents is a beta API, so names and limits may change.
