Title:

* Consolidate llms.txt ingestion into a single MCP “registry” server (gitmcp) with automated refresh

Summary:

* The current setup uses multiple MCP servers (`mcpdoc` and `mcp-remote`) per doc set, with redundant access methods and large configuration surface area.
* Implement a single “llms-txt registry” repository that stores all generated `*-llms*.txt` artifacts and expose it through one MCP server entry (via `mcp-remote` → `gitmcp.io`).
* Add an automated refresh pipeline that runs the Python `llmstxt <url>` generator (venv-aware) and publishes updated artifacts deterministically.

Background / Context:

* User goal: “host these in one place and just call one tool instead of having multiple” MCP servers.
* Current generation workflow is Python-based: (1) activate venv, (2) run `llmstxt <repo-url>`, (3) output goes to `artifacts/`.
* Proposed direction accepted by user: “Pattern A sounds good” (registry repo + gitmcp + one MCP server).

Current Behavior (Actual):

* Multiple MCP servers per doc set (e.g., lots of `uvx mcpdoc ... --urls ...`) and mixed access methods (local `mcpdoc` + remote `mcp-remote` for overlapping sources).
* Manual steps required to regenerate artifacts (venv activation + generator run), and outputs are not centralized for consumption.

Expected Behavior:

* A single, centralized repository containing all generated `*-llms*.txt` artifacts (e.g., under `docs/<source-id>/`).
* A single MCP server entry in each client config (Gemini CLI `settings.json`, Codex `config.toml`) pointing to the registry via `mcp-remote` + `gitmcp.io`.
* Automated refresh (scheduled + manual trigger) that regenerates artifacts and commits updates only when content changes.

Requirements:

* Create a “registry” repo (example name: `llms-txt-registry`) to store generated outputs in a stable structure (e.g., `docs/<id>/...`).
* Maintain a source manifest (e.g., `sources.json`) mapping stable `id` → `repo_url`.
* Implement a refresh script that:

  * Is venv-aware (creates/uses `.venv/` without manual activation).
  * Installs the Python generator via `requirements.txt`.
  * Runs the generator per repo URL.
  * Copies outputs from `artifacts/<owner>/<repo>/*-llms*.txt` into `docs/<id>/`.
  * Supports overriding output directory (`--output-dir` / `OUTPUT_DIR`) to avoid cross-source mixing.
* Add GitHub Actions workflow to refresh on a schedule and on manual dispatch, committing only if diffs exist.
* Update client configs to use one MCP server:

  * Gemini CLI: one `mcpServers.llms-registry` using `npx mcp-remote https://gitmcp.io/<user>/llms-txt-registry`.
  * Codex: one `[mcp_servers.llms-registry]` entry with the same remote endpoint.
* Operational guidance:

  * Prefer one access method per source (avoid duplicating same docs via both local `mcpdoc` and remote).
  * Keep registry limited to generated `*-llms*.txt` artifacts; keep “live docs” servers separate.

Out of Scope:

* Designing/implementing a custom “llms-hub” MCP server (local search/index server) beyond the registry + gitmcp approach (mentioned as an alternative).
* Deciding public vs private hosting approach (not decided; identified as a decision point).

Reproduction Steps:

* Not provided (this is an improvement/architecture change request rather than a single failing repro).

Environment:

* OS: Unknown
* Clients: Gemini CLI (`settings.json`) and Codex (`config.toml`) (per conversation).
* Generator: Python CLI invoked as `llmstxt <url>`; outputs to `artifacts/`.
* MCP tooling: `npx mcp-remote`, `uvx mcpdoc` (current), gitmcp endpoint.

Evidence:

* User workflow: “source activate the venv … `llmstxt <repo-url>` … `artifacts/` is the output directory.”
* Target architecture: “Expose that one place via one MCP server… Pattern A — ‘Registry repo + gitmcp’.”
* Config snippets for one-server approach (Gemini + Codex).
* Proposed refresh automation (GitHub Actions).

Decisions / Agreements:

* Adopt Pattern A (“Registry repo + gitmcp”) as the preferred direction. (per user: “Pattern A sounds good”).

Open Items / Unknowns:

* Registry visibility/hosting: public via gitmcp vs private/self-hosted endpoint.
* Exact installation method for the Python `llmstxt` generator in CI (`requirements.txt` contents / packaging source).
* Whether registry should store both `llms.txt` and `llms-full.txt` for all sources (implied but not strictly specified).

Risks / Dependencies:

* CI refresh depends on having a working runtime environment for the Python generator (venv + dependencies).
* If registry is private, gitmcp accessibility may be a blocker, requiring alternate hosting.
* Large sources (e.g., “TanStack”) previously drove “command-line explosion” in config; migration must ensure equivalent coverage in the registry.

Acceptance Criteria:

* [ ] A registry repo exists with `sources.json`, `docs/`, and refresh automation.
* [ ] Running the refresh script produces/updates `docs/<id>/` with generated `*-llms*.txt` copied from generator outputs under `artifacts/` (or overridden output dir).
* [ ] GitHub Actions refresh runs on schedule and commits only when diffs exist.
* [ ] Gemini CLI and Codex each use exactly one MCP server entry pointing at the registry via `mcp-remote`/gitmcp.
* [ ] Redundant per-source MCP servers (local `mcpdoc` and duplicated remote endpoints) can be removed once their artifacts are present in the registry.

Priority & Severity (if inferable from text):

* Priority: Not provided
* Severity: Not provided

Labels (optional):

* enhancement
* mcp
* automation
* devops
* docs-ingestion
* config-management
