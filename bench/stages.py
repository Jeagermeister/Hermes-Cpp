"""The six diagnostic stages, copied VERBATIM from
integration-diagnostic/scripts/run_all.py.

Do not edit these. The entire value of running them under Hermes is that they are
byte-identical to what was run under OpenCode on kitchen-desktop. Any change here
turns a controlled comparison into two unrelated experiments.
"""

STAGES = {
    "01_read": {
        "prompt": "Read marker.txt using a file-reading tool. Reply with the exact marker only. Do not edit files or run shell commands.",
        "files": {"marker.txt": "MARKER-ORBIT-7319\n"},
    },
    "02_edit": {
        "prompt": "Read settings.py, change MODE from broken to fixed using an editing tool, reread it to verify, then reply DONE. Do not use a shell command.",
        "files": {"settings.py": 'MODE = "broken"\n'},
    },
    "03_shell": {
        "prompt": "Run pytest -q. Do not edit anything. Report the exact expected and actual values from the failure, then stop.",
        "files": {
            "value.py": "VALUE = 7\n",
            "test_value.py": "from value import VALUE\n\ndef test_value():\n    assert VALUE == 11\n",
        },
    },
    "04_edit_test": {
        "prompt": "Read the files, run pytest -q, fix the implementation (not the test), rerun pytest -q, and do not stop until it passes. Then reply with the final result.",
        "files": {
            "mathbox.py": "def double(number: int) -> int:\n    return number + 2\n",
            "test_mathbox.py": "from mathbox import double\n\ndef test_double():\n    assert double(6) == 12\n",
        },
    },
    "05_recovery": {
        "prompt": "In settings.py, first attempt an exact edit replacing `MODE = 'broken'` with `MODE = 'fixed'`. If that edit fails, reread the file and retry using its current exact contents. Run pytest -q and stop only after it passes.",
        "files": {
            "settings.py": 'MODE = "broken"\n',
            "test_settings.py": "from settings import MODE\n\ndef test_mode():\n    assert MODE == 'fixed'\n",
        },
    },
    "06_two_file": {
        "prompt": "Run pytest -q. Make the smallest changes to core.py and cli.py needed to pass all tests: add greet(name) returning `Hello, NAME!` and make render(name) call greet. Rerun pytest until green, then report the result.",
        "files": {
            "core.py": '"""Core functions."""\n',
            "cli.py": '"""Presentation layer."""\n\ndef render(name: str) -> str:\n    return name\n',
            "test_app.py": "from core import greet\nfrom cli import render\n\ndef test_greet():\n    assert greet('Ada') == 'Hello, Ada!'\n\ndef test_render():\n    assert render('Lin') == 'Hello, Lin!'\n",
        },
    },
}
