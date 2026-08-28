import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description:
    "Compile reachability-based Python code context for an edit target. " +
    "Returns tier-1 full source for the target file, tier-2 interface skeletons " +
    "for reachable dependencies, and excludes everything else. " +
    "Use during OpenSpec apply when implementing a task with a known .py target " +
    "instead of broadly reading snekdo/ or tests/.",
  args: {
    target_file: tool.schema
      .string()
      .describe("Repo-relative path to the Python file being edited (e.g. snekdo/api.py)"),
    max_hops: tool.schema
      .number()
      .optional()
      .describe("Reachability depth for tier-2 skeletons (default 2)"),
  },
  async execute(args, context) {
    const worktree = context.worktree
    const script = path.join(worktree, "tools/context_compile.py")
    const hops = args.max_hops ?? 2
    const result =
      await Bun.$`python3 ${script} ${args.target_file} --repo-root ${worktree} --max-hops ${hops}`.text()
    return result
  },
})
