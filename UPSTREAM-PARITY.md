# Upstream parity

This project is a **C/C++ rewrite** of [NousResearch Hermes Agent](https://github.com/nousresearch/hermes-agent),
which is written in Python. Upstream is a **reference, not a base**: there is no shared git
history and nothing is ever merged in. Work here is *ported* — read the Python, understand the
behaviour, implement it in C/C++.

That makes one question the central one, and it is unanswerable without bookkeeping:

> **Which parts of my implementation have fallen behind upstream, and what changed?**

`parity.tsv` answers it. `tools/parity` reports it.

## Granularity: release tags, not commits

Each subsystem records the upstream **release tag** it was ported from — not a commit SHA.

This is deliberate. Upstream lands roughly **1,100 commits a month** but cuts only about
**two releases**. Tracking commits would mean triaging ~1,100 diffs a month, which nobody
sustains; the ledger would rot within weeks and then lie to you. Tags are the natural review
unit — upstream declared that state coherent — and they reduce the job to ~2 review events a
month.

Commit-level detail is still one command away when you actually sit down to port
(`tools/parity <subsystem>`). The ledger stays coarse; the drill-down stays sharp.

## Usage

```bash
tools/parity              # which subsystems are stale, and by how much
tools/parity agent        # the commits touching agent/ since it was ported
```

After porting a subsystem up to some tag, record it:

```
agent	agent/	v2026.8.3	PORTED
```

`STALE` is computed, never written by hand — the script derives it by comparing your recorded
tag against the newest upstream tag.

## Keeping the reference current

The reference clone lives at `~/Source/hermes-upstream` (override with `$HERMES_REF_REPO`).
It is a blobless, single-branch clone — 261 MB against 5.8 GB for a full mirror, because
upstream carries 1,505 branches of which only `main` matters here.

```bash
hermes-upstream-sync      # fast-forward it and print what changed
```

It is disposable: it re-derives from GitHub in about 11 seconds, which is why it lives on
this machine rather than on Gitea. **This** repo is the irreplaceable half.

## Scope reality

Upstream is **~870,000 lines of non-test Python**:

| Subsystem | LOC | Files |
|---|---:|---:|
| `hermes_cli/` | 213,032 | 269 |
| `agent/` | 136,521 | 188 |
| `tools/` | 128,965 | 136 |
| `plugins/` | 128,457 | 200 |
| `gateway/` | 103,744 | 88 |
| `tui_gateway/` | 26,422 | 23 |
| `skills/` | 16,505 | 66 |
| `cron/` | 11,695 | 13 |
| `acp_adapter/` | 5,809 | 11 |
| `providers/` | 452 | 2 |

A wholesale port is not realistic for one person, and chasing full parity against a target
moving at ~1,100 commits/month is a treadmill. The ledger is built to support **partial,
deliberate** parity: pick a vertical slice, port it, record the tag, and let the rest sit at
`NOT_STARTED` honestly rather than silently.

A reasonable first slice is `agent/` + a minimal `tools/` + `providers/` — enough for a loop
that talks to a model and executes a tool. `hermes_cli/` is the largest subsystem and the
least essential to prove the idea.
