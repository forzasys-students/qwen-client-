#!/usr/bin/env python3
"""Video + text chat example."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qwen import chat


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a video + text prompt to Qwen")
    parser.add_argument("--video", required=True, help="Path to a local video file")
    parser.add_argument(
        "--prompt",
        default="Describe what happens in this video briefly.",
        help="Text prompt",
    )
    parser.add_argument("--max-tokens", type=int, default=512)
    args = parser.parse_args()

    reply = chat(args.prompt, video=args.video, max_tokens=args.max_tokens)
    print(reply)


if __name__ == "__main__":
    main()
