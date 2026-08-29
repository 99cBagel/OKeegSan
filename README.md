# O'KeegSan

**Keep going—with a steady companion.**

O'KeegSan is a GitHub-guided audio-chat companion for running, weight training,
and biking. It helps ChatGPT act as:

- a motivational coach and friendly training partner;
- a lightweight timer, rep counter, and activity logger; and
- a concise briefer on requested news, advances, and topics.

The repository is the durable source of guidance. ChatGPT reads the relevant
mode prompt at the beginning of an activity and produces a dated Markdown log
at the end.

## Start a session

1. In ChatGPT, connect the private `OKeegSan` repository through the GitHub app.
2. Start a voice conversation and name the mode and prompt path:
   - Run: `modes/run/README_run_prompt.md`
   - Weight training: `modes/weight-training/README_wt_prompt.md`
   - Bike: `modes/bike/README_bike_prompt.md`
3. Say: “Use the O'KeegSan instructions in that file for this session.”
4. At the end, approve creation of the proposed activity log, download/copy the
   Markdown, and add it to the matching `logs/<mode>/<year>/` folder.

> The ChatGPT GitHub connection is read-only. ChatGPT can draft the log, while
> Codex or local Git is used to save, commit, and push it.

## Repository map

```text
OKeegSan/
├── AGENTS.md                         # Rules for Codex maintenance
├── modes/
│   ├── run/README_run_prompt.md
│   ├── weight-training/README_wt_prompt.md
│   └── bike/README_bike_prompt.md
├── templates/                        # Canonical blank log templates
│   ├── run_log_template.md
│   ├── wt_log_template.md
│   └── bike_log_template.md
├── logs/                             # Dated activity records by mode/year
│   ├── run/2026/
│   ├── weight-training/2026/
│   └── bike/2026/
├── topics/                           # Optional briefing interests/watchlists
└── docs/                             # Setup and workflow documentation
```

Log filenames use local activity date: `YYYYMMDD_run_log.md`,
`YYYYMMDD_wt_log.md`, or `YYYYMMDD_bike_log.md`. If there are two sessions of
the same type on one day, append `_2` to the second filename.

## Important limitations

O'KeegSan is not an emergency or medical service. During outdoor activity,
safety and awareness come before conversation. Timer values are conversational
estimates unless confirmed by a watch, phone, or bike computer. News briefings
should be retrieved from current sources and clearly distinguish verified facts
from inference.

## Maintenance

See [docs/local-and-github-setup.md](docs/local-and-github-setup.md) for the
two-account GitHub setup, local commit workflow, and iPhone connection steps.
