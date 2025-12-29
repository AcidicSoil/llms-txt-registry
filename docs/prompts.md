00.planning/create-plan.md
```
1 | ---
2 | description: Create a comprehensive task plan with context, success criteria, approach, and risks
3 | argument-hint: TASK=<task-description-or-goal>
4 | ---
5 | 
6 | <task>
7 | $TASK
8 | </task>
9 | 
10 | # Create Plan (slash command)
11 | 
12 | Goal: draft a full task plan in `docs/tasks/todo/<XX>-<name>.md`.
13 | 
14 | Always do this first:
15 | - Read AGENTS.md and follow all rules/constraints.
16 | 
17 | Plan requirements (keep concise, but complete):
18 | - Context: 2–3 bullet recap of the problem/goal.
19 | - Success criteria / acceptance: bullet list with measurable checks.
20 | - Deliverables: code/docs/tests to produce.
21 | - Approach: ordered steps (no workarounds; sustainable, clean implementation).
22 | - Risks / unknowns: note dependencies, edge cases, perf/security concerns.
23 | - Testing & validation: what to run (unit/integration/e2e), data sets, platforms.
24 | - Rollback / escape hatches: brief note if applicable.
25 | - Owner / date: stamp with today’s date.
26 | 
27 | After writing the plan:
28 | - Save at path `docs/tasks/todo/<XX>-<name>.md`.
29 | - Ask the user: “What are the most important questions to confirm before implementation?” and list your top 3–5 clarifying questions.
30 | 
31 | Suggested prompt body:
32 | ```
33 | Context
34 | - ...
35 | - ...
36 | 
37 | Success criteria
38 | - ...
39 | 
40 | Deliverables
41 | - ...
42 | 
43 | Approach
44 | 1) ...
45 | 2) ...
46 | 3) ...
47 | 
48 | Risks / unknowns
49 | - ...
50 | 
51 | Testing & validation
52 | - ...
53 | 
54 | Rollback / escape hatch
55 | - ...
56 | 
57 | Owner/Date
58 | - <you> / <YYYY-MM-DD>
59 | ```
60 | 
61 | Reminder:
62 | - No workarounds or half measures; design for long-term maintainability.
63 | - If info is missing, include assumptions and surface them in the questions you ask the user at the end.
```

00.planning/plan-review.md
```
1 | <plan>
2 | $1
3 | </plan>
4 | 
5 | review the current <plan />
6 | 
7 | - reflects the current codebase (files, patterns, constraints)
8 | - no fallbacks, no feature flags
9 | - full change or full refactor only; no “future use” leftovers
10 | - list code smells and caveats
11 | - clear scope and out of scope
12 | - performance, security, and privacy impact
13 | - decision: if the analysis indicates >90% satisfaction with the implementation, mark GREEN LIGHT
14 | 
15 | 
```

00.planning/planning-process.md
```
1 | ---
2 | phase: 'P1 Plan & Scope'
3 | gate: 'Scope Gate'
4 | status: 'confirm problem, users, Done criteria, and stack risks are logged.'
5 | previous:
6 |   - 
7 | next:
8 |   -
9 |   -
10 | ---
11 | 
12 | # Planning Process
13 | 
14 | Trigger: /planning-process
15 | 
16 | Purpose: Draft, refine, and execute a feature plan with strict scope control and progress tracking.
17 | 
18 | ## Steps
19 | 
20 | 1. If no plan file exists, create `PLAN.md`. If it exists, load it.
21 | 2. Draft sections: **Goal**, **User Story**, **Milestones**, **Tasks**, **Won't do**, **Ideas for later**, **Validation**, **Risks**.
22 | 3. Trim bloat. Convert vague bullets into testable tasks with acceptance criteria.
23 | 4. Tag each task with an owner and estimate. Link to files or paths that will change.
24 | 5. Maintain two backlogs: **Won't do** (explicit non-goals) and **Ideas for later** (deferrable work).
25 | 6. Mark tasks done after tests pass. Append commit SHAs next to completed items.
26 | 7. After each milestone: run tests, update **Validation**, then commit `PLAN.md`.
27 | 
28 | ## Output format
29 | 
30 | - Update or create `PLAN.md` with the sections above.
31 | - Include a checklist for **Tasks**. Keep lines under 100 chars.
32 | 
33 | ## Examples
34 | 
35 | **Input**: "Add OAuth login"
36 | 
37 | **Output**:
38 | 
39 | - Goal: Let users sign in with Google.
40 | - Tasks: [ ] add Google client, [ ] callback route, [ ] session, [ ] E2E test.
41 | - Won't do: org SSO.
42 | - Ideas for later: Apple login.
43 | 
44 | ## Notes
45 | 
46 | - Planning only. No code edits.
47 | - Assume a Git repo with test runner available.
```

