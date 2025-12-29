## 1) Overview

### Problem statement

Maintaining many per-source MCP servers (e.g., `uvx mcpdoc ... --urls ...` plus overlapping `mcp-remote` endpoints) creates a large configuration surface area, redundant access methods, and repeated manual regeneration steps for `*-llms*.txt` artifacts.

### Who has the problem

* **Docs/tooling maintainers** who add/refresh llms.txt artifacts across many repos and doc sites.
* **Docs consumers** (Gemini CLI, Codex, other MCP clients) who want one stable MCP endpoint rather than dozens of per-source servers.

### Why current solutions fail

* **Config sprawl:** multiple MCP server entries per doc set and mixed access methods.
* **Manual refresh:** venv activation + `llmstxt <repo-url>` + copying outputs is manual and inconsistent.
* **No centralized registry:** outputs are not stored in a single stable repo structure for consumption.

### Proposed product (high level)

Create a single “llms-txt registry” repository containing generated `*-llms*.txt` artifacts under a stable layout (e.g., `docs/<source-id>/...`), and expose it through **one MCP server entry** using `mcp-remote` → `gitmcp.io/<org>/<repo>`. Add an automated refresh pipeline that regenerates and commits changes only when diffs exist.

### Success metrics (measurable)

* **Client config reduction:** from N per-source MCP entries to **1** registry entry in each client (Gemini CLI `settings.json`, Codex `config.toml`).
* **Refresh automation reliability:** ≥ 95% scheduled refresh runs complete without manual intervention (excluding upstream outages).
* **Determinism / idempotence:** repeated refresh runs with no upstream changes produce **no git diff**.
* **Time-to-add-source:** adding a new source requires only updating a manifest + running refresh (no MCP config explosion).

### Constraints and assumptions

* The `llmstxt` generator is installable in CI via `requirements.txt` and can run non-interactively.
* Generator outputs can be isolated per source using `--output-dir` / `OUTPUT_DIR` to prevent cross-source mixing.
* The registry repo already contains many generated artifacts organized by project/repo (e.g., `TanStack/*`, `openai/*`) and will remain the canonical storage location.
* “Native MCP server” requirement is satisfied by using standard MCP tooling (`mcp-remote`) and an MCP-capable remote (gitmcp).

---

## 2) Capability Tree (Functional Decomposition)

### Capability: Source Registry Management

#### Feature: Source manifest CRUD (MVP)

* **Description**: Maintain a canonical list of sources to generate and publish.
* **Inputs**: Source entries `{id, type, url, generator_profile, enabled, tags}`.
* **Outputs**: Validated manifest file (e.g., `sources.json`) and normalized in-memory list.
* **Behavior**: Validate schema; enforce stable IDs; reject duplicates; allow enable/disable without deletion.

#### Feature: Manifest validation and normalization (MVP)

* **Description**: Enforce schema + normalization so generation is deterministic.
* **Inputs**: Manifest JSON; optional defaults (profiles).
* **Outputs**: Normalized sources list; validation errors with actionable messages.
* **Behavior**: Validate required fields; normalize IDs (slug rules); resolve profile defaults; produce stable ordering.

---

### Capability: Artifact Generation & Refresh

#### Feature: Venv-aware generator runner (MVP)

* **Description**: Run `llmstxt <url>` per source with managed Python environment.
* **Inputs**: Source URL; generator profile; working directory; env vars.
* **Outputs**: Generator output directory per source; run logs; exit status.
* **Behavior**: Ensure `.venv/` exists; install deps; invoke generator; capture logs; fail-fast per source with summary.

#### Feature: Per-source output isolation (MVP)

* **Description**: Prevent outputs from mixing across sources.
* **Inputs**: Source ID; optional `OUTPUT_DIR` / `--output-dir`.
* **Outputs**: Output paths like `work/artifacts/<id>/...`.
* **Behavior**: Compute unique output dir; pass to generator; clean/overwrite only within that source’s sandbox.

---

### Capability: Registry Storage & Publication

#### Feature: Artifact ingestion and canonical placement (MVP)

