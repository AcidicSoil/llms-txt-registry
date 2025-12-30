# strategist questions — oracle pack

---

## run (exactly 20)

```bash
# shellcheck shell=bash
set -euo pipefail

out_dir="artifacts/oracle/strategist-questions/2025-12-30"
mkdir -p "$out_dir"

# 01) ROI=2.80 | Immediate | invariants | src/registry_config/models.py:validate_unique_ids
oracle \
  --files-report \
  --write-output "$out_dir/01-immediate-invariants-unique-ids.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, invariants, ref: src/registry_config/models.py:validate_unique_ids): Does validate_unique_ids correctly detect duplicate source IDs during manifest load and make the error actionable for maintainers? Answer format: Reference: src/registry_config/models.py:validate_unique_ids; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/registry_config/models.py"

# 02) ROI=2.40 | Immediate | invariants | src/registry_config/models.py:validate_slug
oracle \
  --files-report \
  --write-output "$out_dir/02-immediate-invariants-slug-validation.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, invariants, ref: src/registry_config/models.py:validate_slug): Does validate_slug and SLUG_REGEX accept all current source IDs and doc folder names, or will it reject any real entries? Answer format: Reference: src/registry_config/models.py:validate_slug; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/registry_config/models.py" \
  -f "sources.json"

# 03) ROI=2.00 | Immediate | contracts/interfaces | src/registry_config/loader.py:load_manifest
oracle \
  --files-report \
  --write-output "$out_dir/03-immediate-contracts-load-manifest.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, contracts/interfaces, ref: src/registry_config/loader.py:load_manifest): When sources.json is missing or malformed, does load_manifest behave as intended (empty Manifest vs error), and do callers handle that outcome safely? Answer format: Reference: src/registry_config/loader.py:load_manifest; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/registry_config/loader.py" \
  -f "sources.json"

# 04) ROI=1.87 | Immediate | contracts/interfaces | src/registry_config/models.py:Source
oracle \
  --files-report \
  --write-output "$out_dir/04-immediate-contracts-source-schema.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, contracts/interfaces, ref: src/registry_config/models.py:Source): Does the Source model capture all fields actually used by the refresh workflow (enabled/profile/last_refreshed/last_model_used), and are defaults aligned with scripts/refresh.py expectations? Answer format: Reference: src/registry_config/models.py:Source; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/registry_config/models.py" \
  -f "scripts/refresh.py"

# 05) ROI=1.80 | Immediate | observability | src/generator_runner/runner.py:logger
oracle \
  --files-report \
  --write-output "$out_dir/05-immediate-observability-run-logging.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, observability, ref: src/generator_runner/runner.py:logger): Are current log statements sufficient to trace per-source execution, including command, duration, and errors, or do we need additional structured logging? Answer format: Reference: src/generator_runner/runner.py:logger; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/generator_runner/runner.py"

# 06) ROI=1.58 | Immediate | failure modes | src/generator_runner/runner.py:run_source
oracle \
  --files-report \
  --write-output "$out_dir/06-immediate-failure-run-source.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, failure modes, ref: src/generator_runner/runner.py:run_source): Does run_source surface subprocess failures and timeouts with enough context (stderr/stdout/returncode) to diagnose generator issues quickly? Answer format: Reference: src/generator_runner/runner.py:run_source; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/generator_runner/runner.py"

# 07) ROI=1.40 | Immediate | feature flags | src/generator_runner/runner.py:env["ENABLE_CTX"]
oracle \
  --files-report \
  --write-output "$out_dir/07-immediate-feature-flags-enable-ctx.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, feature flags, ref: src/generator_runner/runner.py:env[ENABLE_CTX]): ENABLE_CTX is hard-coded to 1; should this be configurable via CLI or manifest profile, and what is the safest default? Answer format: Reference: src/generator_runner/runner.py:env[ENABLE_CTX]; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/generator_runner/runner.py" \
  -f "scripts/refresh.py"

# 08) ROI=1.40 | Immediate | contracts/interfaces | src/reporting/report.py:RunReport
oracle \
  --files-report \
  --write-output "$out_dir/08-immediate-contracts-run-report.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, contracts/interfaces, ref: src/reporting/report.py:RunReport): Does RunReport capture all fields needed for auditing a refresh run (per-source status, model_used, artifacts, duration), or are key fields missing? Answer format: Reference: src/reporting/report.py:RunReport; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/reporting/report.py"

# 09) ROI=1.40 | Immediate | invariants | src/git_sync/status.py:check_stale_artifacts
oracle \
  --files-report \
  --write-output "$out_dir/09-immediate-invariants-stale-check.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, invariants, ref: src/git_sync/status.py:check_stale_artifacts): Does check_stale_artifacts reliably detect stale docs updates when sources.json changes, or can it miss or misflag common workflows? Answer format: Reference: src/git_sync/status.py:check_stale_artifacts; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/git_sync/status.py"

# 10) ROI=1.40 | Immediate | contracts/interfaces | src/artifact_ingest/ingest.py:ingest_artifacts
oracle \
  --files-report \
  --write-output "$out_dir/10-immediate-contracts-ingest-artifacts.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, contracts/interfaces, ref: src/artifact_ingest/ingest.py:ingest_artifacts): Does ingest_artifacts handle normalization and copying without overwriting unintended files, and should it enforce deduping or cleanup semantics? Answer format: Reference: src/artifact_ingest/ingest.py:ingest_artifacts; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/artifact_ingest/ingest.py"

# 11) ROI=1.20 | Immediate | contracts/interfaces | src/artifact_ingest/index.py:generate_registry_index
oracle \
  --files-report \
  --write-output "$out_dir/11-immediate-contracts-registry-index.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, contracts/interfaces, ref: src/artifact_ingest/index.py:generate_registry_index): Does generate_registry_index produce stable ordering and include all required artifact patterns/metadata for downstream consumers? Answer format: Reference: src/artifact_ingest/index.py:generate_registry_index; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/artifact_ingest/index.py"

# 12) ROI=1.20 | Immediate | background jobs | scripts/refresh.py:main
oracle \
  --files-report \
  --write-output "$out_dir/12-immediate-jobs-refresh-main.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Immediate, background jobs, ref: scripts/refresh.py:main): Is refresh.py main idempotent and safe to re-run on the same source set, and are outputs deterministic across runs? Answer format: Reference: scripts/refresh.py:main; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "scripts/refresh.py"

# 13) ROI=0.84 | Strategic | observability | src/reporting/report.py:to_json
oracle \
  --files-report \
  --write-output "$out_dir/13-strategic-observability-report-json.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, observability, ref: src/reporting/report.py:to_json): Is the RunReport JSON format stable enough for long-term observability and metrics ingestion, or do we need schema versioning and retention strategy? Answer format: Reference: src/reporting/report.py:to_json; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/reporting/report.py"

# 14) ROI=0.75 | Strategic | UX flows | scripts/refresh.py:argparse.ArgumentParser
oracle \
  --files-report \
  --write-output "$out_dir/14-strategic-ux-cli-args.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, UX flows, ref: scripts/refresh.py:argparse.ArgumentParser): Is the CLI UX for refresh.py adequate (help text, error clarity, flags), and would adding a dry-run or list-sources command materially reduce operator error? Answer format: Reference: scripts/refresh.py:argparse.ArgumentParser; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "scripts/refresh.py"

# 15) ROI=0.72 | Strategic | contracts/interfaces | scripts/populate_manifest.py:scan_and_populate
oracle \
  --files-report \
  --write-output "$out_dir/15-strategic-contracts-populate-manifest.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, contracts/interfaces, ref: scripts/populate_manifest.py:scan_and_populate): Does scan_and_populate safely rename doc directories and update sources.json without collisions or data loss, and should it support preview/dry-run? Answer format: Reference: scripts/populate_manifest.py:scan_and_populate; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "scripts/populate_manifest.py"

# 16) ROI=0.70 | Strategic | feature flags | src/registry_config/models.py:GeneratorProfile
oracle \
  --files-report \
  --write-output "$out_dir/16-strategic-feature-profiles.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, feature flags, ref: src/registry_config/models.py:GeneratorProfile): Are GeneratorProfile fields sufficient for future provider support (headers, timeout, model), or do we need additional per-provider flags/config? Answer format: Reference: src/registry_config/models.py:GeneratorProfile; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/registry_config/models.py" \
  -f "sources.json"

# 17) ROI=0.57 | Strategic | background jobs | src/generator_runner/runner.py:GeneratorRunner
oracle \
  --files-report \
  --write-output "$out_dir/17-strategic-jobs-runner-scale.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, background jobs, ref: src/generator_runner/runner.py:GeneratorRunner): Should GeneratorRunner support parallel execution or rate limiting for large source sets, and where is the safest insertion point? Answer format: Reference: src/generator_runner/runner.py:GeneratorRunner; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "src/generator_runner/runner.py"

# 18) ROI=0.53 | Strategic | caching/state | Unknown
oracle \
  --files-report \
  --write-output "$out_dir/18-strategic-cache-unknown.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, caching/state, ref: Unknown; missing patterns: **/*cache*.*, **/redis/**, **/*session*.*, **/*store*.*): Is a caching/state layer needed for artifact generation or downloads, and where should it live if introduced? If reference is Unknown, confirm absence in attached files and suggest the most likely location in this repo. Answer format: Reference: Unknown; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "README.md" \
  -f "sources.json"

# 19) ROI=0.36 | Strategic | permissions | Unknown
oracle \
  --files-report \
  --write-output "$out_dir/19-strategic-permissions-unknown.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, permissions, ref: Unknown; missing patterns: **/auth/**, **/*rbac*.*, **/*permission*.*, **/*policy*.*): Does registry ingestion require access control or URL allowlists, and where would that enforcement live? If reference is Unknown, confirm absence in attached files and suggest the most likely location in this repo. Answer format: Reference: Unknown; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "README.md"

# 20) ROI=0.35 | Strategic | migrations | Unknown
oracle \
  --files-report \
  --write-output "$out_dir/20-strategic-migrations-unknown.md" \
  -p "Repo: llms-txt registry tooling in Python; core code in src/ and scripts/, artifacts in docs/. Constraints: Unknown. Non-goals: Unknown. Team size: Unknown. Deadline: Unknown. Question (Strategic, migrations, ref: Unknown; missing patterns: **/migrations/**, **/schema.* , **/prisma/**): How should sources.json schema evolution be managed, and do we need explicit migrations or versioned schema docs? If reference is Unknown, confirm absence in attached files and suggest the most likely location in this repo. Answer format: Reference: Unknown; Direct answer; Evidence (cite attached paths/symbols); Smallest experiment today; Risks/assumptions (max 3)." \
  -f "README.md" \
  -f "sources.json"
```
