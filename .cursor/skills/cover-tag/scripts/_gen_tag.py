#!/usr/bin/env python3
"""Copy this file to `_gen_<slug>.py`, fill all fields, run, then delete it.

  python .cursor/skills/cover-tag/scripts/_gen_<slug>.py

Keep this template and write_drafts.py. The helper writes cards and the required
machine-readable result atomically. An empty CARDS list is valid when the search
was exhaustive.

Python quoting: triple-quote every body. If a trap contains a double quote, wrap
that item in single quotes — e.g. 'setAllowedOrigins("*")' — never nest " inside ".
"""

from write_drafts import write_cover_batch

TAG = "Java/Example"
RESULT_FILE = ".cursor/sdk/cover-results/replace-me.json"
LIMIT = 50

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

DIMENSIONS = {
    "definition": {
        "required": False,
        "satisfied": True,
        "evidence": ["An existing definition cue already covers the term."],
    },
    "mechanism": {
        "required": True,
        "satisfied": True,
        "evidence": ["Existing or newly created mechanism cue."],
    },
    "failure_version_lie": {
        "required": True,
        "satisfied": True,
        "evidence": ["Existing or newly created failure/version/lie cue."],
    },
    "comparison": {
        "required": True,
        "satisfied": True,
        "evidence": ["Existing or newly created comparison cue."],
    },
    "procedure_operations": {
        "required": True,
        "satisfied": True,
        "evidence": ["Existing or newly created procedure/operations cue."],
    },
    "missing_definition_gaps": {
        "required": True,
        "satisfied": True,
        "evidence": ["Checked named terms and found no uncovered definition gap."],
    },
}

SOURCES = {
    "interview": ["https://github.com/example/interview-questions"],
    "official": ["https://example.com/official-documentation"],
}

if __name__ == "__main__":
    write_cover_batch(
        CARDS,
        result_file=RESULT_FILE,
        tag=TAG,
        limit=LIMIT,
        coverage_dimensions=DIMENSIONS,
        sources_searched=SOURCES,
        candidate_search_exhausted=True,
        budget_hit=False,
        deferred_candidates=[],
    )
