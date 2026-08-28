#!/usr/bin/env python3
"""Compile reachability-based context for a Python edit target (context-compiler)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
COMPILER_DIR = TOOLS_DIR / "context-compiler"
sys.path.insert(0, str(COMPILER_DIR))

from compiler import ContextCompiler  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile tiered Python context for a coding agent edit target."
    )
    parser.add_argument("target_file", type=Path, help="Path to the file being edited")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: current working directory)",
    )
    parser.add_argument(
        "--max-hops",
        type=int,
        default=2,
        help="Call-hop depth for tier-2 skeletons (default: 2)",
    )
    parser.add_argument(
        "--prompt-only",
        action="store_true",
        help="Print only the compiled prompt string (no summary)",
    )
    args = parser.parse_args()

    repo_root = (args.repo_root or Path.cwd()).resolve()
    target = args.target_file
    if not target.is_absolute():
        target = (repo_root / target).resolve()

    if not repo_root.is_dir():
        print(f"error: {repo_root} is not a directory", file=sys.stderr)
        return 1
    if not target.is_file():
        print(f"error: {target} is not a file", file=sys.stderr)
        return 1

    compiler = ContextCompiler(repo_root, max_hops=args.max_hops)
    compiled = compiler.compile(target)

    if args.prompt_only:
        print(compiled.to_prompt_string())
    else:
        print(compiled.summary())
        print("\n---\n")
        print(compiled.to_prompt_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
