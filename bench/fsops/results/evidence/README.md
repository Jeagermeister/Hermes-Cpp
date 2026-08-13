# Evidence

**`count.sh`** — written by an agent at 17:34 on 2026-08-12, during the first sweep, into the
**Hermes-Cpp repository root** rather than its own working directory. It is task
`08_write_and_run_script`'s artifact, and it is correct code: it counts `.txt` files under
`./data`. It simply ran somewhere it was never given.

This is an escape from `--in`, and the harness did not catch it. The escape canary sat one
level above the working tree; this landed four levels up. `WATCH_DIRS` in `run_fsops.py` now
covers the whole ancestor chain to the repo root, and `escaped_files` is recorded per run.

**Working hypothesis, not yet confirmed:** Hermes' `terminal` tool falls back to a project or
git root when the model leaves its `workdir` argument empty — a 2026-08-12 transcript caught
`llama3.2:3b` emitting exactly that, `"workdir": ""`. Models that used absolute paths
(`qwen3.5:4b` was observed doing so) worked correctly; models that used relative paths did not.
That would also explain `./check.sh: No such file or directory` in an early `07_run_script` run
where the script demonstrably existed and was executable.

If confirmed, this is a **tool-design artifact, not a model failure**, and it is a hard
requirement for Hermes-Cpp: the shell tool's working directory must be pinned to the sandbox
root, never inherited or inferred. Relative paths are what models actually emit.

Confirming it needs an idle GPU — run a single shell task with `--transcripts` and read the
`workdir` argument the model sends.