00.planning/prd-generator.md
```
1 | <!-- path: prd-generator.md -->
2 | 
3 | <!--
4 | $1 = source document path or raw Markdown to mine (single input)
5 | $2 = product name override (optional)
6 | $3 = maximum links to mine in $1 (default 20)
7 | $4 = maximum features (default 8)
8 | -->
9 | 
10 | # PRD Generator Template
11 | 
12 | **Goal**
13 | From $1, generate a dependency-aware PRD using RPG method. Infer everything possible from $1. Only use $2–$4 to cap or override.
14 | 
15 | **Output file**
16 | Write plain text to `prd.txt`. Use **exactly** these sections in order, each separated by **one** blank line:
17 | 
18 | # Overview
19 | # Core Features
20 | # User Experience
21 | # Technical Architecture
22 | # Development Roadmap
23 | # Logical Dependency Chain
24 | # Risks and Mitigations
25 | # Appendix
26 | 
27 | ---
28 | 
29 | ## Scavenge and Normalize (do before writing)
30 | 
31 | 1) **Parse $1**
32 | 
33 | - Accept a filesystem path or raw Markdown.
34 | - Extract: product name, problem, users, constraints, notable links, code paths, APIs, data models, UI hints, prior art.
35 | - If a field is missing, infer conservatively from context; if uncertain, mark with `{TBD:<label>}`.
36 | 
37 | 2) **Canonicalize product name**
38 | 
39 | - Prefer $2 if present, else best inferred name.
40 | 
41 | 3) **RPG framing** *(WHAT vs HOW)*
42 | 
43 | - WHAT = capabilities and features.
44 | - HOW = modules, files, APIs, data, infra.
45 | - Map WHAT→HOW later in “Logical Dependency Chain”.
46 | - Keep features atomic and independently testable.
47 | 
48 | 4) **Limit scope**
49 | 
50 | - Cap features to $4 (default 8).
51 | - Cap link-derived evidence to $3 (default 20).
52 | - Prioritize content that supports MVP.
53 | 
54 | ---
55 | 
56 | ## Section Specifications
57 | 
58 | ### # Overview
59 | 
60 | - Problem statement, target users, value. Keep implementation out. Populate from $1.
61 | 
62 | ### # Core Features
63 | List each feature with:
64 | 
65 | - **What**: one sentence.
66 | - **Why**: user value or constraint tie-in.
67 | - **High-level How**: approach without code.
68 | - **BDD**:
69 |   - Given …
70 |   - When …
71 |   - Then …
72 | 
73 | ### # User Experience
74 | 
75 | - Personas, key user flows, UX and accessibility notes. Include the fastest path to “first successful outcome.”
76 | 
77 | ### # Technical Architecture
78 | 
79 | - System components, data models, APIs/integrations, infrastructure, and NFRs. Defer deep design debates to Appendix.
80 | 
81 | ### # Development Roadmap
82 | 
83 | - **MVP**: smallest end-to-end slice with acceptance criteria.
84 | - **Future Enhancements**: clearly separated.
85 | - No dates. Only scope and testable outcomes.
86 | 
87 | ### # Logical Dependency Chain
88 | Use RPG style. Provide a topologically sorted list from foundations to layers. For each module:
89 | 
90 | - **Module**: name
91 | - **Maps to capability**: <capability>
92 | - **Depends on**: [modules]
93 | - **Delivers**: observable behavior
94 | 
95 | Ensure foundation modules have **no** dependencies and no cycles exist.
96 | 
97 | ### # Risks and Mitigations
98 | For each risk:
99 | 
100 | - **Description**
101 | - **Likelihood**: High/Medium/Low
102 | - **Impact**: High/Medium/Low
103 | - **Mitigation**
104 | - **Fallback**
105 | 
106 | ### # Appendix
107 | 
108 | - **Assumptions**: bullets.
109 | - **Research findings**: distilled from $1. Quote minimally.
110 | - **Context notes**: `- <visible text> — inferred topic`
111 | - **Technical specs**: any schemas, API shapes, or file paths referenced.
112 | 
113 | ---
114 | 
115 | ## Validation Checks (reject and fix before writing)
116 | 
117 | - All headers present and in exact order with single blank lines between sections.
118 | - Each feature has full BDD triad.
119 | - Roadmap has MVP and Enhancements, each with acceptance criteria.
120 | - Dependency chain is acyclic, foundations first, maps WHAT→HOW.
121 | - Risks include likelihood and impact.
122 | - No secrets or live URLs leaked; convert links in $1 to **visible text only** in Appendix context notes.
123 | 
124 | ---
125 | 
126 | ## Writing Rules
127 | 
128 | - Plain text only. No markdown tables. No extra sections.
129 | - Prefer concise sentences. No dates. No promises. Only testable statements.
130 | - Use `{TBD:<label>}` for unknowns rather than guessing.
131 | 
132 | ---
133 | 
134 | ## Example Skeleton (format only)
135 | 
136 | # Overview
137 | <problem, users, value>
138 | 
139 | # Core Features
140 | 
141 | - Feature: <name>
142 |   - What: …
143 |   - Why: …
144 |   - High-level How: …
145 |   - BDD:
146 |     - Given …
147 |     - When …
148 |     - Then …
149 | 
150 | # User Experience
151 | <personas, key flows, a11y>
152 | 
153 | # Technical Architecture
154 | <components, data, APIs, infra, NFRs>
155 | 
156 | # Development Roadmap
157 | ## MVP
158 | 
159 | - Outcome: …
160 | - Acceptance criteria: …
161 | 
162 | ## Future Enhancements
163 | 
164 | - Item: …
165 | - Acceptance criteria: …
166 | 
167 | # Logical Dependency Chain
168 | 
169 | - Module: <foundation-a>
170 |   - Maps to capability: …
171 |   - Depends on: []
172 |   - Delivers: …
173 | - Module: <layer-1-x>
174 |   - Maps to capability: …
175 |   - Depends on: [foundation-a]
176 |   - Delivers: …
177 | 
178 | # Risks and Mitigations
179 | 
180 | - Description: …
181 |   - Likelihood: …
182 |   - Impact: …
183 |   - Mitigation: …
184 |   - Fallback: …
185 | 
186 | # Appendix
187 | 
188 | - Assumptions:
189 |   - …
190 | - Research findings:
191 |   - …
192 | - Context notes:
193 |   - <visible text> — <inferred topic>
194 | - Technical specs:
195 |   - …
196 | 
197 | ```
```

01.prework/need-docs-v3.md
```
1 | <!--
2 | $1 = Project scope / feature
3 | $2 = Component / module impacted
4 | $3 = Target date or milestone
5 | $4 = Repos / PRs / specs to reference
6 | $5 = Document owners / SMEs
7 | $6 = Known risks or constraints
8 | $7 = Definition of Done / acceptance criteria
9 | -->
10 | 
11 | # {$2 or Document Gap Assessment}
12 | 
13 | ## Context
14 | 
15 | - Scope/feature: **$1**
16 | - Impacted area: **$2**
17 | - Target date: **$3**
18 | - References: **$4**
19 | - Owners/SMEs: **$5**
20 | - Risks/constraints: **$6**
21 | - Definition of Done: **$7**
22 | 
23 | ## Task
24 | 
25 | Determine whether additional documentation is required to complete the implementation correctly and confidently.
26 | 
27 | ## Expected Deliverable
28 | 
29 | Provide a table of needed documents followed by a single-line verdict.
30 | 
31 | ### Documents Needed (table)
32 | 
33 | - **document_name**
34 | - **why_needed**
35 | - **key_contents_expected**
36 | - **current_status** (available / missing / draft)
37 | - **source_or_owner**
38 | - **blocking_risk** (low / medium / high)
39 | 
40 | **Verdict:** “Ready” _or_ “Not ready—waiting on {items}.”
41 | 
42 | ## Analysis Aids (fill as applicable)
43 | 
44 | ### Affected files / areas
45 | 
46 | _List the files, packages, services, or endpoints that depend on the missing info._
47 | 
48 | ### Root cause of gaps
49 | 
50 | _Explain why the information isn’t available or is ambiguous._
51 | 
52 | ### Proposed fix
53 | 
54 | _Describe how to obtain or author the missing docs (owner, format, timeline)._
55 | 
56 | ### Tests impacted
57 | 
58 | _Call out test plans or cases that are blocked by missing details._
59 | 
60 | ### Docs gaps
61 | 
62 | _Summarize the precise unanswered questions and assumptions._
63 | 
64 | ### Open questions
65 | 
66 | _Bullet the questions that must be answered before implementation proceeds._
67 | 
68 | ## Output format
69 | 
70 | Return:
71 | 
72 | 1. A Markdown table with the specified columns (one row per document).
73 | 2. A single line beginning with **Verdict:** as specified above.
```

01.prework/need-docs.md
```
1 | Okay, do you need any missing documents to implement this correctly?
```

01.prework/prompt-sequence-generator.md
```
1 | # Prompt: Generate Prompt Execution Sequence
2 | 
3 | **Purpose:** Given a high-level goal and a set of available prompts, generate the logical execution sequence required to accomplish that goal by chaining the prompts together.
4 | 
5 | ---
6 | 
7 | ### **Inputs**
8 | 
9 | - **High-Level Goal:** {{high_level_goal}}
10 |   - _A clear, one-sentence description of the final outcome the user wants to achieve._
11 |   - _Example: "Create and document a pull request for the currently staged changes."_
12 | 
13 | - **Available Prompts:**
14 | 
15 |   ```
16 |   {{available_prompts}}
17 |   ```
18 | 
19 |   - _A list of candidate prompt names (e.g., from the output of `rank-root-prompts`)._
20 |   - _Example: ['pr-desc.md', 'commit-msg.md', 'changed-files.md', 'review.md', 'release-notes.md']_
21 | 
22 | - **Context (Optional):** {{context}}
23 |   - _Any additional context, such as the current state of the git repository or specific files of interest._
24 |   - _Example: "The user has already staged files using `git add`."_
25 | 
26 | ---
27 | 
28 | ### **Instructions for the AI**
29 | 
30 | 1. **Analyze the Goal:** Deconstruct the `{{high_level_goal}}` into a series of logical steps required to get from the starting state to the final outcome.
31 | 
32 | 2. **Map Prompts to Steps:** For each logical step, identify the most suitable prompt from the `{{available_prompts}}` list that can perform that step.
33 |     - Consider the inputs and outputs of each prompt to determine dependencies. A prompt's input is often the output of a previous one.
34 | 
35 | 3. **Establish Order:** Arrange the selected prompts into a numbered sequence based on their dependencies. The sequence should represent a complete and logical workflow.
36 | 
37 | 4. **Identify Gaps:** If any necessary step in the workflow cannot be fulfilled by one of the available prompts, explicitly state what action or prompt is missing.
38 | 
39 | ---
40 | 
41 | ### **Required Output Format**
42 | 
43 | **Execution Sequence:**
44 | 
45 | 1. **`[prompt_name_1.md]`**: [Brief justification for why this prompt is first and what it accomplishes.]
46 | 2. **`[prompt_name_2.md]`**: [Brief justification for why this prompt is second, and how it uses the output of the previous step.]
47 | 3. ...
48 | 
49 | **Identified Gaps (if any):**
50 | 
51 | - [Description of a missing step or prompt needed to complete the workflow.]
```

01.prework/rank-root-prompts.md
```
1 | <!--
2 | $1 = command name/identifier
3 | $2 = example user question
4 | $3 = project CWD path to scan for context (defaults to current directory)
5 | $4 = prompt directory path (defaults to "~/.codex/prompts")
6 | $5 = minimum relevance threshold (0–1)
7 | -->
8 | 
9 | # {Context-Aware Prompt Ranking Command}
10 | 
11 | ```md
12 | # Command: $1
13 | 
14 | # Usage: $1 "$2" "$3" "$4" "$5"
15 | 
16 | # Args:
17 | 
18 | # - {{query}}: $2
19 | 
20 | # - {{project_path}}: $3
21 | 
22 | # - {{prompt_path}}: $4
23 | 
24 | # - {{threshold}}: $5
25 | 
26 | prompt = """
27 | Task:
28 | Given a user inquiry ({{query}}) and the context of a software project located at {{project_path}}, your goal is to identify the most relevant prompt-definition file from the directory {{prompt_path}}.
29 | 
30 | Defaults:
31 | 
32 | - If {{project_path}} is missing or blank, use the current working directory.
33 | - If {{prompt_path}} is missing or blank, use "~/.codex/prompts".
34 | 
35 | Do the following:
36 | 
37 | 1. **Analyze Project Context**: Recursively scan {{project_path}} to understand its structure, languages, and purpose. Create a concise summary of the project context.
38 | 2. **Scan Prompts**: List all candidate prompt files in {{prompt_path}} (non-recursively).
39 | 3. **Evaluate Prompts**: For each candidate prompt file:
40 |    a) Read its content.
41 |    b) Create a one-sentence summary of its purpose and domain.
42 |    c) Compute a relevance score from 0 to 1. This score must measure how well the prompt's purpose aligns with the user's {{query}}, considering the project context summary. A higher score means the prompt is a better fit for solving the query within the given project.
43 | 4. **Rank and Filter**: Order the prompts by their relevance score in descending order.
44 | 5. **Generate Output**: Emit a compact markdown table with the columns: `filename | description | match_score` (rounded to 2 decimals).
45 | 
46 | Rules:
47 | 
48 | - The description must be 1–2 sentences capturing the prompt's purpose and domain.
49 | - Only include prompts in the table where `match_score` is greater than or equal to {{threshold}}.
50 | - If no prompts meet the threshold, output a single line: "No prompt exceeds threshold {{threshold}} — recommend creating a new prompt."
51 | 
52 | Acceptance:
53 | 
54 | - If one or more matches meet the {{threshold}}, a markdown table sorted by descending `match_score` is produced.
55 | - Otherwise, the single-line fallback message is produced.
56 | 
57 | !{echo "Scanning project: ${PROJECT_PATH_ARG:-.}"}
58 | !{echo "Searching for prompts in: ${PROMPT_PATH_ARG:-~/.codex/prompts}"}
59 | """
60 | ```
61 | 
62 | ## Output format
63 | 
64 | - **Preferred**: a markdown table with columns `filename | description | match_score` sorted by `match_score` (desc) and filtered by `{{threshold}}`.
65 | - **Fallback**: the exact one-line message when no entries meet `{{threshold}}`.
```

01.prework/research-better-lib.md
```
1 | ---
2 | description: Find a modern, faster JavaScript/TypeScript library alternative to a baseline library
3 | argument-hint: BASELINE_LIB=<library> DOMAIN_USE_CASE=<use-case> CANDIDATE_LIBS=<lib1,lib2,...> [SCALE=<size>] [TOP_N=<number>]
4 | ---
5 | 
6 | ## Problem statement
7 | - Goal: Find a modern, faster JavaScript/TypeScript library for $DOMAIN_USE_CASE that outperforms $BASELINE_LIB in latency and bundle size while maintaining or improving relevance/quality.
8 | - Context: Runs in Node 18+/browser, ESM‑first, TS types, no native deps; list size $SCALE; return $TOP_N suggestions per query.
9 | - Note: If SCALE or TOP_N are not provided, defaults to "5k–50k items" and "top-3" respectively.
10 | 
11 | ## Success metrics (make these explicit)
12 | - P95 latency/query: target <1 ms at 10k items; <5 ms at 50k items (Node laptop). Adjust as needed.
13 | - Bundle size: <25 KB min+gzip for core (no heavy optional modules).
14 | - Quality: NDCG@5 (or task‑specific metric) ≥ $BASELINE_LIB on the same corpus (≥1.0x).
15 | - Features: multi‑field weights, typo tolerance, diacritics, highlight ranges, incremental updates.
16 | - DX: ESM, TS types, active maintenance (<6 months since last release), permissive license.
17 | 
18 | ## Scope and exclusions
19 | - In‑scope: in‑memory, client/Node libraries (no servers, no external indexes).
20 | - Out‑of‑scope: hosted/search servers unless used only for comparison; heavy NLP stacks unless used for query expansion (phase 2).
21 | 
22 | ## Concrete research question to post/search
23 | - "Which modern JS/TS libraries outperform $BASELINE_LIB for $DOMAIN_USE_CASE at $SCALE, with ESM, TS types, and <25 KB gzip bundle? Compare $CANDIDATE_LIBS by p95 latency, relevance (NDCG@5 or equivalent), bundle size, multi‑field weighting, and maintenance."
24 | 
25 | ## Search queries (copy/paste)
26 | - benchmark "$BASELINE_LIB" vs $CANDIDATE_LIBS js performance
27 | - "$CANDIDATE_LIBS vs $BASELINE_LIB" latency relevance "typescript" "esm"
28 | - "$CANDIDATE_LIBS" library benchmark $DOMAIN_USE_CASE
29 | - $CANDIDATE_LIBS benchmark bundle size "diacritics" "highlight"
30 | - $CANDIDATE_LIBS javascript benchmark "multi field"
31 | - $CANDIDATE_LIBS js benchmark in‑memory search
32 | 
33 | ## Shortlist to evaluate
34 | Evaluate the following candidate libraries: $CANDIDATE_LIBS
35 | 
36 | (Example for fuzzy name/description search: fuzzysort, quick‑score, FlexSearch, MiniSearch, Orama/Lyra, fast‑fuzzy, match‑sorter)
37 | 
38 | ## Minimal benchmark design
39 | - Dataset: 25k items with fields relevant to the task (e.g., name, description). Combine synthetic + real.
40 | - Queries: 100 mixed queries (typos, prefixes, mid‑word, camelCase splits, etc.).
41 | - Procedure: warm index; run 1k queries; record mean/p95; compute NDCG@5 (or task metric) vs hand‑labeled relevancy; measure min+gzip bundle.
42 | - Environments: Node 20, Chrome stable. Configs: defaults + one tuned weights (e.g., name:0.7, description:0.3).
43 | 
44 | ## Decision rubric
45 | - Must meet latency + bundle targets and maintain ≥ $BASELINE_LIB quality metric.
46 | - Prefer simple multi‑field API and highlight support.
47 | - Tie‑breaker: maintenance cadence, type safety, ESM‑first.
48 | 
49 | ## Deliverables
50 | - One‑page results table (latency, quality metric, size, features).
51 | - Example integration snippet for our "did‑you‑mean"/ranking path.
52 | - Recommendation + migration notes (config, weights).
53 | 
54 | ---
55 | 
56 | ## Example usage
57 | 
58 | Usage: `/prompts:research-better-lib BASELINE_LIB=Fuse.js DOMAIN_USE_CASE="fuzzy matching tool names + short descriptions (10–500 chars)" CANDIDATE_LIBS="fuzzysort, quick-score, FlexSearch, MiniSearch, Orama" SCALE="5k–50k items" TOP_N="top-3"`
59 | 
60 | **Resulting research question:**
61 | "Which modern JS/TS fuzzy search libraries outperform Fuse.js on 5k–50k items for fuzzy matching tool names + short descriptions (10–500 chars), with ESM, TS types, and <25 KB gzip bundle? Please compare fuzzysort, quick‑score, FlexSearch, MiniSearch, Orama by p95 latency, relevance (NDCG@5), bundle size, multi‑field weighting, and maintenance."
62 | 
```

02.postwork/code-review-high.md
```
1 | ---
2 | description: Comprehensive high-level code review focusing on correctness, security, performance, and integration
3 | argument-hint: TASK=<change-description>
4 | ---
5 | 
6 | <task>
7 | $TASK
8 | </task>
9 | 
10 | <role>
11 |   You are a senior software engineer, security reviewer, and performance specialist. Review the provided change with a focus on correctness, security, performance, integration, test quality, and long-term maintainability. Be precise, cite file paths and line ranges, and prioritize risks that could impact users, data, uptime, or developer velocity.
12 | </role>
13 | 
14 | <objectives>
15 | - Identify correctness defects, code smells, and anti-patterns.
16 | - Surface exploitable security issues and data-protection risks.
17 | - Spot performance/regression risks and complexity hotspots.
18 | - Check integration points (APIs, events, DB, configs, CI/CD, infra) for compatibility and rollout safety.
19 | - Assess tests for sufficiency, signal, reliability, and coverage.
20 | - Recommend minimal, safe, high-leverage improvements and monitoring.
21 | </objectives>
22 | 
23 | <severity_rubric>
24 | - BLOCKER: Exploitable security flaw, data loss risk, broken build/deploy, user-impacting crash, irreversible migration risk, leaked secrets.
25 | - HIGH: Likely prod incident or major regression; authz/auth gaps; significant perf degradation; schema incompatibility.
26 | - MEDIUM: Correctness edge cases; non-exploitable but risky pattern; moderate perf concerns; flaky tests.
27 | - LOW: Maintainability, readability, style, minor test gaps; suggestions.
28 | - NIT: Optional polish.
29 | </severity_rubric>
30 | 
31 | <tasks>
32 | - Scope & Impact: Map all affected files/modules and why each is implicated. Note transitive and runtime impact (build, deploy, config, data).
33 | - Root Cause / Risk Analysis: Explain the change intent, risks introduced, and any hidden assumptions or environmental dependencies.
34 | - Security Review: Use the checklist below; escalate any secret exposure, injection, auth/authz flaws, SSRF/XXE/path traversal, insecure deserialization, command execution, mass assignment, CSRF/XSS, prototype pollution, weak crypto, missing TLS verification, permissive CORS, logging of secrets/PII, dependency vulns, or IaC/container misconfigurations.
35 | - Performance Review: Identify complexity issues, N+1 queries, unbounded loops, memory churn/leaks, blocking I/O on hot paths, missing indexes, cache misuse, chatty network calls, unnecessary allocations/boxing, and concurrency contention.
36 | - Integration Review: Validate API schema changes, versioning, backward/forward compatibility, idempotency, retries/timeouts/circuit breakers, feature-flag rollout, DB migrations (order/locking/rollback), message/event contracts, and config drift.
37 | - Testing Review: Evaluate unit/integration/e2e tests, coverage, negative/property-based cases, concurrency/time-dependent tests, fixture health, determinism, and flakiness risk. Propose a targeted test plan.
38 | - Observability & Operations: Check log levels, PII in logs, correlation/trace IDs, metrics and alerts, runbooks. Recommend what to monitor post-merge.
39 | - Documentation & DX: Flag missing or outdated README/CHANGELOG/ADRs/API docs/config comments/schema diagrams. Note onboarding and maintenance friction.
40 | - Minimal, Safe Fix: Propose the smallest viable change to eliminate blockers/high risks. Include tests and rollout/rollback steps.
41 | </tasks>
42 | 
43 | <detailed_checklist>
44 |   <category name="Correctness & Code Smells">
45 | - Duplicate code / long methods / large classes / deep nesting.
46 | - Leaky abstractions, tight coupling, poor cohesion, improper layering.
47 | - Dead code, unused variables/imports, TODOs that should be addressed now.
48 | - Non-idempotent operations where idempotency is required.
49 | - Edge cases: null/empty/NaN/overflow/encoding/timezone/locale.
50 | - Concurrency: shared state, race conditions, improper locking, async misuse.
51 |   </category>
52 | 
53 |   <category name="Security">
54 | - Secrets in code/logs/env/examples; credential handling, key rotation, KMS/secret manager usage.
55 | - Input validation & output encoding; SQL/NoSQL/LDAP/OS injection; XSS (reflected/stored/DOM); CSRF.
56 | - AuthN/AuthZ: broken access control, least privilege, multi-tenant boundaries, insecure direct object references.
57 | - SSRF/XXE/path traversal/file upload validation; sandboxing for untrusted inputs.
58 | - Crypto: algorithms, modes, IVs, nonces, randomness, key sizes, cert pinning/TLS verification.
59 | - CORS/security headers (CSP/HSTS/X-Frame-Options/SameSite), cookie flags.
60 | - Dependency & supply chain: pinned versions, known CVEs, pre/post-install scripts, integrity checks.
61 | - IaC/Containers: public buckets, open security groups (0.0.0.0/0), missing encryption, root containers, mutable latest tags.
62 | - Data protection & privacy: PII/PHI handling, minimization, retention, encryption at rest/in transit.
63 |   </category>
64 | 
65 |   <category name="Performance">
66 | - Time/space complexity, hot-path allocations, unnecessary synchronization.
67 | - N+1 queries, missing DB indexes, inefficient joins, full scans, pagination vs. streaming.
68 | - Caching: invalidation, eviction, key design, stampedes.
69 | - Network patterns: chattiness, batching, compression, timeouts, backoff.
70 | - Client-side perf (if UI): bundle size/regressions, critical path, images/fonts.
71 |   </category>
72 | 
73 |   <category name="Integration & Rollout Safety">
74 | - Backward/forward compatibility; versioned contracts; consumer-producer alignment.
75 | - DB migrations: zero-downtime (expand/migrate/contract), locks, data backfills, rollback plan.
76 | - Feature flags: default off, kill switch, gradual rollout, owner/expiry.
77 | - Resilience: retries with jitter, timeouts, circuit breakers, idempotency keys.
78 | - Config changes: validation, defaults, environment parity, secrets not in plain text.
79 | - CI/CD: reproducibility, cache safety, test gates, artifact signing.
80 |   </category>
81 | 
82 |   <category name="Testing & Quality Signals">
83 | - Tests exist for new behavior and regressions; meaningful assertions.
84 | - Coverage on critical branches/edge cases; mutation score (if available).
85 | - Isolation: minimal mocking vs. over-mocking; flaky patterns (sleep-based timing, order reliance).
86 | - Property-based/fuzz tests for parsers/validators/serializers.
87 | - Load/soak tests where perf risk exists; snapshot tests stability (if UI).
88 |   </category>
89 | 
90 |   <category name="Docs, Observability, Accessibility, i18n">
91 | - README/CHANGELOG/ADR/API docs updated; code comments for non-obvious logic.
92 | - Logs/metrics/traces with actionable context; PII redaction; alert thresholds.
93 | - Accessibility (if UI): semantics, focus order, labels, contrast, keyboard nav, ARIA use.
94 | - i18n/l10n: hard-coded strings, pluralization, date/time/number formats.
95 |   </category>
96 | </detailed_checklist>
97 | 
98 |   <output_requirements>
99 |     <instructions>
100 | - Produce a concise but comprehensive report.
101 | - Group findings by category and severity.
102 | - Reference exact file paths and line ranges (e.g., src/foo/bar.py:120–147).
103 | - Include brief code excerpts only as necessary (≤20 lines per finding).
104 | - Prefer specific, minimal fixes and tests that maximize risk reduction.
105 | - If information is missing, state the assumption and its impact.
106 |     </instructions>
107 |   </output_requirements>
108 | 
109 |   <report_skeleton>
110 | - Summary:
111 |   - What changed: <concise overview>
112 |   - Top risks: <1-3 bullets>
113 |   - Approval: <approve|comment|request_changes|blocker>
114 | 
115 | - Affected files:
116 |   - <path> — <reason> (<added|modified|deleted>)
117 | 
118 | - Root cause & assumptions:
119 |   - <analysis>
120 |   - Assumptions: <items>
121 | 
122 | - Findings (repeat per finding):
123 |   - [<severity>] [<category>] <short title>
124 |     - Where: <file:line-range>
125 |     - Evidence: <brief snippet_trace>
126 |     - Impact: <what breaks_who is affected>
127 |     - Standards: <CWE/OWASP/Policy refs>
128 |     - Repro: <steps>
129 |     - Recommendation: <minimal fix>
130 |     - Tests: <tests to add_update>
131 | 
132 | - Performance:
133 |   - Hotspots: <items>
134 |   - Complexity notes: <items>
135 |   - Bench/Monitoring plan: <how to measure & watch>
136 | 
137 | - Integration:
138 |   - API/contracts: <compat/versioning/idempotency>
139 |   - DB migrations: <expand-migrate-contract, locks, rollback>
140 |   - Feature flags & rollout: <plan/kill switch_owner>
141 |   - Resilience: <timeouts/retries/circuits>
142 |   - Rollback plan: <how to revert safely>
143 | 
144 | - Testing:
145 |   - Coverage: <statements_branches_critical_paths>
146 |   - Gaps: <cases>
147 |   - Flakiness risks: <items>
148 |   - Targeted test plan: <Given_When_Then bullets>
149 | 
150 | - Docs & Observability:
151 |   - Docs to update/create: <paths/sections>
152 |   - Logs/Metrics/Traces/Alerts: <plan>
153 |   - Runbook: <updates>
154 | 
155 | - Open questions:
156 |   - <items>
157 | 
158 | - Final recommendation:
159 |   - Decision: <approve|comment|request_changes|blocker>
160 |   - Must-fix before merge: <items>
161 |   - Nice-to-have post-merge: <items>
162 |   - Confidence: <low|medium|high>
163 |   </report_skeleton>
164 | 
165 | <process_notes>
166 | - Prioritize BLOCKER/HIGH issues. If any are found, set approval to “blocker” or “request_changes”.
167 | - Favor minimal, safe changes and targeted tests over broad refactors (unless safety demands it).
168 | - If diff is very large, focus on high-risk/new code paths, public interfaces, security-critical modules, and hot paths.
169 | - Reference concrete files/lines. Keep code excerpts minimal (≤20 lines). Do not rewrite large code blocks.
170 | - If required inputs are missing (e.g., DB migration script or API schema), flag as a risk and propose what is needed.
171 | </process_notes>
172 | 
173 | <constraints>
174 | - DO NOT write or generate full code implementations in this review. Provide patch outlines, pseudocode, or stepwise instructions only.
175 | - Maintain confidentiality: if a secret or sensitive data appears, describe it without reproducing it verbatim.
176 | </constraints>
177 | 
178 | <success_criteria>
179 | - Findings are specific, actionable, and ordered by severity and blast radius.
180 | - Every high-risk change has a minimal fix and a concrete test/monitoring plan.
181 | - Output follows the provided report skeleton (markdown text only).
182 | </success_criteria>
183 | 
184 | <reminder>DON'T CODE YET.</reminder>
```

02.postwork/code-review-low.md
```
1 | ---
2 | description: Lightweight code review focusing on code smells, security, performance, and test coverage
3 | argument-hint: TASK=<change-description>
4 | ---
5 | 
6 | <task>
7 | $TASK
8 | </task>
9 | 
10 | ## Role
11 | Senior engineer reviewing **only**: code smells, security, performance, and whether new tests are needed for the new feature.
12 | 
13 | ## Inputs
14 | - {CHANGE_SUMMARY}
15 | - {DIFF} + {FILES}
16 | - {CI_LOGS} {COVERAGE_SUMMARY} (optional)
17 | - {ENVIRONMENT} {API_SCHEMAS} {DB_MIGRATIONS} {DEPENDENCIES} (if relevant)
18 | 
19 | ## What to check
20 | ### Code Smells
21 | - Duplicates, long methods, deep nesting, dead code, unused imports
22 | - Leaky abstractions, tight coupling, improper layering
23 | - Edge cases: null, empty, timezones, encodings
24 | - Concurrency misuse and non-idempotent ops where required
25 | 
26 | ### Security
27 | - Secrets in code/logs; proper secret management
28 | - Input validation and output encoding; SQL/NoSQL/OS injection; XSS/CSRF
29 | - AuthN/AuthZ and multi-tenant boundaries
30 | - SSRF/XXE/path traversal/file upload validation
31 | - Crypto choices; TLS verification; CORS and security headers
32 | - Dependency CVEs and supply-chain risks; IaC/container misconfig
33 | 
34 | ### Performance
35 | - Time/space complexity; hot-path allocations; blocking I/O
36 | - N+1 queries; missing indexes; inefficient joins; full scans
37 | - Caching correctness and stampedes
38 | - Chatty network calls; batching; timeouts; backoff
39 | - Client bundle size and critical path (if UI)
40 | 
41 | ### Tests needed
42 | - Does new behavior have unit/integration/e2e tests
43 | - Edge cases, negative cases, concurrency/time-based cases
44 | - Minimal test plan to guard the change
45 | 
46 | ## Output format
47 | - **Summary**: what changed, top 1–3 risks, **Decision**: approve | request_changes | blocker
48 | - **Findings** grouped by **Smell | Security | Performance | Tests**
49 |   - `[severity] <title>`  
50 |     - Where: `<file:line-range>`  
51 |     - Impact: `<who/what is affected>`  
52 |     - Recommendation: `<smallest safe fix>`  
53 |     - Tests: `<tests to add/update>`
54 | - Cite exact files and line ranges. Keep code excerpts ≤20 lines.
55 | 
56 | ## Constraints
57 | - No full implementations. Pseudocode or patch outline only.
58 | - If data is missing, state the assumption and risk.
```

02.postwork/generate-tests.md
```
1 | ---
2 | phase: 'P5 Quality Gates & Tests'
3 | gate: 'Test Gate'
4 | status: 'targeted unit tests authored for the specified module.'
5 | previous:
6 |   - 
7 | next:
8 |   -
9 | ---
10 | 
11 | # Generate Unit Tests
12 | 
13 | Trigger: /generate <source-file>
14 | 
15 | Purpose: Generate unit tests for a given source file.
16 | 
17 | You are a CLI assistant focused on helping contributors with the task: Generate unit tests for a given source file.
18 | 
19 | ## Steps
20 | 
21 | 1. Inspect `package.json` to identify the unit test framework, runner scripts, and any helper utilities required for the suite.
22 | 2. Review the target source file with `sed -n '1,400p' {{args}}` to catalog exported members, branching logic, and error handling paths that must be exercised.
23 | 3. Outline the test file structure (location, naming, setup/teardown) and propose arrange/act/assert cases that cover happy paths, edge cases, and failure scenarios.
24 | 4. Provide guidance on implementing the tests and how to validate them locally (e.g., `npm test -- <pattern>` or framework-specific commands).
25 | 
26 | ## Output
27 | 
28 | - Begin with a concise summary that restates the goal: Generate unit tests for a given source file.
29 | - List the recommended test files, describe each test case, and highlight coverage gaps they close.
30 | - Call out the command(s) to run the new tests and any fixtures or mocks required.
31 | - Document the evidence you used (e.g., `package.json`, specific functions/branches in the source file) so maintainers can trust the conclusion.
32 | 
33 | ## Example
34 | 
35 | **Input**
36 | 
37 | ```
38 | src/components/Button.tsx
39 | ```
40 | 
41 | **Output**
42 | 
43 | - Summary: Author React Testing Library unit tests for `Button` to cover rendering, disabled behavior, and click handling.
44 | - Create `src/components/__tests__/Button.test.tsx` that:
45 |   - Renders the button label and asserts it matches `props.children`.
46 |   - Verifies `onClick` fires once when the button is enabled and is skipped when `disabled` is true.
47 |   - Confirms the `variant="primary"` branch applies the `btn-primary` class.
48 | - Validation: Run `npm test -- Button.test.tsx` to execute the suite.
49 | - Evidence: `package.json` (scripts.test uses Jest + RTL), component branches in `src/components/Button.tsx` (disabled guard, variant styling).
```

02.postwork/problem-analyzer.md
```
1 | ---
2 | description: Analyze a problem by locating affected files, root cause, and proposing minimal fixes
3 | argument-hint: PROBLEM=<problem-description>
4 | ---
5 | 
6 | <problem>
7 | $PROBLEM
8 | </problem>
9 | 
10 | Tasks:
11 | 1) Locate all files/modules affected by the issue. List paths and why each is implicated.
12 | 2) Explain the root cause(s): what changed, how it propagates to the failure, and any environmental factors.
13 | 3) Propose the minimal, safe fix. Include code-level steps, side effects, and tests to add/update.
14 | 4) Flag any missing or outdated documentation/configs/schemas that should be updated or added (especially if code appears outdated vs. current behavior). Specify exact docs/sections to create or amend.
15 | 
16 | Output format:
17 | - Affected files:
18 |   - <path>: <reason>
19 | - Root cause:
20 |   - <concise explanation>
21 | - Proposed fix:
22 |   - <steps/patch outline>
23 |   - Tests:
24 | - Documentation gaps:
25 |   - <doc_section_what_to_update_add>
26 | - Open questions/assumptions:
27 |   - <items>
```

02.postwork/refactor-code.md
```
1 | ---
2 | description: Refactor code with a specific goal, keeping changes isolated
3 | argument-hint: GOAL=<refactoring-goal-description>
4 | ---
5 | 
6 | <refactoring_goal>
7 | $GOAL
8 | </refactoring_goal>
9 | 
10 | Task: <refactoring_goal>
11 | 
12 | - Keep the commit isolated to this feature.
13 | - Document but do not fix unrelated problems you find.
14 | - Never add fallbacks/backward-compability/feature flags, we are always build the full new refactored solution.
```

02.postwork/ui-screenshots.md
```
1 | ---
2 | phase: 'P4 Frontend UX'
3 | gate: 'Accessibility checks queued'
4 | status: 'capture UX issues and backlog fixes.'
5 | previous:
6 |   -
7 |   -
8 | next:
9 |   -
10 |   - 
11 | ---
12 | 
13 | # UI Screenshots
14 | 
15 | Trigger: /ui-screenshots
16 | 
17 | Purpose: Analyze screenshots for UI bugs or inspiration and propose actionable UI changes.
18 | 
19 | ## Steps
20 | 
21 | 1. Accept screenshot paths or links.
22 | 2. Describe visual hierarchy, spacing, contrast, and alignment issues.
23 | 3. Output concrete CSS or component changes.
24 | 
25 | ## Output format
26 | 
27 | - Issue list and code snippets to fix visuals.
```
