"""
compiler.py
===========
ContextCompiler — orchestrates the three-tier context strategy.

  Tier 1  Full source            the file actively being edited
  Tier 2  Skeletonized interface  files reachable within `max_hops` call hops
  Tier 3  Total exclusion         everything else in the repo

Produces a CompiledContext: the assembled prompt-ready text, plus token-count
diagnostics comparing this strategy against a naive full-repo dump, plus the
raw ReachabilityResult so callers can see (and disclose) what the resolver
missed rather than pretending it's exhaustive.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from skeletonizer import skeletonize_source
from symbol_resolver import SymbolResolver, ReachabilityResult

CHARS_PER_TOKEN = 4  # rough heuristic; swap in a real tokenizer for exact counts


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // CHARS_PER_TOKEN)


@dataclass
class TierEntry:
    path: Path
    tier: int
    content: str
    tokens: int
    hop_distance: Optional[int] = None


@dataclass
class CompiledContext:
    target_file: Path
    entries: List[TierEntry] = field(default_factory=list)
    excluded_count: int = 0
    total_repo_files: int = 0
    naive_dump_tokens: int = 0
    compiled_tokens: int = 0
    build_seconds: float = 0.0
    diagnostics: Optional[ReachabilityResult] = None

    def to_prompt_string(self) -> str:
        parts = []
        for entry in self.entries:
            label = "FULL SOURCE" if entry.tier == 1 else "SKELETON"
            parts.append(f"# ---- [{label}] {entry.path} ----\n{entry.content}")
        return "\n\n".join(parts)

    def reduction_pct(self) -> float:
        if self.naive_dump_tokens == 0:
            return 0.0
        return 100 * (1 - self.compiled_tokens / self.naive_dump_tokens)

    def summary(self) -> str:
        tier2 = sum(1 for e in self.entries if e.tier == 2)
        lines = [
            f"Target file: {self.target_file}",
            f"Repo files scanned: {self.total_repo_files}",
            "Tier 1 (full source): 1 file",
            f"Tier 2 (skeletonized): {tier2} files",
            f"Tier 3 (excluded): {self.excluded_count} files",
            f"Naive full-dump estimate: {self.naive_dump_tokens} tokens",
            f"Compiled context: {self.compiled_tokens} tokens",
            f"Reduction: {self.reduction_pct():.1f}%",
            f"Build time: {self.build_seconds * 1000:.2f} ms",
        ]
        if self.diagnostics:
            if self.diagnostics.dynamic_dispatch_files:
                lines.append(
                    f"Warning: {len(self.diagnostics.dynamic_dispatch_files)} file(s) use "
                    f"getattr()-based dynamic dispatch \u2014 targets may be missing from tier 2."
                )
            if self.diagnostics.decorator_hint_files:
                lines.append(
                    f"Warning: {len(self.diagnostics.decorator_hint_files)} file(s) use "
                    f"event-style decorators (e.g. @receiver) \u2014 handlers may be missing from tier 2."
                )
            if self.diagnostics.name_collisions:
                lines.append(
                    f"Note: {len(self.diagnostics.name_collisions)} call name(s) resolved to "
                    f"more than one file (name-only resolution) \u2014 tier 2 may include false positives."
                )
        return "\n".join(lines)


class ContextCompiler:
    def __init__(self, repo_root, max_hops: int = 2):
        self.root = Path(repo_root).resolve()
        self.max_hops = max_hops
        self.resolver = SymbolResolver(self.root, max_hops=max_hops)

    def compile(self, target_file) -> CompiledContext:
        start = time.perf_counter()
        target_path = Path(target_file).resolve()
        target_source = target_path.read_text(encoding="utf-8")

        reachability = self.resolver.resolve(target_path)

        entries = [
            TierEntry(
                path=target_path, tier=1, content=target_source,
                tokens=estimate_tokens(target_source), hop_distance=0,
            )
        ]

        for dep_path, hop in sorted(reachability.reachable.items(), key=lambda kv: kv[1]):
            try:
                source = dep_path.read_text(encoding="utf-8")
                skeleton, _ = skeletonize_source(source)
            except (ValueError, UnicodeDecodeError):
                continue
            entries.append(TierEntry(
                path=dep_path, tier=2, content=skeleton,
                tokens=estimate_tokens(skeleton), hop_distance=hop,
            ))

        all_py_files = list(self.resolver.index.path_to_module.keys())
        included_paths = {e.path for e in entries}
        excluded_count = len(all_py_files) - len(included_paths)

        naive_dump_tokens = 0
        for path in all_py_files:
            try:
                naive_dump_tokens += estimate_tokens(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue

        compiled_tokens = sum(e.tokens for e in entries)

        return CompiledContext(
            target_file=target_path,
            entries=entries,
            excluded_count=excluded_count,
            total_repo_files=len(all_py_files),
            naive_dump_tokens=naive_dump_tokens,
            compiled_tokens=compiled_tokens,
            build_seconds=time.perf_counter() - start,
            diagnostics=reachability,
        )
