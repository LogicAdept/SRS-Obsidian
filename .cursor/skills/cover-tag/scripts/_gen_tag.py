#!/usr/bin/env python3
"""Copy this file to `_gen_<slug>.py`, fill CARDS, run, then delete the copy.

  python .cursor/skills/cover-tag/scripts/_gen_<slug>.py

Keep this template and write_drafts.py. Do not reimplement meta/callouts/names-file.

Python quoting: triple-quote every body. If a trap contains a double quote, wrap
that item in single quotes — e.g. 'setAllowedOrigins("*")' — never nest " inside ".
"""

from write_drafts import write_all

CARDS = [
    # Draft (dump has an answer):
    # {
    #     "name": "What is example.md",
    #     "tags": "#Java/Example #SRS #New",
    #     "body": """Dump answer, English, no URLs or source names.""",
    #     "traps": [
    #         "Dump trap or version split.",
    #     ],
    # },
    # Stub (title only in the dump): omit body and traps.
    # {
    #     "name": "What is title only.md",
    #     "tags": "#Java/Example #SRS #New",
    # },
]

if __name__ == "__main__":
    write_all(CARDS)
