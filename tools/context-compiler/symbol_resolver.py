"""
symbol_resolver.py
===================
Reachability analysis for the Context Compiler.

Given a target file inside a repository, the SymbolResolver builds an
approximate dependency graph: which other files in the repo are reachable
from the target file via (a) explicit imports and (b) name-only call
resolution, out to a configurable depth in call hops.

This is intentionally NOT a full type-aware call graph. It trades soundness
for speed and zero external dependencies. Three blind spots follow directly
from that trade-off, and the resolver surfaces them as diagnostics rather
than hiding them:

  1. Decorator-registered handlers (e.g. Django-style @receiver) have no
     direct AST link from sender to receiver — files using known event-style
     decorators are flagged, not resolved.
  2. Dynamic dispatch via getattr(module, name) is invisible to static
     analysis — files that call getattr() are flagged.
  3. Calls are resolved by bare name only (`.save()` matches every `save`
     method in the repo), which can pull in unrelated files — every name
     that resolves to more than one file is reported as a collision.
"""

from __future__ import annotations

import ast
import builtins
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

_BUILTIN_NAMES = set(dir(builtins))
KNOWN_EVENT_DECORATORS = {"receiver", "signal", "event", "on", "hook", "register", "route"}


@dataclass
class ModuleIndex:
    """Maps every .py file in a repo to its dotted module path, and back."""

    root: Path
    path_to_module: Dict[Path, str] = field(default_factory=dict)
    module_to_path: Dict[str, Path] = field(default_factory=dict)

    @classmethod
    def build(cls, root: Path) -> "ModuleIndex":
        index = cls(root=root)
        for py_file in root.rglob("*.py"):
            if any(
                part in {".git", "venv", ".venv", "__pycache__", "node_modules", ".opencode"}
                for part in py_file.parts
            ):
                continue
            rel = py_file.relative_to(root)
            parts = list(rel.with_suffix("").parts)
            if parts and parts[-1] == "__init__":
                parts = parts[:-1]
            module = ".".join(parts) if parts else rel.stem
            index.path_to_module[py_file] = module
            if module:
                index.module_to_path[module] = py_file
        return index

    def resolve_import(self, module_name: str) -> Optional[Path]:
        """Best-effort resolution of a dotted import name to a file in the repo.

        Tries the full dotted path first, then walks up parent packages, so
        `from myapp.utils import helper` resolves to myapp/utils.py even when
        `helper` isn't itself a submodule.
        """
        if module_name in self.module_to_path:
            return self.module_to_path[module_name]
        parts = module_name.split(".")
        while len(parts) > 1:
            parts.pop()
            candidate = ".".join(parts)
            if candidate in self.module_to_path:
                return self.module_to_path[candidate]
        return None


@dataclass
class FileSymbols:
    imported_modules: Set[str] = field(default_factory=set)
    called_names: Set[str] = field(default_factory=set)
    defined_names: Set[str] = field(default_factory=set)
    uses_dynamic_dispatch: bool = False
    uses_decorators: Set[str] = field(default_factory=set)


def _decorator_name(node: ast.expr) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return None


class _SymbolVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.symbols = FileSymbols()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.symbols.imported_modules.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self.symbols.imported_modules.add(node.module)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute):
            self.symbols.called_names.add(func.attr)
        elif isinstance(func, ast.Name):
            self.symbols.called_names.add(func.id)
            if func.id == "getattr":
                self.symbols.uses_dynamic_dispatch = True
        self.generic_visit(node)

    def _visit_func(self, node) -> None:
        self.symbols.defined_names.add(node.name)
        for deco in node.decorator_list:
            name = _decorator_name(deco)
            if name:
                self.symbols.uses_decorators.add(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_func(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_func(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.symbols.defined_names.add(node.name)
        self.generic_visit(node)


def extract_symbols(source: str) -> FileSymbols:
    tree = ast.parse(source)
    visitor = _SymbolVisitor()
    visitor.visit(tree)
    return visitor.symbols


@dataclass
class ReachabilityResult:
    reachable: Dict[Path, int] = field(default_factory=dict)  # path -> hop distance
    unresolved_calls: Set[str] = field(default_factory=set)
    dynamic_dispatch_files: Set[Path] = field(default_factory=set)
    decorator_hint_files: Dict[Path, Set[str]] = field(default_factory=dict)
    name_collisions: Dict[str, List[Path]] = field(default_factory=dict)


class SymbolResolver:
    """Builds an approximate reachability graph outward from a target file."""

    def __init__(self, repo_root, max_hops: int = 2) -> None:
        self.root = Path(repo_root).resolve()
        self.max_hops = max_hops
        self.index = ModuleIndex.build(self.root)
        self._symbol_table: Optional[Dict[str, List[Path]]] = None

    def _global_symbol_table(self) -> Dict[str, List[Path]]:
        """name -> [files defining a function/class with that name].

        Built lazily and cached. Used only to resolve bare-name calls that
        imports alone don't explain — this is the source of the documented
        name-collision limitation.
        """
        if self._symbol_table is not None:
            return self._symbol_table
        table: Dict[str, List[Path]] = {}
        for path in self.index.path_to_module:
            try:
                source = path.read_text(encoding="utf-8")
                symbols = extract_symbols(source)
            except (SyntaxError, UnicodeDecodeError):
                continue
            for name in symbols.defined_names:
                table.setdefault(name, []).append(path)
        self._symbol_table = table
        return table

    def resolve(self, target_file) -> ReachabilityResult:
        target_path = Path(target_file).resolve()
        result = ReachabilityResult()
        visited = {target_path}
        symbol_table = self._global_symbol_table()

        hop = 0
        current_layer = [target_path]
        while current_layer and hop < self.max_hops:
            hop += 1
            next_layer: List[Path] = []
            for file_path in current_layer:
                try:
                    source = file_path.read_text(encoding="utf-8")
                    symbols = extract_symbols(source)
                except (SyntaxError, UnicodeDecodeError):
                    continue

                if symbols.uses_dynamic_dispatch:
                    result.dynamic_dispatch_files.add(file_path)

                event_decorators = symbols.uses_decorators & KNOWN_EVENT_DECORATORS
                if event_decorators:
                    result.decorator_hint_files[file_path] = event_decorators

                # (a) explicit imports
                for module_name in symbols.imported_modules:
                    resolved = self.index.resolve_import(module_name)
                    if resolved and resolved not in visited:
                        visited.add(resolved)
                        result.reachable[resolved] = hop
                        next_layer.append(resolved)

                # (b) name-only call resolution
                for called_name in symbols.called_names:
                    if called_name in _BUILTIN_NAMES or called_name.startswith("__"):
                        continue
                    candidates = symbol_table.get(called_name)
                    if not candidates:
                        result.unresolved_calls.add(called_name)
                        continue
                    if len(candidates) > 1:
                        result.name_collisions[called_name] = candidates
                    for candidate in candidates:
                        if candidate not in visited:
                            visited.add(candidate)
                            result.reachable[candidate] = hop
                            next_layer.append(candidate)

            current_layer = next_layer

        result.reachable.pop(target_path, None)
        return result
