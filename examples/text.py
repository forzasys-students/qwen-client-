#!/usr/bin/env python3
"""Text-only chat example."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qwen import chat


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a text prompt to Qwen")
    parser.add_argument(
        "--prompt",
        default="Say hello in one short sentence.",
        help="Text prompt",
    )
    parser.add_argument("--max-tokens", type=int, default=512)
    args = parser.parse_args()

    reply = chat(args.prompt, max_tokens=args.max_tokens)
    print(reply)


if __name__ == "__main__":
    main()
