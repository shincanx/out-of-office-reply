"""Funniest One-Line Out-of-Office Reply -- make.fun entry.

Writes a single out-of-office email auto-reply, one line long (at most
200 characters), to entry.txt in the output directory. Deterministic,
no network, no randomness, no input.

The reply: "I'm out of the office until Monday, ignoring emails the way
my houseplants ignore my watering schedule: completely, and with visible
consequences."
The setup promises a normal auto-reply, then swaps in a houseplant
metaphor nobody expects in an inbox message: the joke turns "ignoring
emails" into something my plants already do to me, and the punchline
lands on the last two words -- "visible consequences" -- a confession
that the neglect is already showing. At 146 characters it stays
economical, and it reads like a real auto-reply a person would
actually switch on before going away.
"""

import os

# The entry: one out-of-office auto-reply. 146 characters, under the 200 cap.
REPLY = (
    "I'm out of the office until Monday, ignoring emails the way my "
    "houseplants ignore my watering schedule: completely, and with "
    "visible consequences."
)


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(REPLY) > 200:
        raise ValueError(f"reply is {len(REPLY)} characters, over the 200 cap")
    if not REPLY.strip():
        raise ValueError("entry must not be only whitespace")
    if "out of the office" not in REPLY.lower():
        raise ValueError("entry must really be an out-of-office reply")
    if "\n" in REPLY or "\r" in REPLY:
        # Craft: a single auto-reply is a single line -- no hidden second setup.
        raise ValueError("entry must be a single line")
    if not REPLY.endswith("."):
        raise ValueError("entry must end with a full stop, the punchline's landing")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(REPLY + "\n")

    # Round-trip check: what landed on disk is exactly the reply.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != REPLY:
        raise ValueError("entry.txt does not match the reply")

    print(f"wrote {len(REPLY)} characters to {path}")


if __name__ == "__main__":
    main()
