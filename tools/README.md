# Agent tools

## context-compiler

Vendored from https://github.com/Emmimal/context-compiler (MIT).

Wrapper CLI for OpenCode and shell use:

```bash
python3 tools/context_compile.py snekdo/api.py --repo-root .
```

OpenCode exposes this as the `context-compile` tool (`.opencode/tools/context-compile.ts`).

Update the vendored copy:

```bash
rm -rf tools/context-compiler
git clone --depth 1 https://github.com/Emmimal/context-compiler.git tools/context-compiler
rm -rf tools/context-compiler/.git
```

Then re-apply the snekdo exclude patch in `tools/context-compiler/symbol_resolver.py` (`ModuleIndex.build`): skip `.venv` and `.opencode` in addition to upstream's `venv`, `node_modules`, etc.