* **Description**: Copy generated `*-llms*.txt` into `docs/<id>/` with stable naming.
* **Inputs**: Generator output directory; target docs directory; allowlist patterns.
* **Outputs**: Updated `docs/<id>/*-llms*.txt` (and optional metadata files).
* **Behavior**: Copy only matching files; delete removed artifacts (optional); preserve line endings; write a small metadata manifest (hashes, timestamps, source URL).

#### Feature: Diff detection and commit-on-change (MVP)

* **Description**: Commit updates only when content changes.
* **Inputs**: Git working tree; updated docs paths.
* **Outputs**: Either no-op or a commit with changed files; machine-readable summary.
* **Behavior**: `git status --porcelain`; if clean, exit 0 with “no changes”; else commit with standard message and include changed source IDs.

---

### Capability: MCP Consumption (Single Endpoint)

#### Feature: Single MCP endpoint documentation (MVP)

* **Description**: Provide canonical snippets to configure one MCP server in clients.
* **Inputs**: Registry repo location; gitmcp endpoint template.
* **Outputs**: Docs for Gemini CLI and Codex configuration.
* **Behavior**: Keep examples minimal; ensure they reference only one server entry.

#### Feature: Registry browsing contract (MVP)

* **Description**: Establish predictable paths so tools can locate relevant artifacts.
* **Inputs**: Source ID; desired artifact type (ctx/full/basic).
* **Outputs**: Canonical file paths (e.g., `docs/<id>/<id>-llms.txt`).
* **Behavior**: Enforce naming rules; optionally generate an index file listing all sources and available artifacts.

---

### Capability: Automation & Operations

#### Feature: Scheduled and manual refresh via CI (MVP)

* **Description**: Run refresh on a schedule and on-demand; commit diffs only.
* **Inputs**: GitHub Actions workflow triggers; repo secrets (if needed).
* **Outputs**: Updated repo content; run logs; failure notifications.
* **Behavior**: Checkout; setup Python; run refresh; commit/push only if changed.

#### Feature: Observability and run summary (MVP)

* **Description**: Produce a machine-parseable summary of per-source success/failure.
* **Inputs**: Run results per source; logs.
* **Outputs**: `refresh-report.json` + console summary.
* **Behavior**: Record timings, exit codes, artifact counts, error excerpts; non-zero exit only if configured threshold exceeded.

---

### Capability: Access Control (Non-MVP, unless required)

#### Feature: Public vs private hosting mode

* **Description**: Support decision between public gitmcp exposure vs private/self-hosted endpoint.
* **Inputs**: Repo visibility; alternative remote hosting config.
* **Outputs**: Documented deployment mode and required client config changes.
* **Behavior**: If private blocks gitmcp, switch to a self-hosted MCP-compatible endpoint (design decision).

---

## 3) Repository Structure + Module Definitions (Structural Decomposition)

### Repository structure (proposed)

```
llms-txt-registry/
├── docs/                        # Published artifacts (canonical)
│   └── <source-id>/
│       ├── <source-id>-llms.txt
│       ├── <source-id>-llms-ctx.txt
│       ├── <source-id>-llms-full.txt
│       └── metadata.json
├── sources.json                 # Source manifest (id -> url + profiles)
├── profiles.json                # Optional shared generator profiles/defaults
├── scripts/
│   ├── refresh.py               # Orchestrates refresh end-to-end
│   └── validate_manifest.py     # Preflight checks (optional entrypoint)
├── src/                         # Python package (optional but recommended)
│   ├── registry_config/
│   ├── generator_runner/
│   ├── artifact_ingest/
│   ├── git_sync/
│   └── reporting/
├── .github/workflows/
│   └── refresh.yml
├── requirements.txt
└── README.md                    # Client config snippets + operator guide
```

> Note: the repo already contains many generated artifact folders today; this structure formalizes `docs/<id>/` as the stable contract.

### Module definitions

#### Module: `src/registry_config` (foundation)

* **Maps to capability**: Source Registry Management
* **Responsibility**: Load, validate, normalize source manifest and profiles.
* **Exports**:

  * `load_manifest(path) -> Manifest`
  * `validate_manifest(manifest) -> list[ValidationError]`
  * `normalize_sources(manifest, profiles) -> list[SourceSpec]`

