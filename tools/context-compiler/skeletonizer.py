"""
skeletonizer.py
================
AST-based body stripping.

Reduces a Python source file to its structural skeleton: imports, class and
function signatures, and docstrings, with all executable logic removed and
replaced by a single `...` placeholder.

Used by ContextCompiler to represent "reachable but not actively edited"
dependencies without spending tokens on implementation detail the model
doesn't need in order to navigate or reason about the interface.

This intentionally drops:
  - module-level executable statements (assignments, `if __name__ == "__main__"`
    blocks, top-level function calls) — they are neither structure nor interface
  - function/method bodies (replaced with a docstring, if present, plus `...`)

It intentionally keeps:
  - imports
  - class definitions and their nesting
  - function/method signatures, including decorators, defaults, and type hints
  - docstrings (module, class, and function level)
"""

from __future__ import annotations

import ast
from typing import Optional, Tuple


class CodeSkeletonizer(ast.NodeTransformer):
    """Strips function and method bodies, leaving only signatures and docstrings."""

    def __init__(self) -> None:
        super().__init__()
        self.functions_stripped = 0

    @staticmethod
    def _docstring_node(node: ast.AST) -> Optional[ast.Expr]:
        body = getattr(node, "body", None)
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            return body[0]
        return None

    def _strip_body(self, node):
        docstring = self._docstring_node(node)
        placeholder = ast.Expr(value=ast.Constant(value=Ellipsis))
        ast.copy_location(placeholder, node)
        node.body = [docstring, placeholder] if docstring else [placeholder]
        self.functions_stripped += 1
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        return self._strip_body(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return self._strip_body(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.generic_visit(node)
        if not node.body:
            placeholder = ast.Expr(value=ast.Constant(value=Ellipsis))
            ast.copy_location(placeholder, node)
            node.body = [placeholder]
        return node

    def visit_Module(self, node: ast.Module):
        keep_types = (ast.Import, ast.ImportFrom, ast.ClassDef,
                      ast.FunctionDef, ast.AsyncFunctionDef)
        new_body = []
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, keep_types):
                new_body.append(self.visit(stmt))
            elif (
                i == 0
                and isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)
            ):
                new_body.append(stmt)  # module docstring
            # everything else (top-level assignments, side-effecting calls,
            # __main__ guards, etc.) is dropped from the skeleton
        node.body = new_body
        return node


def skeletonize_source(source: str) -> Tuple[str, int]:
    """Parse `source`, strip implementation bodies, return (skeleton_text, funcs_stripped).

    Raises ValueError if the source fails to parse — callers should treat a
    parse failure as a tier-2 miss, not silently drop the file from diagnostics.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"could not parse source for skeletonization: {exc}") from exc

    skeletonizer = CodeSkeletonizer()
    new_tree = skeletonizer.visit(tree)
    ast.fix_missing_locations(new_tree)
    return ast.unparse(new_tree), skeletonizer.functions_stripped
