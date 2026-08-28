# context-compiler

A pure-Python reachability and skeletonization layer that decides what a coding agent actually sees before a request reaches the API.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

Most coding agents build a "repo map" — file paths and source concatenated together — and send the whole thing to the model on the assumption that a big enough window makes the excess harmless. This library does what a real compiler does instead: resolve what a target file actually depends on, reduce the rest to interfaces, and exclude everything else, before any of it reaches the API.

Read the full write-up on Towards Data Science → [Graph Engineering Isn’t About More Connections—It’s About Which Ones Get Used](https://towardsdatascience.com/author/emmimalp-alexander/)

## What It Does

```
Target file ──▶ Symbol Resolver ──▶ Skeletonizer ──▶ ContextCompiler ──▶ CompiledContext
              (reachability graph)  (AST body-strip)   (three-tier assembly)
```

Three passes, one `compile()` call:

| Pass | Job |
|---|---|
| Symbol Resolution | traces imports and name-only call sites outward from a target file to build an approximate dependency graph, out to a configurable hop depth |
| Interface Extraction | an `ast.NodeTransformer` that strips function/method bodies, keeping signatures, decorators, type hints, and docstrings |
| Context Assembly | assigns every file in the repo to one of three tiers and reports the token cost against a naive full-repo dump |

## Installation

```bash
git clone https://github.com/Emmimal/context-compiler.git
cd context-compiler
python demo.py                    # no dependencies to install — standard library only
```

No other dependencies. Everything runs on `ast`, `pathlib`, and `dataclasses`. Requires Python 3.9+ (uses `ast.unparse`).

## Quick Start

```python
from compiler import ContextCompiler

compiler = ContextCompiler(repo_root="/path/to/your/repo", max_hops=2)
compiled = compiler.compile(target_file="/path/to/your/repo/app/views.py")

print(compiled.summary())
prompt_text = compiled.to_prompt_string()
```

## Running the Demos

Five runnable demos, four built on a synthetic repo constructed to trip every documented failure mode, one a real self-benchmark:

```bash
python demo.py
```

| Demo | What It Shows |
|---|---|
| 1 | Skeletonizer stripping a function body while keeping its docstring |
| 2 | Reachability analysis — what gets found, what gets missed, and why |
| 3 | A full three-tier compile with token diagnostics |
| 4 | The three known failure modes, explained against the same synthetic repo |
| 5 | Self-benchmark — the compiler run against its own source directory |

## Running the CLI Against a Real Repo

```bash
python benchmark.py /path/to/repo /path/to/repo/target_file.py --max-hops 2
```

First argument is the repository root, second is the file being treated as "actively edited" — that file gets full-source treatment (Tier 1) while everything reachable gets skeletonized (Tier 2) and everything else is excluded (Tier 3). Add `--dump PATH` to write the full compiled prompt string to a file.

## Configuration Reference

```python
ContextCompiler(
    repo_root="...",   # repository root to index
    max_hops=2,         # call-hop depth for tier 2 (1 = direct imports/calls only)
)

compiler.compile(target_file="...")   # returns a CompiledContext
```

Tuning `max_hops`:

| `max_hops` | What reaches Tier 2 | Trade-off |
|---|---|---|
| 1 | Direct imports and calls only | Smallest payload; a secondary helper may be missed |
| 2 | Direct dependencies plus one layer out | Default used for every benchmark below |
| 3+ | Wider transitive neighborhood | Approaches a full call graph again as depth grows |

`CompiledContext` fields: `entries` (list of `TierEntry`), `excluded_count`, `total_repo_files`, `naive_dump_tokens`, `compiled_tokens`, `build_seconds`, `diagnostics` (the raw `ReachabilityResult`), plus `.summary()`, `.to_prompt_string()`, and `.reduction_pct()`.

## Project Structure

```
context-compiler/
├── __init__.py                  # Public API surface
├── skeletonizer.py              # CodeSkeletonizer (ast.NodeTransformer) + skeletonize_source()
├── symbol_resolver.py           # SymbolResolver + ModuleIndex + ReachabilityResult
├── compiler.py                  # ContextCompiler + CompiledContext (orchestrator)
├── demo.py                      # Five runnable demos, including the self-benchmark
├── benchmark.py                 # CLI to run the compiler against any real repo
└── test_context_compiler.py     # unittest suite (stdlib only, no pytest dependency)
```

## Running the Tests

```bash
python -m unittest test_context_compiler -v
```

14 tests, standard library only — covers skeletonization, reachability, all three documented failure modes, and tier assignment.

## Performance

Measured across repeated runs, Python 3.12, CPU only, standard library only, `max_hops=2`:

| Repository | Files | Naive tokens | Compiled tokens | Reduction | Build time |
|---|---|---|---|---|---|
| context-compiler (self) | 7 | 9,379 | 2,867 | 69.4% | ~43–61 ms |
| loop-engine (external) | 12 | 13,254 | 3,404 | 74.3% | ~66–73 ms |

Token counts use a `characters // 4` heuristic, not a real tokenizer — treat the reduction percentage as the meaningful figure. Swap in `tiktoken` in `compiler.py`'s `estimate_tokens()` for exact counts.

## When to Use This

Worth it when you have:
- Multi-file agent tasks where most of the codebase is irrelevant to the file being edited
- A context budget you're actively trying to protect
- A codebase that favors explicit imports over heavy dynamic dispatch, so the resolver's blind spots stay rare

Skip it when you have:
- Single-file scripts or small repos where a naive dump is already cheap
- A codebase built heavily around signals, event buses, or `getattr()`-based plugin loading, without also maintaining an explicit registry the resolver can read

## Known Limitations

- The Symbol Resolver is not a type-aware call graph. Calls are resolved by bare name only, which produces three specific, reproducible blind spots, all demonstrated in `demo.py` Demo 4:
  - **Dynamic dispatch** via `getattr()` or `importlib.import_module()` is invisible to static analysis; affected files are excluded and flagged, not silently guessed at.
  - **Event-style decorators** (`@receiver` and similar) create a sender-to-handler relationship with no direct AST edge; the resolver surfaces a hint from a fixed decorator-name list, not a resolved dependency.
  - **Name collisions** — `.save()` matches every `save` defined anywhere in the repo, which can pull unrelated files into Tier 2. This inflates token count but never silently drops something that should have been included.
- Token estimation uses `1 token ≈ 4 characters`, not a real tokenizer.
- `ModuleIndex` is rebuilt from scratch on every `compile()` call — no caching across runs.
- Tiering is strictly binary: a hop-1 dependency and a hop-2 dependency receive identical treatment once both clear the resolver.
- Requires Python 3.9+.

## License

MIT
