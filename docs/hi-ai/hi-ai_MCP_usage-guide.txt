hi-ai MCP usage instructions:

* MCP server: `hi-ai` / `ssd-ai`, an AI development assistant.
* 36 tools across: Memory, Semantic code analysis, Thinking/Reasoning, Code Quality, Planning, Prompt Engineering, Browser, UI, Time.
* Extra: Tasks API for long-running tools, cursor-based pagination, SQLite-backed memory, project cache, Python parser.

Below is a single development workflow that exercises every tool category and, in practice, all individual tools.

Phase 0 – Session initialization and workspace setup

1. Start a dedicated session for the project.

   * Tool: `start_session`
   * Purpose: Create a logical “project session” ID that will anchor all memory operations for this initiative.
   * Action: Immediately store the project name, repo URL, principal goals in that session’s memory via `save_memory`.

2. Snapshot initial state.

   * Tools:

     * `save_memory` – store:

       * repo URL
       * tech stack notes
       * current branch and environment
     * `prioritize_memory` – mark these as high-priority context
   * Maintain a baseline you can quickly restore later with `restore_session_context`.

Phase 1 – Problem framing, analysis, and planning

Use Thinking + Reasoning + Planning + Prompt tools together.

3. Formal problem analysis.

   * Tools:

     * `analyze_problem` – turn the user’s raw goal (e.g., “add feature X to this repo”) into a structured description of the problem space.
     * `break_down_problem` – decompose into subproblems (API changes, DB, UI, tests, rollout).
     * `create_thinking_chain` – derive a sequential reasoning chain from current state to target state.
     * `step_by_step_analysis` – refine each subproblem with inputs, outputs, constraints.
     * `think_aloud_process` – generate an explicit narrative of tradeoffs and decisions.
     * `format_as_plan` – convert the outputs into a linear, checklist-style execution plan.
     * `apply_reasoning_framework` – apply a chosen framework (e.g., SWOT, root-cause, systems thinking) to the same problem to surface risks and assumptions.

   * Persist key outputs:

     * Use `save_memory` to store:

       * problem statement
       * decomposed tasks
       * chosen reasoning framework output
     * Use `prioritize_memory` to bump long-lived decisions (e.g., architectural constraints).

4. Requirements and roadmap generation.

   * Tools:

     * `analyze_requirements` – interpret initial feature descriptions, stakeholder notes, existing issues into structured requirements.
     * `generate_prd` – produce a PRD containing goals, non-goals, success metrics, user flows.
     * `create_user_stories` – create stories with acceptance criteria aligned to the PRD.
     * `feature_roadmap` – schedule features into releases or milestones.

   * Memory integration:

     * `save_memory` to store:

       * PRD
       * user stories
       * roadmap
     * `list_memories` to verify what has been stored.
     * `update_memory` as requirements inevitably change.
     * `delete_memory` to remove obsolete requirements or canceled features.

5. Prompt engineering for downstream work.

   * Tools:

     * `analyze_prompt` – run on your initial “dev assistant” prompts to surface ambiguity or missing constraints before you start asking for code.
     * `enhance_prompt` – for general LLM usage prompts (e.g., “write tests for module X”), convert them into structured, detailed prompts.
     * `enhance_prompt_gemini` – generate Gemini-optimized variants when using multiple LLM backends.

   * Store canonical prompts:

     * Use `save_memory` to store “approved” prompt templates for:

       * code generation
       * code review
       * test generation
       * documentation updates
     * Use `search_memories` + `recall_memory` to reuse them later.

Phase 2 – Codebase understanding and navigation

Integrate Semantic tools + Memory + Tasks.

