# Hermes-Cpp

A **C/C++ rewrite** of [NousResearch Hermes Agent](https://github.com/nousresearch/hermes-agent)
(upstream is Python).

This is an independent implementation, not a fork. There is no shared git history with
upstream and nothing is merged from it — behaviour is *ported* by reading the Python and
reimplementing it.

## Layout

| Path | What |
|---|---|
| `parity.tsv` | Which subsystems are ported, and from which upstream release tag |
| `tools/parity` | Reports drift against upstream; drills into a subsystem's changes |
| `UPSTREAM-PARITY.md` | How the parity system works and why it is tag-granular |

Architecture, build system and source layout are not yet decided — nothing here presumes
them.

## Working with upstream

The Python reference lives at `~/Source/hermes-upstream` (blobless, `main` only, 261 MB).
It is not part of this repo and is disposable — it re-clones from GitHub in ~11s.

```bash
hermes-upstream-sync      # refresh the reference, print what changed
tools/parity              # what has drifted since I ported it
tools/parity agent        # the specific commits behind agent/
```

Set `$HERMES_REF_REPO` if the reference lives elsewhere.

## Where this lives

Gitea (`git@gitea:Jeagermeister/Hermes-Cpp.git`) is authoritative, consistent with the rest
of the setup — see the `gitea-selfhost` repo. The reference clone deliberately does **not**
live there: it is a pure function of upstream, so backing it up would be storing something
freely regenerable.
