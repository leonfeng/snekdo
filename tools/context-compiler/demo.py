"""
demo.py
=======
Five runnable demos for the Context Compiler.

Demos 1-4 build a small synthetic repo in a temp directory so the reachability
analysis, skeletonization, and known failure modes (signals, dynamic dispatch,
name collisions) are all reproducible without needing an external codebase.

Demo 5 runs the compiler against its OWN source directory — a real, honest
benchmark with numbers anyone running this script can reproduce, rather than
numbers from a repo the reader doesn't have access to.

Run:
    python demo.py
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from skeletonizer import skeletonize_source
from symbol_resolver import SymbolResolver
from compiler import ContextCompiler


def _build_synthetic_repo(root: Path) -> None:
    """A small Django-flavored repo built to reliably trip all three
    documented resolver blind spots: signals, getattr dispatch, and a
    name collision on `.save()`.
    """
    (root / "app").mkdir(parents=True)
    (root / "app" / "handlers").mkdir()

    (root / "app" / "__init__.py").write_text("", encoding="utf-8")
    (root / "app" / "handlers" / "__init__.py").write_text("", encoding="utf-8")

    (root / "app" / "models.py").write_text('''
"""User model."""


class User:
    """A registered user."""

    def __init__(self, name):
        self.name = name

    def save(self):
        """Persist the user record."""
        print(f"saving user {self.name}")
''', encoding="utf-8")

    (root / "app" / "models_order.py").write_text('''
"""Order model -- defines a second, unrelated `save()`."""


class Order:
    """A purchase order."""

    def __init__(self, order_id):
        self.order_id = order_id

    def save(self):
        """Persist the order record."""
        print(f"saving order {self.order_id}")
''', encoding="utf-8")

    (root / "app" / "services.py").write_text('''
"""Notification service, registered via a signal-style decorator."""


def receiver(signal_name):
    def wrapper(func):
        return func
    return wrapper


@receiver("user_saved")
def notify_on_save(user):
    """React to a user being saved. No caller imports this directly."""
    print(f"notifying about {user.name}")


def build_summary(user):
    """Builds a short summary string for a user."""
    return f"User: {user.name}"
''', encoding="utf-8")

    (root / "app" / "handlers" / "handler_email.py").write_text('''
"""Reached only via getattr() dynamic dispatch -- invisible to static analysis."""


def handle(payload):
    """Send an email notification."""
    print(f"emailing: {payload}")
''', encoding="utf-8")

    (root / "app" / "handlers" / "handler_sms.py").write_text('''
"""Also reached only via getattr() dynamic dispatch."""


def handle(payload):
    """Send an SMS notification."""
    print(f"texting: {payload}")
''', encoding="utf-8")

    (root / "app" / "utils.py").write_text('''
"""Unrelated helper module -- never imported or called by views.py.