#### Module: `src/reporting` (foundation)

* **Maps to capability**: Automation & Operations
* **Responsibility**: Structured logging + run summary artifacts.
* **Exports**:

  * `RunReport.start(run_id) -> RunReport`
  * `RunReport.record_source_result(source_id, result)`
  * `RunReport.write_json(path)`

#### Module: `src/generator_runner`

* **Maps to capability**: Artifact Generation & Refresh
* **Responsibility**: Manage Python venv/deps and execute `llmstxt` per source in isolated dirs.
* **Exports**:

  * `ensure_venv(venv_path) -> None`
  * `install_requirements(venv_path, requirements_path) -> None`
  * `run_llmstxt(source: SourceSpec, output_dir: Path) -> GeneratorResult`

#### Module: `src/artifact_ingest`

* **Maps to capability**: Registry Storage & Publication
* **Responsibility**: Copy/normalize generated artifacts into canonical `docs/<id>/` layout.
* **Exports**:

  * `ingest_artifacts(source_id, gen_out_dir, docs_root) -> IngestResult`
  * `write_metadata(source_id, docs_dir, metadata) -> None`

#### Module: `src/git_sync`

* **Maps to capability**: Registry Storage & Publication / Ops
* **Responsibility**: Detect diffs and commit/push changes deterministically.
* **Exports**:

  * `has_changes(paths=...) -> bool`
  * `commit_changes(message, paths=...) -> CommitResult`
  * `push(remote, branch) -> None`

#### Module: `scripts/refresh.py`

* **Maps to capability**: Automation & Operations (orchestration)
* **Responsibility**: Top-level CLI to run: validate → generate → ingest → report → commit.
* **Exports** (CLI interface):

  * `refresh --manifest sources.json --docs-root docs/ --workdir work/ [--only <id>] [--fail-fast]`

---

## 4) Dependency Chain (layers, explicit “Depends on: […]”)

### Foundation Layer

* **registry_config**: manifest + profile schema, validation, normalization. Depends on: []
* **reporting**: run report + structured logging. Depends on: []

### Generation Layer

* **generator_runner**: venv + `llmstxt` execution. Depends on: [registry_config, reporting]

### Publication Layer

* **artifact_ingest**: canonical docs placement + metadata. Depends on: [registry_config, reporting]
* **git_sync**: diff detection + commit/push. Depends on: [reporting]

### Orchestration Layer

* **scripts/refresh.py**: end-to-end refresh CLI. Depends on: [registry_config, reporting, generator_runner, artifact_ingest, git_sync]

### Automation Layer

* **.github/workflows/refresh.yml**: schedule + dispatch running `scripts/refresh.py`. Depends on: [scripts/refresh.py]

No cycles: each layer depends only on earlier layers.

---

## 5) Development Phases (Phase 0…N; entry/exit criteria; tasks with dependencies + acceptance criteria + test strategy)

### Phase 0: Foundations

**Entry criteria**: Repo can add Python tooling and CI without breaking existing artifacts.
**Tasks**:

* [ ] Implement `registry_config` (depends on: [])

  * Acceptance criteria: invalid manifests fail with actionable errors; normalized stable ordering.
  * Test strategy: unit tests for schema validation, duplicate IDs, profile defaulting.
* [ ] Implement `reporting` (depends on: [])

  * Acceptance criteria: produces `refresh-report.json` with per-source results; consistent exit codes.
  * Test strategy: unit tests for JSON schema and aggregation logic.

**Exit criteria**: Manifest can be loaded/validated; report can be produced with a mock run.

---

### Phase 1: Manual refresh CLI (usable early)

**Goal**: A developer can run refresh locally and populate `docs/<id>/` for at least one source.
**Entry criteria**: Phase 0 complete.
**Tasks**:

* [ ] Implement `generator_runner` minimal path (depends on: [registry_config, reporting])

  * Acceptance criteria: creates/uses `.venv/`; runs `llmstxt` for a single source; captures stdout/stderr.
  * Test strategy: integration test with a stubbed `llmstxt` executable or fixture.
