"""
test_context_compiler.py
=========================
Standard-library-only test suite (unittest). No pytest dependency required.

Run:
    python -m unittest test_context_compiler -v
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from skeletonizer import skeletonize_source
from symbol_resolver import SymbolResolver
from compiler import ContextCompiler, estimate_tokens


class TestSkeletonizer(unittest.TestCase):
    def test_strips_function_body_keeps_docstring(self):
        source = '''
def add(a, b):
    """Add two numbers."""
    result = a + b
    return result
'''
        skeleton, stripped = skeletonize_source(source)
        self.assertEqual(stripped, 1)
        self.assertIn("def add(a, b):", skeleton)
        self.assertIn('"""Add two numbers."""', skeleton)
        self.assertNotIn("result = a + b", skeleton)
        self.assertIn("...", skeleton)

    def test_strips_body_without_docstring(self):
        source = "def f(x):\n    return x * 2\n"
        skeleton, stripped = skeletonize_source(source)
        self.assertEqual(stripped, 1)
        self.assertNotIn("return x * 2", skeleton)

    def test_drops_module_level_side_effects(self):
        source = "import os\nX = 1\nprint('side effect')\ndef f():\n    pass\n"
        skeleton, _ = skeletonize_source(source)
        self.assertNotIn("X = 1", skeleton)
        self.assertNotIn("print(", skeleton)
        self.assertIn("import os", skeleton)

    def test_preserves_class_nesting(self):
        source = '''
class Outer:
    class Inner:
        def method(self):
            return 1
'''
        skeleton, _ = skeletonize_source(source)
        self.assertIn("class Outer:", skeleton)
        self.assertIn("class Inner:", skeleton)

    def test_raises_on_invalid_syntax(self):
        with self.assertRaises(ValueError):
            skeletonize_source("def f(:\n  pass")


class TestSymbolResolver(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "a.py").write_text(
            "from b import helper\n\ndef use():\n    return helper()\n"
        )
        (self.tmp / "b.py").write_text(
            "def helper():\n    return 1\n"
        )
        (self.tmp / "unrelated.py").write_text(
            "def never_called():\n    return 0\n"
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_resolves_direct_import(self):
        resolver = SymbolResolver(self.tmp, max_hops=2)
        result = resolver.resolve(self.tmp / "a.py")
        reached = {p.name for p in result.reachable}
        self.assertIn("b.py", reached)
        self.assertNotIn("unrelated.py", reached)

    def test_flags_dynamic_dispatch(self):
        (self.tmp / "c.py").write_text(
            "import importlib\n\ndef dispatch(name):\n"
            "    mod = importlib.import_module(name)\n"
            "    return getattr(mod, 'run')()\n"
        )
        resolver = SymbolResolver(self.tmp, max_hops=1)
        result = resolver.resolve(self.tmp / "c.py")
        self.assertIn(self.tmp / "c.py", result.dynamic_dispatch_files)

    def test_flags_name_collision(self):
        (self.tmp / "model_x.py").write_text("class X:\n    def save(self):\n        pass\n")
        (self.tmp / "model_y.py").write_text("class Y:\n    def save(self):\n        pass\n")
        (self.tmp / "caller.py").write_text(
            "from model_x import X\n\ndef go():\n    x = X()\n    x.save()\n"
        )
        resolver = SymbolResolver(self.tmp, max_hops=1)
        result = resolver.resolve(self.tmp / "caller.py")
        self.assertIn("save", result.name_collisions)
        self.assertEqual(len(result.name_collisions["save"]), 2)

    def test_flags_event_decorator_hint(self):
        (self.tmp / "signals.py").write_text(
            "def receiver(sig):\n    def wrap(f):\n        return f\n    return wrap\n\n"
            "@receiver('saved')\ndef on_save(sender):\n    pass\n"
        )
        resolver = SymbolResolver(self.tmp, max_hops=1)
        result = resolver.resolve(self.tmp / "signals.py")
        self.assertIn(self.tmp / "signals.py", result.decorator_hint_files)

    def test_respects_max_hops(self):
        (self.tmp / "d.py").write_text("from e import far\n\ndef use():\n    return far()\n")
        (self.tmp / "e.py").write_text("def far():\n    return 1\n")
        (self.tmp / "chain_start.py").write_text("from d import use\n\ndef go():\n    return use()\n")

        resolver_1hop = SymbolResolver(self.tmp, max_hops=1)
        result_1hop = resolver_1hop.resolve(self.tmp / "chain_start.py")
        reached_1 = {p.name for p in result_1hop.reachable}
        self.assertIn("d.py", reached_1)
        self.assertNotIn("e.py", reached_1)  # e.py is 2 hops away

        resolver_2hop = SymbolResolver(self.tmp, max_hops=2)
        result_2hop = resolver_2hop.resolve(self.tmp / "chain_start.py")
        reached_2 = {p.name for p in result_2hop.reachable}
        self.assertIn("e.py", reached_2)


class TestContextCompiler(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "target.py").write_text(
            "from dep import helper\n\ndef run():\n    return helper()\n"
        )
        (self.tmp / "dep.py").write_text(
            '"""A dependency."""\n\ndef helper():\n    """Help."""\n    return 42\n'
        )
        (self.tmp / "excluded.py").write_text(
            "def unrelated():\n    return 'never reached'\n"
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_tier_assignment(self):
        compiler = ContextCompiler(self.tmp, max_hops=2)
        compiled = compiler.compile(self.tmp / "target.py")

        tier1 = [e for e in compiled.entries if e.tier == 1]
        tier2 = [e for e in compiled.entries if e.tier == 2]

        self.assertEqual(len(tier1), 1)
        self.assertEqual(tier1[0].path, (self.tmp / "target.py").resolve())
        self.assertEqual(len(tier2), 1)
        self.assertEqual(tier2[0].path, (self.tmp / "dep.py").resolve())
        self.assertEqual(compiled.excluded_count, 1)  # excluded.py

    def test_tier1_is_full_source_tier2_is_skeleton(self):
        compiler = ContextCompiler(self.tmp, max_hops=2)
        compiled = compiler.compile(self.tmp / "target.py")

        tier1_entry = next(e for e in compiled.entries if e.tier == 1)
        tier2_entry = next(e for e in compiled.entries if e.tier == 2)

        self.assertIn("return helper()", tier1_entry.content)  # full logic kept
        self.assertNotIn("return 42", tier2_entry.content)     # body stripped
        self.assertIn("def helper():", tier2_entry.content)    # signature kept

    def test_compiled_tokens_less_than_naive_dump(self):
        compiler = ContextCompiler(self.tmp, max_hops=2)
        compiled = compiler.compile(self.tmp / "target.py")
        self.assertLess(compiled.compiled_tokens, compiled.naive_dump_tokens)
        self.assertGreater(compiled.reduction_pct(), 0)

    def test_estimate_tokens_nonzero_for_nonempty_string(self):
        self.assertGreaterEqual(estimate_tokens("x" * 100), 1)


if __name__ == "__main__":
    unittest.main()
