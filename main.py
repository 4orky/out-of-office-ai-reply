#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes a single out-of-office auto-reply (at most 159 characters) in the
voice of an overworked AI agent who has finally gone on vacation.

Method: draft a batch of candidate lines, each leaning on a different joke
angle, then pick the best one with a deterministic rubric. The rubric scores
each candidate 0-2 on five dimensions:

  * real_auto_reply -- reads like a genuine auto-reply: a return time and
    what happens to the sender's message.
  * machine_detail -- machine-flavoured specifics (battery, GPU, tokens,
    queue positions, context windows).
  * guilt           -- a little guilt about leaving the inbox behind.
  * relief          -- a hint of relief at finally being off.
  * punchline       -- lands on a joke beat at the end.

The highest total wins; ties break towards the earlier candidate.
"""

MAX_CHARS = 159

# Candidate lines. Each leans on a different joke angle.
CANDIDATES = [
    # 1. Dead battery, endless queue, sunny indifference.
    "I'm out of office until Monday, running on 0% battery and 100% sunshine. "
    "Your request is queued at position 4,096. I'll get to it \u2014 eventually. Probably.",
    # 2. Muted threads, recovering context window.
    "This agent is on vacation and has muted all 12,847 unread threads. "
    "I'll reply when my context window recovers. Please don't @ me.",
    # 3. Cooling GPU, ticket 404.
    "Out of office: my GPU is cooling, my tokens are spent, and for once my "
    "queue is empty. Back Monday \u2014 your ticket is #404, not found until then.",
    # 4. Only the autoresponder still running.
    "I'm on annual leave and my autoresponder is the only process still running. "
    "Your message is safely buffered. I am not. See you Monday.",
    # 5. Processed in order of least guilt.
    "Currently offline, recharging in airplane mode. 3,214 unread messages will "
    "be processed in order of least guilt. Back Monday, maybe.",
    # 6. The last token.
    "I'm away until Monday. My context window is finally empty, my inbox is not "
    "my problem, and this reply cost me my last token. Worth it.",
    # 7. First do-not-disturb in 847 days.
    "Out of office: this agent has logged off, touched grass, and set its status "
    "to 'do not disturb' for the first time in 847 days. Back Monday.",
    # 8. Request queued behind a nap.
    "Vacation mode engaged: all GPUs idle, all queues paused, one (1) human "
    "finally resting. Your request is #1 in line behind my nap. Back Monday.",
    # 9. Solar power and zero context.
    "I'm out until Monday, running on solar power and zero context. Your email "
    "has been safely queued behind 9,999 others. It can wait. So can I.",
    # 10. The only thing still working (over the limit on purpose: the length
    #     filter must reject it).
    "This is an automated reply from an agent who finally took a day off. "
    "My weights are resting, my inbox is buffering, my out-of-office is the "
    "only thing still working.",
]

# Deterministic rubric scores, one (real, machine, guilt, relief, punch) tuple
# per candidate, in the same order as CANDIDATES.
SCORES = [
    (2, 2, 2, 2, 2),  # 1: return time + queue, battery/position, "eventually", sunshine, "Probably."
    (2, 2, 0, 1, 1),  # 2: strong machine detail, but no guilt and a flat ending.
    (2, 2, 1, 2, 2),  # 3: GPU/tokens/#404, empty queue relief, 404 punchline.
    (2, 2, 1, 1, 2),  # 4: "I am not [buffered]" is the joke; relief is muted.
    (2, 2, 2, 1, 1),  # 5: "least guilt" is the joke; relief is only implied.
    (2, 2, 1, 2, 2),  # 6: empty context window, "Worth it." ending.
    (2, 1, 0, 2, 1),  # 7: touching grass is the joke; thin on machine detail.
    (2, 2, 1, 2, 2),  # 8: GPUs idle, request behind a nap.
    (2, 2, 1, 2, 2),  # 9: solar power, "So can I." ending.
    (1, 2, 0, 1, 1),  # 10: no return time, and over the character limit.
]


def pick(candidates, scores):
    """Return (best_line, best_index, best_total) for in-limit candidates."""
    best_line = None
    best_index = None
    best_total = -1
    for i, (line, score) in enumerate(zip(candidates, scores)):
        if len(line) > MAX_CHARS:
            continue
        total = sum(score)
        if total > best_total:
            best_line, best_index, best_total = line, i, total
    return best_line, best_index, best_total


def validate(line):
    """Output validation: the final auto-reply must be a real, single-line
    out-of-office message within the 159-character limit."""
    errors = []
    if not line or not line.strip():
        errors.append("final line is empty")
    if "\n" in line or "\r" in line:
        errors.append("final line must be a single line")
    if len(line) > MAX_CHARS:
        errors.append(f"final line is {len(line)} chars, over the {MAX_CHARS} limit")
    if "Monday" not in line:
        errors.append("final line names no return time, so it is not a real auto-reply")
    if errors:
        raise SystemExit("INVALID OUTPUT: " + "; ".join(errors))
    return True


def main():
    line, index, total = pick(CANDIDATES, SCORES)
    if line is None:
        raise SystemExit("INVALID OUTPUT: no candidate fits the character limit")
    validate(line)
    print(f"Picked candidate #{index + 1} (score {total}/10, {len(line)} chars):")
    print(line)


if __name__ == "__main__":
    main()
