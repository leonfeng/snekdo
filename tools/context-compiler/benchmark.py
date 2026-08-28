"""
benchmark.py
============
CLI entry point to run the Context Compiler against a real repository, so
any benchmark numbers you publish are reproducible from a command anyone
can re-run -- not hand-typed placeholders.

Usage:
    python benchmark.py <repo_root> <target_file> [--max-hops N] [--dump PATH]

Example:
    python benchmark.py ~/code/django-inventory-api \\
        ~/code/django-inventory-api/middleware/auth.py --max-hops 2
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from compiler import ContextCompiler


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark the Context Compiler against a real repo.")
    parser.add_argument("repo_root", type=Path, help="Path to the repository root")
    parser.add_argument("target_file", type=Path, help="Path to the file being edited")
    parser.add_argument("--max-hops", type=int, default=2, help="Call-hop depth for tier 2 (default: 2)")
    parser.add_argument("--dump", type=Path, default=None,
                         help="Optional path to write the full compiled prompt string to")
    args = parser.parse_args()

    if not args.repo_root.is_dir():
        print(f"error: {args.repo_root} is not a directory", file=sys.stderr)
        return 1
    if not args.target_file.is_file():
        print(f"error: {args.target_file} is not a file", file=sys.stderr)
        return 1

    compiler = ContextCompiler(args.repo_root, max_hops=args.max_hops)
    compiled = compiler.compile(args.target_file)

    print(compiled.summary())

    if args.dump:
        args.dump.write_text(compiled.to_prompt_string(), encoding="utf-8")
        print(f"\nFull compiled prompt written to {args.dump}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