Should end up correctly excluded (tier 3), not skeletonized.
"""


def unrelated_helper():
    """Not reachable from views.py by any path."""
    return 42
''', encoding="utf-8")

    (root / "app" / "views.py").write_text('''
"""The file a developer is actively editing -- this is Tier 1 (full source)."""

import importlib
from app.models import User
from app.services import build_summary


def dispatch_handler(name, payload):
    """Looks up a handler module by name at runtime -- getattr()-based
    dynamic dispatch that the Symbol Resolver cannot trace statically."""
    module = importlib.import_module(f"app.handlers.handler_{name}")
    handler = getattr(module, "handle")
    return handler(payload)


def save_user_view(request_name):
    """Creates a user and saves it. `.save()` is resolved by bare name,
    so it will also pull in Order.save() from models_order.py."""
    user = User(request_name)
    user.save()
    return build_summary(user)
''', encoding="utf-8")


def demo_1_skeletonizer() -> None:
    print("=" * 70)
    print("DEMO 1: Skeletonizer strips bodies, keeps signatures + docstrings")
    print("=" * 70)

    source = '''
class PaymentProcessor:
    """Handles payment capture."""

    def charge(self, amount, currency="USD"):
        """Charge a card for `amount` in `currency`."""
        client = get_gateway_client()
        result = client.charge(amount=amount, currency=currency)
        if not result.ok:
            raise PaymentError(result.message)
        return result.transaction_id

TAX_RATE = 0.08  # module-level statement -- dropped from the skeleton
'''
    skeleton, stripped = skeletonize_source(source)
    print(f"\nOriginal: {len(source)} chars | Skeleton: {len(skeleton)} chars "
          f"| {stripped} function body stripped\n")
    print(skeleton)


def demo_2_reachability(repo_root: Path) -> None:
    print("\n" + "=" * 70)
    print("DEMO 2: Reachability analysis on the synthetic repo")
    print("=" * 70)

    target = repo_root / "app" / "views.py"
    resolver = SymbolResolver(repo_root, max_hops=2)
    result = resolver.resolve(target)

    print(f"\nTarget: {target.relative_to(repo_root)}")
    print(f"Reachable files ({len(result.reachable)}):")
    for path, hop in sorted(result.reachable.items(), key=lambda kv: kv[1]):
        print(f"  hop {hop}: {path.relative_to(repo_root)}")

    print(f"\nDynamic dispatch flagged in: "
          f"{[p.relative_to(repo_root) for p in result.dynamic_dispatch_files]}")
    print(f"Event-decorator hints flagged in: "
          f"{ {p.relative_to(repo_root): v for p, v in result.decorator_hint_files.items()} }")
    print(f"Name collisions: "
          f"{ {k: [p.relative_to(repo_root) for p in v] for k, v in result.name_collisions.items()} }")

    missed = {repo_root / "app" / "handlers" / "handler_email.py",
              repo_root / "app" / "handlers" / "handler_sms.py",
              repo_root / "app" / "services.py"}
    for path in missed:
        note = "correctly reached" if path in result.reachable else "MISSED (as expected)"
        try:
            label = path.relative_to(repo_root)
        except ValueError:
            label = path
        if "handler" in str(path):
            print(f"  {label}: {note} -- getattr() dispatch is invisible to static analysis")


def demo_3_full_compile(repo_root: Path) -> None:
    print("\n" + "=" * 70)
    print("DEMO 3: Full three-tier compile")
    print("=" * 70)

    compiler = ContextCompiler(repo_root, max_hops=2)
    compiled = compiler.compile(repo_root / "app" / "views.py")

    print()
    print(compiled.summary())
    print("\n--- First 600 chars of compiled prompt string ---")
    print(compiled.to_prompt_string()[:600])
    print("...")


def demo_4_failure_modes(repo_root: Path) -> None:
    print("\n" + "=" * 70)
    print("DEMO 4: The three documented failure modes, explicitly")
    print("=" * 70)
    print('''
1. Signals / event decorators: notify_on_save() in services.py is decorated
   with @receiver but never directly imported or called by views.py -- there
   is no AST edge from sender to receiver, so it is invisible to the resolver
   even though it would fire at runtime. The resolver only surfaces this as a
   *hint* (via KNOWN_EVENT_DECORATORS), not a resolved dependency.

2. Dynamic dispatch: dispatch_handler() in views.py resolves its target with
   importlib.import_module() + getattr() using an f-string. Both handler
   files are structurally unreachable to static analysis and are correctly
   flagged as tier-3 excluded, not tier-2 included -- silently wrong context
   is worse than no context, so the resolver flags rather than guesses.

3. Name collisions: `user.save()` is resolved by bare method name only, so
   the resolver cannot distinguish it from Order.save() in models_order.py.
   Both get pulled into tier 2. This does not break anything -- it just
   slightly inflates the token count with a false positive.
''')


def demo_5_self_benchmark() -> None:
    print("\n" + "=" * 70)
    print("DEMO 5: Self-benchmark -- compiling THIS repository's own source")
    print("(reproducible by anyone running this script, not a private dataset)")
    print("=" * 70)

    repo_root = Path(__file__).resolve().parent
    compiler = ContextCompiler(repo_root, max_hops=2)
    compiled = compiler.compile(repo_root / "compiler.py")

    print()
    print(compiled.summary())


def main() -> None:
    demo_1_skeletonizer()

    tmp_dir = Path(tempfile.mkdtemp(prefix="context_compiler_demo_"))
    try:
        _build_synthetic_repo(tmp_dir)
        demo_2_reachability(tmp_dir)
        demo_3_full_compile(tmp_dir)
        demo_4_failure_modes(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    demo_5_self_benchmark()


if __name__ == "__main__":
    main()