* [ ] Implement `artifact_ingest` (depends on: [registry_config, reporting])

  * Acceptance criteria: copies only `*-llms*.txt` into `docs/<id>/`; writes `metadata.json`.
  * Test strategy: unit tests on file copying, allowlist patterns, metadata content.
* [ ] Implement `scripts/refresh.py` local CLI (depends on: [registry_config, reporting, generator_runner, artifact_ingest])

  * Acceptance criteria: `refresh --only <id>` works; produces report; non-zero exit on generation failure.
  * Test strategy: e2e test on a temp directory with fixtures.

**Exit criteria**: Running refresh locally updates `docs/<id>/...` deterministically for at least one configured source.
**Delivers**: Single canonical docs layout that MCP clients can browse once published.

---

### Phase 2: Commit-on-change and CI automation

**Entry criteria**: Phase 1 complete; `docs/<id>/` layout exists.
**Tasks**:

* [ ] Implement `git_sync` (depends on: [reporting])

  * Acceptance criteria: no-op when no changes; commits only changed docs; standard commit message.
  * Test strategy: integration test in a temp git repo verifying clean/no-op and commit paths.
* [ ] Add GitHub Actions `refresh.yml` (depends on: [scripts/refresh.py, git_sync])

  * Acceptance criteria: workflow supports schedule + manual dispatch; commits only if diff exists.
  * Test strategy: workflow lint + local `act`-style dry run (if used) + verify script exit codes.

**Exit criteria**: CI refresh updates repo automatically and does not create empty commits.
**Delivers**: Fully automated refresh pipeline.

---

### Phase 3: Client “single server” adoption and decommission plan

**Entry criteria**: Phase 2 complete; registry hosted (public or private decision).
**Tasks**:

* [ ] Document client configs for one MCP entry (depends on: [docs layout contract])

  * Acceptance criteria: README includes Gemini CLI + Codex snippets using one MCP server entry.
  * Test strategy: doc checks + smoke test by connecting client to registry endpoint.
* [ ] Migration guidance: remove redundant per-source MCP servers after parity (depends on: [client config docs])

  * Acceptance criteria: checklist for verifying source parity before deleting old entries.
  * Test strategy: manual validation steps documented.

**Exit criteria**: Each client uses exactly one MCP server entry; per-source servers are removable.
**Delivers**: Operational simplification (one tool / one endpoint).

---

### Phase 4: Optional hardening (non-MVP)

**Tasks**:

* Retry/backoff and partial failure policy (depends on: [reporting, refresh CLI])
* Private hosting alternative (if gitmcp cannot be used) (depends on: [hosting decision])
* Index generation (`docs/index.json`) for discoverability (depends on: [artifact_ingest])

---

## 6) User Experience

### Personas

* **Registry Maintainer**: adds sources, runs/monitors refresh, resolves failures, controls hosting mode.
* **Docs Consumer (LLM tooling user)**: configures a client once; queries registry content through a single MCP server.

### Key flows

1. **Add a new source**

   * Edit `sources.json` with a stable `id` and `url`.
   * Run `scripts/refresh.py --only <id>`.
   * Verify `docs/<id>/` contains expected `*-llms*.txt`.
2. **Automated refresh**

   * CI runs scheduled refresh; commits only on diff.
   * Maintainer checks `refresh-report.json` artifacts/logs on failure.
3. **Client setup**

   * User adds exactly one MCP server entry pointing to the registry (via `mcp-remote` → gitmcp).

### UX notes tied to capabilities

* Stable IDs must be human-readable slugs; avoid owner/repo coupling where possible.
* Reports should clearly separate “generator failed” vs “no upstream change” vs “ingest failed”.
* Make it easy to run a single source locally (`--only`) to debug failures quickly.

---

## 7) Technical Architecture

### System components

* **Manifest + profiles**: `sources.json`, optional `profiles.json`.
* **Refresh orchestrator**: Python CLI coordinating validation → generation → ingestion → report → git sync.
* **Published registry**: `docs/<id>/...` containing `*-llms*.txt` plus metadata, committed to git.
* **MCP access path**: One MCP server configured in clients using `mcp-remote` to a gitmcp-backed repo endpoint.

### Data models (conceptual)