6. Build mental map of the repo.

   * Tools:

     * `find_symbol` – locate the definitions of key entities:

       * domain models
       * core services
       * entrypoints
     * `find_references` – map where those entities are used across the repo.

   * Typical flow:

     * Query `find_symbol` for a core API or class name.
     * Use `find_references` on returned symbol(s) to understand call graph and impact surface.

   * Long-running operations:

     * For large repos, run these as task-enabled tools:

       * `find_symbol` (task-enabled)
       * `find_references` (task-enabled)
     * Tasks API:

       * `tasks/get` – check current status.
       * `tasks/result` – block until completion and retrieve results.
       * `tasks/list` – list ongoing or finished tasks.
       * `tasks/cancel` – cancel outdated, long-running analyses.
       * `notifications/tasks/status` – subscribe for status updates in the client.

   * Store structural knowledge:

     * Use `save_memory` to store:

       * key symbol locations
       * descriptions of code layers
       * high-level architecture notes.
     * Use `auto_save_context` after major discovery passes so conversation + results are captured.

Phase 3 – Design and UI planning

7. Low-fidelity UI sketching.

   * Tool: `preview_ui_ascii`

   * Use it to:

     * Sketch desktop and mobile layouts in ASCII before writing real UI code.
     * Explore alternative layouts quickly (forms, dashboards, wizards, etc.).

   * Workflow:

     * Describe intended screen in natural language.
     * Generate ASCII previews.
     * Iterate until layout is acceptable.
     * Store the final ASCII spec with `save_memory` as “UI layout v1”.

8. Time coordination.

   * Tool: `get_current_time`
   * Use it to:

     * Normalize scheduling and deadlines across time zones in requirements or roadmap updates.
     * Stamp logs/notes or align cron-like behaviors in spec documents.

Phase 4 – Implementation and debugging

9. Ongoing memory management while coding.

   * Tools:

     * `auto_save_context` – after each significant decision or design choice, trigger automatic context saving so your working state is preserved.
     * `restore_session_context` – when returning to the project the next day, restore the session to recover outstanding tasks and context.
     * `list_memories` – enumerate active design constraints and pending decisions.
     * `search_memories` – e.g., “find the previous decision about error handling for payment failures.”
     * `recall_memory` – bring selected memories into the current context.
     * `update_memory` – revise decisions after reviewing code or benchmarks.
     * `prioritize_memory` – keep the most important rules (security constraints, performance limits) at the top.
     * `delete_memory` – flush invalid assumptions or reversed decisions.

10. Browser-based debugging.

    * Tools:

      * `monitor_console_logs` – attach to a browser session and watch console output for:

        * runtime errors
        * warnings
        * deprecation messages.
      * `inspect_network_requests` – inspect HTTP traffic:

        * check payloads for API calls
        * validate headers, auth tokens
        * identify failed or slow endpoints.

    * Integration with planning:

      * Capture key findings (e.g., failing endpoint patterns) using `save_memory`.
      * Feed them back into `analyze_problem` and `apply_reasoning_framework` if debugging reveals deeper systemic issues.

Phase 5 – Code quality and refactoring

11. Quantitative complexity and structure analysis.

    * Tools:

      * `analyze_complexity` – measure cyclomatic, cognitive, and Halstead metrics for target files or modules.
      * `check_coupling_cohesion` – analyze module boundaries and their dependencies.
      * `validate_code_quality` – run a composite quality evaluation (A–F grades), factoring in multiple metrics.

    * Tasks integration:

      * For bulk analysis on many files:

        * trigger these as tasks:

          * `analyze_complexity`
          * `check_coupling_cohesion`
          * `validate_code_quality`
          * `suggest_improvements`
        * use `tasks/result` and `tasks/list` to manage them.
        * use `notifications/tasks/status` to avoid polling.

