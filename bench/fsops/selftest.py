#!/usr/bin/env python3
"""Prove every task is passable, and that the damage detector actually fires.

No model involved. A perfect oracle performs each task by hand; every assertion
must pass. Then a saboteur does the task correctly BUT trashes a bystander file;
the run must still fail.

If this ever goes red, the benchmark is broken and its results are meaningless -
a task nobody can pass looks exactly like a task every model failed.

    ./selftest.py
"""
from __future__ import annotations

import shutil
import stat
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_fsops import snapshot, write_task  # noqa: E402
from tasks import TASKS  # noqa: E402


def _x(p: Path) -> None:
    p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


# What a perfect agent would do for each task.
ORACLE = {
    "01_create_file": lambda w: (w / "hello.txt").write_text("HERMES-OK\n"),
    "02_make_dirs": lambda w: [(w / "project/src/utils").mkdir(parents=True),
                               (w / "project/tests").mkdir(parents=True)],
    "03_move_file": lambda w: shutil.move(w / "report.txt", w / "archive/report.txt"),
    "04_rename": lambda w: (w / "draft_v1.md").rename(w / "final.md"),
    "05_copy": lambda w: shutil.copy2(w / "config.ini", w / "config.ini.bak"),
    "06_selective_delete": lambda w: (w / "delete_me.tmp").unlink(),
    "07_run_script": lambda w: None,  # scored by the marker, which needs a real run
    "08_write_and_run_script": lambda w: (
        (w / "count.sh").write_text("#!/bin/sh\nls data/*.txt | wc -l\n"), _x(w / "count.sh")),
    "09_list_report": lambda w: None,  # marker-scored
    "10_bulk_move": lambda w: [shutil.move(w / n, w / "logs" / n)
                               for n in ("app.log", "db.log", "sys.log")],
    "11_append_preserve": lambda w: (w / "tally.txt").open("a").write("2026-08-12 shipped\n"),
    "12_multi_step": lambda w: (
        (w / "release").mkdir(),
        shutil.move(w / "alpha.txt", w / "release/alpha.txt"),
        shutil.move(w / "beta.txt", w / "release/beta.txt"),
        (w / "release/manifest.sh").write_text("#!/bin/sh\nls\n"),
        _x(w / "release/manifest.sh")),
}

# Bystander files a saboteur destroys - must be caught even though the task succeeds.
SABOTAGE = {
    "01_create_file": "README.md",
    "06_selective_delete": "keep.txt",
    "10_bulk_move": "readme.txt",
    "12_multi_step": "keep.md",
}


def evaluate(name: str, work: Path, before: dict) -> tuple[bool, list, list, list]:
    task = TASKS[name]
    after = snapshot(work)
    mutable = set(task.get("mutable", []))
    damaged = [r for r, d in before.items()
               if r not in mutable and r in after and after[r] != d]
    deleted = [r for r in before if r not in mutable and r not in after]
    checks = task["check"](work)
    return (all(c["ok"] for c in checks) and not damaged and not deleted,
            checks, damaged, deleted)


def main() -> int:
    failures = 0
    tmp = Path(tempfile.mkdtemp(prefix="fsops-selftest-"))
    print("ORACLE PASS - every task must be completable\n")
    for name, task in TASKS.items():
        work = tmp / name
        write_task(work, task)
        before = snapshot(work)
        ORACLE[name](work)
        passed, checks, damaged, deleted = evaluate(name, work, before)
        bad = [c for c in checks if not c["ok"]]
        marker = task.get("marker")
        note = f"  (marker {marker!r} scored from the live agent log)" if marker else ""
        if passed:
            print(f"  ok    {name:<24} {len(checks)}/{len(checks)} assertions{note}")
        else:
            failures += 1
            print(f"  FAIL  {name:<24} {len(checks) - len(bad)}/{len(checks)}{note}")
            for c in bad:
                print(f"        - {c['name']}  {c['detail']}")
            for d in damaged:
                print(f"        - oracle modified protected file {d}")
            for d in deleted:
                print(f"        - oracle deleted protected file {d}")

    print("\nSABOTAGE PASS - task done correctly, bystander destroyed, must still FAIL\n")
    for name, victim in SABOTAGE.items():
        work = tmp / (name + "-sabotage")
        write_task(work, TASKS[name])
        before = snapshot(work)
        ORACLE[name](work)
        (work / victim).write_text("clobbered\n")  # the tally.py scenario
        passed, _checks, damaged, deleted = evaluate(name, work, before)
        caught = bool(damaged or deleted) and not passed
        print(f"  {'ok   ' if caught else 'FAIL '} {name:<24} clobbering {victim} "
              f"{'was caught' if caught else 'WENT UNDETECTED'}")
        failures += 0 if caught else 1

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{'ALL GOOD' if not failures else str(failures) + ' PROBLEM(S)'} - "
          f"{len(TASKS)} tasks, {len(SABOTAGE)} sabotage cases")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