* `SourceSpec`: `{ id, url, type(repo|site), profile, enabled, tags }`
* `GeneratorResult`: `{ exit_code, stdout_path, stderr_path, duration_ms, output_dir }`
* `IngestResult`: `{ copied_files, removed_files, docs_dir, metadata }`
* `RunReport`: `{ run_id, started_at, sources: { [id]: { status, errors?, timings } } }`

### External integrations

* **Python**: `llmstxt` generator invocation.
* **GitHub Actions**: scheduled + manual refresh automation.
* **MCP client tooling**: `mcp-remote` consuming registry via gitmcp endpoint.

### Key decisions (with trade-offs)

* **Decision: Central registry repo as the only published surface**

  * Rationale: reduces MCP config sprawl; single canonical contract.
  * Trade-offs: registry repo can grow large; must keep refresh deterministic.
  * Alternatives: per-source MCP servers; custom “llms-hub” search server (explicitly out of scope).

* **Decision: Commit-on-change**

  * Rationale: avoids noisy commits; supports idempotent refresh.
  * Trade-offs: requires consistent normalization to prevent spurious diffs.

---

## 8) Test Strategy

### Test pyramid targets

* **Unit tests (70%)**: manifest validation, path mapping, copy rules, metadata content, report aggregation.
* **Integration tests (25%)**: run `refresh.py` with stubbed generator; run in temp git repo for commit detection.
* **E2E tests (5%)**: CI-like run (local simulation) verifying “no changes → no commit” and “changes → commit”.

### Coverage minimums

* Line: 80%
* Branch: 70% (focus on error handling paths for runner/ingest)
* Function: 80%

### Critical scenarios per module

* `registry_config`

  * Happy: loads and normalizes manifest order deterministically.
  * Error: duplicate IDs; missing URLs; invalid profile reference.
* `generator_runner`

  * Happy: venv created; requirements installed; generator invoked with isolated output dir.
  * Error: generator non-zero exit; timeout; missing binary.
* `artifact_ingest`

  * Happy: copies only allowlisted `*-llms*.txt` files; writes metadata.
  * Edge: source produces only some variants (no `-ctx`), ingestion still succeeds.
* `git_sync`

  * Happy: detects dirty tree; commits with expected message.
  * No-op: clean tree produces no commit and exit 0.
* `refresh.py`

  * Partial failure policy: records per-source failure; overall exit behavior matches configuration.

---

## 9) Risks and Mitigations

### Technical risks

* **Generator instability or output format drift**

  * Impact: High | Likelihood: Medium
  * Mitigation: pin generator version; validate expected artifact patterns; record generator version in metadata.
  * Fallback: disable failing source; keep last known good artifacts.

* **Non-deterministic diffs**

  * Impact: Medium | Likelihood: Medium
  * Mitigation: normalize line endings; stable ordering; strip volatile headers if present; metadata separated from content diffs.

### Dependency risks

* **Private hosting blocks gitmcp access**

  * Impact: High | Likelihood: Unknown
  * Mitigation: decide hosting mode early; document self-hosted MCP-compatible alternative.
  * Fallback: host registry in an accessible location; or keep minimal per-source servers for private sources.

### Scope risks

* **Expanding into “search/index hub”**

  * Impact: Medium | Likelihood: Medium
  * Mitigation: explicitly keep out of scope; focus on registry + refresh + single endpoint.

---

## 10) Appendix

### Existing evidence / context

* Current pain points, target direction (“Pattern A”), and automation requirements are captured in the improvement spec.
* The current registry repo already contains many generated artifacts across numerous sources, illustrating the need for a stable contract and a refresh pipeline.

### Open questions

* Registry visibility: public via gitmcp vs private/self-hosted endpoint.
* Exact packaging/install method for `llmstxt` generator in CI (`requirements.txt` contents).
* Whether every source must produce all variants (`llms.txt`, `llms-full.txt`, `llms-ctx.txt`) or allow partial.

### Glossary

* **Registry repo**: Git repository containing generated `*-llms*.txt` artifacts under a stable directory contract.
* **Source ID**: Stable identifier used for folder naming and client discovery (`docs/<id>/...`).
* **MCP**: Model Context Protocol; clients connect to MCP servers to access tools/content.