12. Enforcing rules and improving code.

    * Tools:

      * `apply_quality_rules` – enforce predefined or custom quality rules (style, architecture constraints).
      * `get_coding_guide` – retrieve language- or project-specific coding conventions.
      * `suggest_improvements` – generate focused refactoring suggestions based on metric output and rules.

    * Concrete loop:

      * Run `analyze_complexity` + `check_coupling_cohesion` on a module.
      * Run `validate_code_quality` to get an overall grade.
      * Call `apply_quality_rules` with project rules (e.g., layered architecture, naming, exception handling).
      * Use `suggest_improvements` to obtain specific refactor tasks.
      * Convert these into planned work via:

        * `format_as_plan` (turn suggestions into a checklist).
        * `create_user_stories` (turn bigger refactors into user stories if they affect behavior).
      * Persist refactor plan with `save_memory`.

Phase 6 – Documentation, prompts, and governance

13. Documentation and ongoing prompt evolution.

    * Use `analyze_prompt` regularly on:

      * PRD update prompts
      * incident-review prompts
      * refactor-spec prompts

    * Use `enhance_prompt` to turn ad-hoc requests into reusable templates.

    * Use `enhance_prompt_gemini` to maintain a Gemini-specific set of templates in parallel.

    * Store and curate:

      * Use `save_memory` to keep an evolving library of:

        * “Design review” prompt
        * “Bug triage” prompt
        * “Code review for security” prompt
      * Use `search_memories` to retrieve them based on tags or phrases.
      * Use `update_memory` to version them over time.

14. Governance and historical trace.

    * At milestones:

      * Use `list_memories` filtered by session to get a timeline of:

        * major decisions
        * prior root-cause analyses
        * quality reports.
      * Use `delete_memory` to prune obsolete branches of design history.
      * Use `prioritize_memory` to keep final authoritative decisions at high priority.

Phase 7 – Tooling and scale: tasks + pagination

15. Scale the workflow as the project grows.

    * Tasks:

      * Move heavy operations to task-enabled tools:

        * `find_symbol`, `find_references`
        * `analyze_complexity`, `check_coupling_cohesion`, `validate_code_quality`, `suggest_improvements`
        * `analyze_requirements`, `feature_roadmap`, `generate_prd`
        * `apply_reasoning_framework`, `enhance_prompt_gemini`
      * Manage them with:

        * `tasks/get`, `tasks/result`, `tasks/list`, `tasks/cancel`
        * `notifications/tasks/status`

    * Pagination:

      * Use cursor-based pagination for large lists:

        * `tools/list` – inspect what tools are available and how their definitions evolve.
        * `resources/list` – explore resources exposed by the server (e.g., project-specific documents).
        * `prompts/list` – browse available predefined prompts.
        * `tasks/list` – browse long-running tasks over time.
      * Use pagination cursors to automate audits (e.g., periodic scan of all tools or tasks).

Coverage checklist (all showcased tool families)

* Memory: `start_session`, `save_memory`, `recall_memory`, `list_memories`, `search_memories`, `delete_memory`, `update_memory`, `auto_save_context`, `restore_session_context`, `prioritize_memory`.
* Semantic: `find_symbol`, `find_references`.
* Thinking: `create_thinking_chain`, `analyze_problem`, `step_by_step_analysis`, `break_down_problem`, `think_aloud_process`, `format_as_plan`.
* Reasoning: `apply_reasoning_framework`.
* Code Quality: `analyze_complexity`, `validate_code_quality`, `check_coupling_cohesion`, `suggest_improvements`, `apply_quality_rules`, `get_coding_guide`.
* Planning: `generate_prd`, `create_user_stories`, `analyze_requirements`, `feature_roadmap`.
* Prompt: `analyze_prompt`, `enhance_prompt`, `enhance_prompt_gemini`.
* Browser: `monitor_console_logs`, `inspect_network_requests`.
* UI: `preview_ui_ascii`.
* Time: `get_current_time`.
* Tasks API and pagination: `tasks/get`, `tasks/result`, `tasks/list`, `tasks/cancel`, `notifications/tasks/status`, `tools/list`, `resources/list`, `prompts/list`, `tasks/list`.

This is the end-to-end workflow that exercises every tool family in the repo in a coherent development lifecycle.
