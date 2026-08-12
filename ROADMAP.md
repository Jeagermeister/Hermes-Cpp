# Roadmap

Scope, sequencing, and the things that must be settled before code is worth writing.

---

## What this is

A **supervisor for local models doing filesystem work** — not a chatbot, and not a port of
upstream Hermes. It drives Ollama models through bounded sessions, verifies what they actually
did between turns, and re-invokes them with one concrete remaining failure.

That architecture is not a preference. It is what the local-model tournaments concluded.

---

## The evidence this is built on

From `local-agent-integration-diagnostic/results/RECOMMENDATIONS.md`, run on **`kitchen-desktop`**
through **OpenCode**:

| Finding | Consequence for this project |
|---|---|
| Qwen 9B: **6/6** functional stages; best bounded implementation worker | Primary target model |
| Gemma 12B failed only by selecting a **similarly named test file** | Tools must make targets unambiguous |
| E4B treated **rendered end-of-file annotations as literal content** | File rendering is a tool-design hazard |
| *"Use an external supervisor that checks repository state and reinvokes"* | This is the product |
| *"Break larger work into fresh sessions"* | Startup cost compounds — hence a native binary |
| Historical Q4 **6/6**, matched rerun **4/6**, identical inputs | Run-to-run variance is large |
| Q8 run **erased `tally.py`** | Destructive failure is real; guardrails are not optional |

**Two of these are probably harness artifacts, not model behaviour** — the EOF-annotation
failure and the short-file edit guidance both smell like OpenCode's tool design rather than
anything intrinsic to the model. Separating those is the point of Phase 0.

---

## Phase 0 — Establish which findings actually transfer

**Question:** which OpenCode findings are model-intrinsic, and which are tool-design artifacts?
A finding you must design *around* is very different from one you can design *away*.

**The harness is written and smoke-tested — see [`bench/`](./bench/).**

- [ ] **Install Hermes Agent on `kitchen-desktop`.** It is currently only on the MSI laptop.
- [ ] **Build the `num_ctx`-pinned Ollama variants** from
      `local-agent-tournament/models/*.Modelfile`. `bench/run_hermes_diagnostic.py` preflights
      these and refuses to start if any are missing.
- [ ] **Run it:** `bench/run_hermes_diagnostic.py --models qwen-9b gemma-12b gemma-e4b --repeats 3`
- [ ] **Run on `kitchen-desktop`, not the laptop.** The OpenCode results came from there;
      running the comparison on different hardware would confound harness with GPU.
- [ ] **Three repeats minimum per model per stage.** Non-negotiable given 6/6-vs-4/6 variance on
      identical inputs. Single runs are noise.
- [ ] **Re-pull `qwen3.5:9b`** — the tournament's best performer is not currently installed.
- [ ] **Record the delta, not the score.** The interesting output is where the two harnesses
      make the *same model* behave differently. That delta is the tool-design requirements list.

> Phase 1 does not depend on any of this and can run in parallel.

---

## Phase 1 — Foundations (no blockers)

- [ ] Ollama client over the OpenAI-compatible endpoint (`/v1/chat/completions`).
      **Verified working 2026-08-12:** `gemma4:12b` emits clean structured `tool_calls`.
- [ ] JSON handling
- [ ] Config + CLI entry point
- [ ] Session/history model

### Decisions to settle first

These are hard to reverse and benefit from being argued out before code exists:

- [ ] **Concurrency model** — threads, an event loop, or blocking-and-simple?
- [ ] **HTTP library** — libcurl, or something lighter?
- [ ] **JSON library** — nlohmann for ergonomics, simdjson for speed, or both at different layers?
- [ ] **Tool interface shape** — this is the one that matters. Fifty tools will be added over
      time; the interface decides whether that is pleasant or awful.
- [ ] **Constrained decoding.** Ollama supports a JSON schema via `format`. This turns "hope the
      12B emits valid tool JSON" into "it structurally cannot emit invalid JSON" — likely the
      single biggest reliability lever available for small local models. Decide early; it shapes
      the tool interface.

---

## Phase 2 — Core loop and minimal tools

- [ ] Agent loop: history, tool dispatch, bounded turns
- [ ] `read`, `write`, `list` — enough to prove the loop end to end
- [ ] `edit` — hardest to get right; patch application is where harnesses usually fail
- [ ] `move`, `search`

---

## Phase 3 — The supervisor (the actual product)

- [ ] **State verification.** After each turn, check what the model *claims* against what the
      filesystem *shows*.
- [ ] **Re-invocation** with one concrete remaining failure, per the tournament recommendation.
- [ ] **Guardrails** — dry-run, backup-before-mutate, undo. The erased `tally.py` is the argument.
- [ ] **Bounded sessions** — fresh session per unit of work rather than one long autonomous run.

---

## Explicitly out of scope

Tracked in `parity.tsv` as `OUT_OF_SCOPE` so upstream drift there is ignored rather than
silently accumulating:

`hermes_cli/` · `gateway/` · `tui_gateway/` · `acp_adapter/` · `plugins/` · `skills/` · `cron/`

Upstream is ~870k lines of non-test Python. A wholesale port is not the goal and never was.

---

## Open questions

- **Test oracle.** Upstream ships 2,877 test files. Are any worth adapting as a behavioural
  spec, given this is not a port and the behaviour is only selectively shared?
- **Context strategy.** Local models have far less context than cloud models. Agentic file work
  consumes it quickly, so what gets sent, and what gets summarised, is a first-class design
  problem rather than an optimisation.
- **Which models, on which machines.** A full list exists; the tournament harnesses already
  encode part of it.
