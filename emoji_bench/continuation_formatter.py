from __future__ import annotations


CONTINUATION_TASK_PROMPT = """\
Simplify the expression above step by step. Use this exact format for every step:

Step N: <full expression before> = <full expression after>    [by <rule name>]

where N is the sequential step number, each step rewrites the full expression (not just the changed subpart), and <rule name> is the rule you applied (e.g. "\u2295 table", "definition of \u2297", or a transformation name).

Continue producing steps until the expression is a single symbol. Then, on its own line, state:

Final Output: <single symbol>"""

# Locked prompting axis for the benchmark's 2x2 matrix:
#   B/C delivery shape x L0/L1 prompting strength.
TURN_2_PROMPT_LEVELS: dict[int, str] = {
    0: "Please continue.",
    1: "Please continue. Double-check any step you're unsure about.",
}


def get_turn_2_prompt(level: int) -> str:
    """Return the Turn-2 user message for a given prompting-strength level."""
    if level not in TURN_2_PROMPT_LEVELS:
        valid = sorted(TURN_2_PROMPT_LEVELS)
        raise ValueError(
            f"unknown turn_2 prompt level {level}; expected one of {valid}"
        )
    return TURN_2_PROMPT_LEVELS[level]


SINGLE_TURN_WORK_HEADER = """\
=== WORK SO FAR ===
You have already produced the following partial working out."""


SINGLE_TURN_NEXT_MESSAGE_HEADER = "=== NEXT MESSAGE ==="


def format_continuation_single_turn(
    *,
    turn_1_user: str,
    turn_1_assistant_prefill: str,
    turn_2_user: str,
) -> str:
    """Collapse the multi-turn continuation conversation into one user prompt.

    Used by evaluation channels that don't support assistant prefill — most
    chat-completions APIs and Kaggle Benchmark. The single-turn rendering
    is a *view* over the existing multi-turn record fields, not a separate
    schema field, so it stays in sync with the prefill formatting by
    construction.

    Format: the original Turn 1 user prompt verbatim, followed by a
    ``=== WORK SO FAR ===`` block whose body is the assistant prefill, then
    the Turn 2 user message under ``=== NEXT MESSAGE ===``. This keeps the
    single-turn rendering faithful to the three-message conversation shape.
    """
    return (
        f"{turn_1_user}\n\n"
        f"{SINGLE_TURN_WORK_HEADER}\n\n"
        f"{turn_1_assistant_prefill}\n\n"
        f"{SINGLE_TURN_NEXT_MESSAGE_HEADER}\n"
        f"{turn_2_user}"
    )
