# Hermes-Cpp

A fast, local-first agent runner in **C/C++**, built around **Ollama**.

Inspired by [NousResearch Hermes Agent](https://github.com/nousresearch/hermes-agent) (Python),
but **not a port of it**. Upstream is a reference for behaviour worth having, not a target to
match. Most of it — the messaging gateway, the plugin surface, the fifty cloud providers — is
deliberately out of scope.

## What it is for

Driving **local** models to do real filesystem work: create, modify, move, summarise and update
files, either directly or when called as a tool by a larger model.

The design follows an empirical finding rather than a preference. Local-model tournaments run on
`kitchen-desktop` (see `local-agent-tournament`, `local-agent-integration-diagnostic`) concluded:

> Use an external supervisor that checks repository state and reinvokes the model with one
> concrete remaining failure instead of relying on a single long autonomous session.
>
> Break larger work into fresh sessions. The isolated-session results strongly support this
> architecture.

So this is **a supervisor, not a chatbot**. Its job is keeping a 9–12B model on rails: bounded
sessions, verified state between turns, and guardrails on anything destructive.

## Why native code, honestly

Not for inference speed — the process is blocked on the model, and always will be. The wins are
structural:

| | |
|---|---|
| **Startup** | Bounded sessions mean *many* process launches. Python pays 1–3 s of interpreter and imports every time; a static binary pays ~10 ms. Under this architecture the advantage compounds per session. |
| **Verification** | Checking what the model actually did — walking trees, hashing, diffing — happens every turn. That is real work, and native code is good at it. |
| **Distribution** | One binary, versus a Python environment plus Node plus system dependencies. |

## Layout

| Path | What |
|---|---|
| `ROADMAP.md` | Scope, phases, and what has to be settled before code |
| `parity.tsv` | Which upstream subsystems are in scope, and where each stands |
| `tools/parity` | Reports drift against upstream for in-scope subsystems |
| `UPSTREAM-PARITY.md` | How the reference tracking works and why it is tag-granular |

Architecture, build system and source layout are **not yet decided**. Nothing here presumes them.

## Working with upstream

The Python reference lives at `~/Source/hermes-upstream` (blobless, `main` only, 261 MB). It is
not part of this repo and is disposable — it re-clones from GitHub in ~11 s.

```bash
hermes-upstream-sync      # refresh the reference, print what changed
tools/parity              # what has drifted in the subsystems we care about
tools/parity agent        # the specific commits behind agent/
```

Set `$HERMES_REF_REPO` if the reference lives elsewhere.

## Where this lives

Gitea (`git@gitea:Jeagermeister/Hermes-Cpp.git`) is authoritative, mirrored to GitHub — see the
`gitea-selfhost` repo. The reference clone deliberately does **not** live there: it is a pure
function of upstream, so backing it up would be storing something freely regenerable.

## License

**MIT** — see [LICENSE](./LICENSE).

Upstream Hermes Agent is also MIT (Copyright (c) 2025 Nous Research), so the licenses are
compatible. Since this is a reimplementation rather than a port, most code here is original
work — but MIT requires the copyright notice to travel with *substantial portions*, so anything
closely transliterated should carry an upstream attribution header.
