"""Context Compiler — a pure-Python, zero-dependency reachability + skeletonization
layer that decides what a coding agent actually sees before a request reaches the API.
"""

try:
    from .compiler import ContextCompiler, CompiledContext, TierEntry, estimate_tokens
    from .symbol_resolver import SymbolResolver, ReachabilityResult, ModuleIndex
    from .skeletonizer import CodeSkeletonizer, skeletonize_source
except ImportError:  # running from inside the repo directory rather than as a package
    from compiler import ContextCompiler, CompiledContext, TierEntry, estimate_tokens
    from symbol_resolver import SymbolResolver, ReachabilityResult, ModuleIndex
    from skeletonizer import CodeSkeletonizer, skeletonize_source

__all__ = [
    "ContextCompiler", "CompiledContext", "TierEntry", "estimate_tokens",
    "SymbolResolver", "ReachabilityResult", "ModuleIndex",
    "CodeSkeletonizer", "skeletonize_source",
]

__version__ = "0.1.0"
