<filetree>
Project Structure:
└── .gemini
    └── commands
        └── tm
            ├── add-dependency.toml
            ├── add-subtask.toml
            ├── add-task.toml
            ├── analyze-complexity.toml
            ├── analyze-project.toml
            ├── auto-implement-tasks.toml
            ├── command-pipeline.toml
            ├── complexity-report.toml
            ├── convert-task-to-subtask.toml
            ├── expand-all-tasks.toml
            ├── expand-task.toml
            ├── fix-dependencies.toml
            ├── help.toml
            ├── init-project-quick.toml
            ├── init-project.toml
            ├── install-taskmaster.toml
            ├── learn.toml
            ├── list-tasks-by-status.toml
            ├── list-tasks-with-subtasks.toml
            ├── list-tasks.toml
            ├── next-task.toml
            ├── parse-prd-with-research.toml
            ├── parse-prd.toml
            ├── project-status.toml
            ├── quick-install-taskmaster.toml
            ├── remove-all-subtasks.toml
            ├── remove-dependency.toml
            ├── remove-subtask.toml
            ├── remove-subtasks.toml
            ├── remove-task.toml
            ├── setup-models.toml
            ├── show-task.toml
            ├── smart-workflow.toml
            ├── sync-readme.toml
            ├── tm-main.toml
            ├── to-cancelled.toml
            ├── to-deferred.toml
            ├── to-done.toml
            ├── to-in-progress.toml
            ├── to-pending.toml
            ├── to-review.toml
            ├── update-single-task.toml
            ├── update-task.toml
            ├── update-tasks-from-id.toml
            ├── validate-dependencies.toml
            └── view-models.toml

</filetree>

<source_code>
.gemini/commands/tm/add-dependency.toml
```
description="Add Dependency"
prompt = """
Add a dependency between tasks.

Arguments: $ARGUMENTS

Parse the task IDs to establish dependency relationship.

## Adding Dependencies

Creates a dependency where one task must be completed before another can start.

## Argument Parsing

Parse natural language or IDs:
- "make 5 depend on 3" → task 5 depends on task 3
- "5 needs 3" → task 5 depends on task 3
- "5 3" → task 5 depends on task 3
- "5 after 3" → task 5 depends on task 3

## Execution

```bash
task-master add-dependency --id=<task-id> --depends-on=<dependency-id>
```

## Validation

Before adding:
1. **Verify both tasks exist**
2. **Check for circular dependencies**
3. **Ensure dependency makes logical sense**
4. **Warn if creating complex chains**

## Smart Features

- Detect if dependency already exists
- Suggest related dependencies
- Show impact on task flow
- Update task priorities if needed

## Post-Addition

After adding dependency:
1. Show updated dependency graph
2. Identify any newly blocked tasks
3. Suggest task order changes
4. Update project timeline

## Example Flows

```
/taskmaster:add-dependency 5 needs 3
→ Task #5 now depends on Task #3
→ Task #5 is now blocked until #3 completes
→ Suggested: Also consider if #5 needs #4
```
"""
```

.gemini/commands/tm/add-subtask.toml
```
description="Add Subtask"
prompt = """
Add a subtask to a parent task.

Arguments: $ARGUMENTS

Parse arguments to create a new subtask or convert existing task.

## Adding Subtasks

Creates subtasks to break down complex parent tasks into manageable pieces.

## Argument Parsing

Flexible natural language:
- "add subtask to 5: implement login form"
- "break down 5 with: setup, implement, test"
- "subtask for 5: handle edge cases"
- "5: validate user input" → adds subtask to task 5

## Execution Modes

### 1. Create New Subtask
```bash
task-master add-subtask --parent=<id> --title="<title>" --description="<desc>"
```

### 2. Convert Existing Task
```bash
task-master add-subtask --parent=<id> --task-id=<existing-id>
```

## Smart Features

1. **Automatic Subtask Generation**
   - If title contains "and" or commas, create multiple
   - Suggest common subtask patterns
   - Inherit parent's context

2. **Intelligent Defaults**
   - Priority based on parent
   - Appropriate time estimates
   - Logical dependencies between subtasks

3. **Validation**
   - Check parent task complexity
   - Warn if too many subtasks
   - Ensure subtask makes sense

## Creation Process

1. Parse parent task context
2. Generate subtask with ID like "5.1"
3. Set appropriate defaults
4. Link to parent task
5. Update parent's time estimate

## Example Flows

```
/taskmaster:add-subtask to 5: implement user authentication
→ Created subtask #5.1: "implement user authentication"
→ Parent task #5 now has 1 subtask
→ Suggested next subtasks: tests, documentation

/taskmaster:add-subtask 5: setup, implement, test
→ Created 3 subtasks:
  #5.1: setup
  #5.2: implement
  #5.3: test
```

## Post-Creation

- Show updated task hierarchy
- Suggest logical next subtasks
- Update complexity estimates
- Recommend subtask order
"""
```

.gemini/commands/tm/add-task.toml
```
description="Add Task"
prompt = """
Add new tasks with intelligent parsing and context awareness.

Arguments: $ARGUMENTS

## Smart Task Addition

Parse natural language to create well-structured tasks.

### 1. **Input Understanding**

I'll intelligently parse your request:
- Natural language → Structured task
- Detect priority from keywords (urgent, ASAP, important)
- Infer dependencies from context
- Suggest complexity based on description
- Determine task type (feature, bug, refactor, test, docs)

### 2. **Smart Parsing Examples**

**"Add urgent task to fix login bug"**
→ Title: Fix login bug
→ Priority: high
→ Type: bug
→ Suggested complexity: medium

**"Create task for API documentation after task 23 is done"**
→ Title: API documentation
→ Dependencies: [23]
→ Type: documentation
→ Priority: medium

**"Need to refactor auth module - depends on 12 and 15, high complexity"**
→ Title: Refactor auth module
→ Dependencies: [12, 15]
→ Complexity: high
→ Type: refactor

### 3. **Context Enhancement**

Based on current project state:
- Suggest related existing tasks
- Warn about potential conflicts
- Recommend dependencies
- Propose subtasks if complex

### 4. **Interactive Refinement**

```yaml
Task Preview:
─────────────
Title: [Extracted title]
Priority: [Inferred priority]
Dependencies: [Detected dependencies]
Complexity: [Estimated complexity]

Suggestions:
- Similar task #34 exists, consider as dependency?
- This seems complex, break into subtasks?
- Tasks #45-47 work on same module
```

### 5. **Validation & Creation**

Before creating:
- Validate dependencies exist
- Check for duplicates
- Ensure logical ordering
- Verify task completeness

### 6. **Smart Defaults**

Intelligent defaults based on:
- Task type patterns
- Team conventions
- Historical data
- Current sprint/phase

Result: High-quality tasks from minimal input.
"""
```

.gemini/commands/tm/analyze-complexity.toml
```
description="Analyze Complexity"
prompt = """
Analyze task complexity and generate expansion recommendations.

Arguments: $ARGUMENTS

Perform deep analysis of task complexity across the project.

## Complexity Analysis

Uses AI to analyze tasks and recommend which ones need breakdown.

## Execution Options

```bash
task-master analyze-complexity [--research] [--threshold=5]
```

## Analysis Parameters

- `--research` → Use research AI for deeper analysis
- `--threshold=5` → Only flag tasks above complexity 5
- Default: Analyze all pending tasks

## Analysis Process

### 1. **Task Evaluation**
For each task, AI evaluates:
- Technical complexity
- Time requirements
- Dependency complexity
- Risk factors
- Knowledge requirements

### 2. **Complexity Scoring**
Assigns score 1-10 based on:
- Implementation difficulty
- Integration challenges
- Testing requirements
- Unknown factors
- Technical debt risk

### 3. **Recommendations**
For complex tasks:
- Suggest expansion approach
- Recommend subtask breakdown
- Identify risk areas
- Propose mitigation strategies

## Smart Analysis Features

1. **Pattern Recognition**
   - Similar task comparisons
   - Historical complexity accuracy
   - Team velocity consideration
   - Technology stack factors

2. **Contextual Factors**
   - Team expertise
   - Available resources
   - Timeline constraints
   - Business criticality

3. **Risk Assessment**
   - Technical risks
   - Timeline risks
   - Dependency risks
   - Knowledge gaps

## Output Format

```
Task Complexity Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

High Complexity Tasks (>7):
📍 #5 "Implement real-time sync" - Score: 9/10
   Factors: WebSocket complexity, state management, conflict resolution
   Recommendation: Expand into 5-7 subtasks
   Risks: Performance, data consistency

📍 #12 "Migrate database schema" - Score: 8/10
   Factors: Data migration, zero downtime, rollback strategy
   Recommendation: Expand into 4-5 subtasks
   Risks: Data loss, downtime

Medium Complexity Tasks (5-7):
📍 #23 "Add export functionality" - Score: 6/10
   Consider expansion if timeline tight

Low Complexity Tasks (<5):
✅ 15 tasks - No expansion needed

Summary:
- Expand immediately: 2 tasks
- Consider expanding: 5 tasks
- Keep as-is: 15 tasks
```

## Actionable Output

For each high-complexity task:
1. Complexity score with reasoning
2. Specific expansion suggestions
3. Risk mitigation approaches
4. Recommended subtask structure

## Integration

Results are:
- Saved to `.taskmaster/reports/complexity-analysis.md`
- Used by expand command
- Inform sprint planning
- Guide resource allocation

## Next Steps

After analysis:
```
/taskmaster:expand 5    # Expand specific task
/taskmaster:expand-all  # Expand all recommended
/taskmaster:complexity-report  # View detailed report
```
"""
```

.gemini/commands/tm/analyze-project.toml
```
description="Analyze Project"
prompt = """
Advanced project analysis with actionable insights and recommendations.

Arguments: $ARGUMENTS

## Comprehensive Project Analysis

Multi-dimensional analysis based on requested focus area.

### 1. **Analysis Modes**

Based on $ARGUMENTS:
- "velocity" → Sprint velocity and trends
- "quality" → Code quality metrics
- "risk" → Risk assessment and mitigation
- "dependencies" → Dependency graph analysis
- "team" → Workload and skill distribution
- "architecture" → System design coherence
- Default → Full spectrum analysis

### 2. **Velocity Analytics**

```
📊 Velocity Analysis
━━━━━━━━━━━━━━━━━━━
Current Sprint: 24 points/week ↗️ +20%
Rolling Average: 20 points/week
Efficiency: 85% (17/20 tasks on time)

Bottlenecks Detected:
- Code review delays (avg 4h wait)
- Test environment availability
- Dependency on external team

Recommendations:
1. Implement parallel review process
2. Add staging environment
3. Mock external dependencies
```

### 3. **Risk Assessment**

**Technical Risks**
- High complexity tasks without backup assignee
- Single points of failure in architecture
- Insufficient test coverage in critical paths
- Technical debt accumulation rate

**Project Risks**
- Critical path dependencies
- Resource availability gaps
- Deadline feasibility analysis
- Scope creep indicators

### 4. **Dependency Intelligence**

Visual dependency analysis:
```
Critical Path:
#12 → #15 → #23 → #45 → #50 (20 days)
         ↘ #24 → #46 ↗

Optimization: Parallelize #15 and #24
Time Saved: 3 days
```

### 5. **Quality Metrics**

**Code Quality**
- Test coverage trends
- Complexity scores
- Technical debt ratio
- Review feedback patterns

**Process Quality**
- Rework frequency
- Bug introduction rate
- Time to resolution
- Knowledge distribution

### 6. **Predictive Insights**

Based on patterns:
- Completion probability by deadline
- Resource needs projection
- Risk materialization likelihood
- Suggested interventions

### 7. **Executive Dashboard**

High-level summary with:
- Health score (0-100)
- Top 3 risks
- Top 3 opportunities
- Recommended actions
- Success probability

Result: Data-driven decisions with clear action paths.
"""
```

.gemini/commands/tm/auto-implement-tasks.toml
```
description="Auto Implement Tasks"
prompt = """
Enhanced auto-implementation with intelligent code generation and testing.

Arguments: $ARGUMENTS

## Intelligent Auto-Implementation

Advanced implementation with context awareness and quality checks.

### 1. **Pre-Implementation Analysis**

Before starting:
- Analyze task complexity and requirements
- Check codebase patterns and conventions
- Identify similar completed tasks
- Assess test coverage needs
- Detect potential risks

### 2. **Smart Implementation Strategy**

Based on task type and context:

**Feature Tasks**
1. Research existing patterns
2. Design component architecture
3. Implement with tests
4. Integrate with system
5. Update documentation

**Bug Fix Tasks**
1. Reproduce issue
2. Identify root cause
3. Implement minimal fix
4. Add regression tests
5. Verify side effects

**Refactoring Tasks**
1. Analyze current structure
2. Plan incremental changes
3. Maintain test coverage
4. Refactor step-by-step
5. Verify behavior unchanged

### 3. **Code Intelligence**

**Pattern Recognition**
- Learn from existing code
- Follow team conventions
- Use preferred libraries
- Match style guidelines

**Test-Driven Approach**
- Write tests first when possible
- Ensure comprehensive coverage
- Include edge cases
- Performance considerations

### 4. **Progressive Implementation**

Step-by-step with validation:
```
Step 1/5: Setting up component structure ✓
Step 2/5: Implementing core logic ✓
Step 3/5: Adding error handling ⚡ (in progress)
Step 4/5: Writing tests ⏳
Step 5/5: Integration testing ⏳

Current: Adding try-catch blocks and validation...
```

### 5. **Quality Assurance**

Automated checks:
- Linting and formatting
- Test execution
- Type checking
- Dependency validation
- Performance analysis

### 6. **Smart Recovery**

If issues arise:
- Diagnostic analysis
- Suggestion generation
- Fallback strategies
- Manual intervention points
- Learning from failures

### 7. **Post-Implementation**

After completion:
- Generate PR description
- Update documentation
- Log lessons learned
- Suggest follow-up tasks
- Update task relationships

Result: High-quality, production-ready implementations.
"""
```

.gemini/commands/tm/command-pipeline.toml
```
description="Command Pipeline"
prompt = """
Execute a pipeline of commands based on a specification.

Arguments: $ARGUMENTS

## Command Pipeline Execution

Parse pipeline specification from arguments. Supported formats:

### Simple Pipeline
`init → expand-all → sprint-plan`

### Conditional Pipeline
`status → if:pending>10 → sprint-plan → else → next`

### Iterative Pipeline
`for:pending-tasks → expand → complexity-check`

### Smart Pipeline Patterns

**1. Project Setup Pipeline**
```
init [prd] →
expand-all →
complexity-report →
sprint-plan →
show first-sprint
```

**2. Daily Work Pipeline**
```
standup →
if:in-progress → continue →
else → next → start
```

**3. Task Completion Pipeline**
```
complete [id] →
git-commit →
if:blocked-tasks-freed → show-freed →
next
```

**4. Quality Check Pipeline**
```
list in-progress →
for:each → check-idle-time →
if:idle>1day → prompt-update
```

### Pipeline Features

**Variables**
- Store results: `status → $count=pending-count`
- Use in conditions: `if:$count>10`
- Pass between commands: `expand $high-priority-tasks`

**Error Handling**
- On failure: `try:complete → catch:show-blockers`
- Skip on error: `optional:test-run`
- Retry logic: `retry:3:commit`

**Parallel Execution**
- Parallel branches: `[analyze | test | lint]`
- Join results: `parallel → join:report`

### Execution Flow

1. Parse pipeline specification
2. Validate command sequence
3. Execute with state passing
4. Handle conditions and loops
5. Aggregate results
6. Show summary

This enables complex workflows like:
`parse-prd → expand-all → filter:complex>70 → assign:senior → sprint-plan:weighted`
"""
```

.gemini/commands/tm/complexity-report.toml
```
description="Complexity Report"
prompt = """
Display the task complexity analysis report.

Arguments: $ARGUMENTS

View the detailed complexity analysis generated by analyze-complexity command.

## Viewing Complexity Report

Shows comprehensive task complexity analysis with actionable insights.

## Execution

```bash
task-master complexity-report [--file=<path>]
```

## Report Location

Default: `.taskmaster/reports/complexity-analysis.md`
Custom: Specify with --file parameter

## Report Contents

### 1. **Executive Summary**
```
Complexity Analysis Summary
━━━━━━━━━━━━━━━━━━━━━━━━
Analysis Date: 2024-01-15
Tasks Analyzed: 32
High Complexity: 5 (16%)
Medium Complexity: 12 (37%)
Low Complexity: 15 (47%)

Critical Findings:
- 5 tasks need immediate expansion
- 3 tasks have high technical risk
- 2 tasks block critical path
```

### 2. **Detailed Task Analysis**
For each complex task:
- Complexity score breakdown
- Contributing factors
- Specific risks identified
- Expansion recommendations
- Similar completed tasks

### 3. **Risk Matrix**
Visual representation:
```
Risk vs Complexity Matrix
━━━━━━━━━━━━━━━━━━━━━━━
High Risk  | #5(9) #12(8) | #23(6)
Med Risk   | #34(7)       | #45(5) #67(5)
Low Risk   | #78(8)       | [15 tasks]
           | High Complex  | Med Complex
```

### 4. **Recommendations**

**Immediate Actions:**
1. Expand task #5 - Critical path + high complexity
2. Expand task #12 - High risk + dependencies
3. Review task #34 - Consider splitting

**Sprint Planning:**
- Don't schedule multiple high-complexity tasks together
- Ensure expertise available for complex tasks
- Build in buffer time for unknowns

## Interactive Features

When viewing report:
1. **Quick Actions**
   - Press 'e' to expand a task
   - Press 'd' for task details
   - Press 'r' to refresh analysis

2. **Filtering**
   - View by complexity level
   - Filter by risk factors
   - Show only actionable items

3. **Export Options**
   - Markdown format
   - CSV for spreadsheets
   - JSON for tools

## Report Intelligence

- Compares with historical data
- Shows complexity trends
- Identifies patterns
- Suggests process improvements

## Integration

Use report for:
- Sprint planning sessions
- Resource allocation
- Risk assessment
- Team discussions
- Client updates

## Example Usage

```
/taskmaster:complexity-report
→ Opens latest analysis

/taskmaster:complexity-report --file=archived/2024-01-01.md
→ View historical analysis

After viewing:
/taskmaster:expand 5
→ Expand high-complexity task
```
"""
```

.gemini/commands/tm/convert-task-to-subtask.toml
```
description="Convert Task To Subtask"
prompt = """
Convert an existing task into a subtask.

Arguments: $ARGUMENTS

Parse parent ID and task ID to convert.

## Task Conversion

Converts an existing standalone task into a subtask of another task.

## Argument Parsing

- "move task 8 under 5"
- "make 8 a subtask of 5"
- "nest 8 in 5"
- "5 8" → make task 8 a subtask of task 5

## Execution

```bash
task-master add-subtask --parent=<parent-id> --task-id=<task-to-convert>
```

## Pre-Conversion Checks

1. **Validation**
   - Both tasks exist and are valid
   - No circular parent relationships
   - Task isn't already a subtask
   - Logical hierarchy makes sense

2. **Impact Analysis**
   - Dependencies that will be affected
   - Tasks that depend on converting task
   - Priority alignment needed
   - Status compatibility

## Conversion Process

1. Change task ID from "8" to "5.1" (next available)
2. Update all dependency references
3. Inherit parent's context where appropriate
4. Adjust priorities if needed
5. Update time estimates

## Smart Features

- Preserve task history
- Maintain dependencies
- Update all references
- Create conversion log

## Example

```
/taskmaster:add-subtask/from-task 5 8
→ Converting: Task #8 becomes subtask #5.1
→ Updated: 3 dependency references
→ Parent task #5 now has 1 subtask
→ Note: Subtask inherits parent's priority

Before: #8 "Implement validation" (standalone)
After:  #5.1 "Implement validation" (subtask of #5)
```

## Post-Conversion

- Show new task hierarchy
- List updated dependencies
- Verify project integrity
- Suggest related conversions
"""
```

.gemini/commands/tm/expand-all-tasks.toml
```
description="Expand All Tasks"
prompt = """
Expand all pending tasks that need subtasks.

## Bulk Task Expansion

Intelligently expands all tasks that would benefit from breakdown.

## Execution

```bash
task-master expand --all
```

## Smart Selection

Only expands tasks that:
- Are marked as pending
- Have high complexity (>5)
- Lack existing subtasks
- Would benefit from breakdown

## Expansion Process

1. **Analysis Phase**
   - Identify expansion candidates
   - Group related tasks
   - Plan expansion strategy

2. **Batch Processing**
   - Expand tasks in logical order
   - Maintain consistency
   - Preserve relationships
   - Optimize for parallelism

3. **Quality Control**
   - Ensure subtask quality
   - Avoid over-decomposition
   - Maintain task coherence
   - Update dependencies

## Options

- Add `force` to expand all regardless of complexity
- Add `research` for enhanced AI analysis

## Results

After bulk expansion:
- Summary of tasks expanded
- New subtask count
- Updated complexity metrics
- Suggested task order
"""
```

.gemini/commands/tm/expand-task.toml
```
description="Expand Task"
prompt = """
Break down a complex task into subtasks.

Arguments: $ARGUMENTS (task ID)

## Intelligent Task Expansion

Analyzes a task and creates detailed subtasks for better manageability.

## Execution

```bash
task-master expand --id=$ARGUMENTS
```

## Expansion Process

1. **Task Analysis**
   - Review task complexity
   - Identify components
   - Detect technical challenges
   - Estimate time requirements

2. **Subtask Generation**
   - Create 3-7 subtasks typically
   - Each subtask 1-4 hours
   - Logical implementation order
   - Clear acceptance criteria

3. **Smart Breakdown**
   - Setup/configuration tasks
   - Core implementation
   - Testing components
   - Integration steps
   - Documentation updates

## Enhanced Features

Based on task type:
- **Feature**: Setup → Implement → Test → Integrate
- **Bug Fix**: Reproduce → Diagnose → Fix → Verify
- **Refactor**: Analyze → Plan → Refactor → Validate

## Post-Expansion

After expansion:
1. Show subtask hierarchy
2. Update time estimates
3. Suggest implementation order
4. Highlight critical path
"""
```

.gemini/commands/tm/fix-dependencies.toml
```
description="Fix Dependencies"
prompt = """
Automatically fix dependency issues found during validation.

## Automatic Dependency Repair

Intelligently fixes common dependency problems while preserving project logic.

## Execution

```bash
task-master fix-dependencies
```

## What Gets Fixed

### 1. **Auto-Fixable Issues**
- Remove references to deleted tasks
- Break simple circular dependencies
- Remove self-dependencies
- Clean up duplicate dependencies

### 2. **Smart Resolutions**
- Reorder dependencies to maintain logic
- Suggest task merging for over-dependent tasks
- Flatten unnecessary dependency chains
- Remove redundant transitive dependencies

### 3. **Manual Review Required**
- Complex circular dependencies
- Critical path modifications
- Business logic dependencies
- High-impact changes

## Fix Process

1. **Analysis Phase**
   - Run validation check
   - Categorize issues by type
   - Determine fix strategy

2. **Execution Phase**
   - Apply automatic fixes
   - Log all changes made
   - Preserve task relationships

3. **Verification Phase**
   - Re-validate after fixes
   - Show before/after comparison
   - Highlight manual fixes needed

## Smart Features

- Preserves intended task flow
- Minimal disruption approach
- Creates fix history/log
- Suggests manual interventions

## Output Example

```
Dependency Auto-Fix Report
━━━━━━━━━━━━━━━━━━━━━━━━
Fixed Automatically:
✅ Removed 2 references to deleted tasks
✅ Resolved 1 self-dependency
✅ Cleaned 3 redundant dependencies

Manual Review Needed:
⚠️ Complex circular dependency: #12 → #15 → #18 → #12
  Suggestion: Make #15 not depend on #12
⚠️ Task #45 has 8 dependencies
  Suggestion: Break into subtasks

Run '/taskmaster:validate-dependencies' to verify fixes
```

## Safety

- Preview mode available
- Rollback capability
- Change logging
- No data loss
"""
```

.gemini/commands/tm/help.toml
```
description="Help"
prompt = """
Show help for Task Master AI commands.

Arguments: $ARGUMENTS

Display help for Task Master commands and available options.

## Task Master AI Command Help

### Quick Navigation

Type `/taskmaster:` and use tab completion to explore all commands.

### Command Categories

#### 🚀 Setup & Installation
- `/taskmaster:install-taskmaster` - Comprehensive installation guide
- `/taskmaster:quick-install-taskmaster` - One-line global install

#### 📋 Project Setup
- `/taskmaster:init-project` - Initialize new project
- `/taskmaster:init-project-quick` - Quick setup with auto-confirm
- `/taskmaster:view-models` - View AI configuration
- `/taskmaster:setup-models` - Configure AI providers

#### 🎯 Task Generation
- `/taskmaster:parse-prd` - Generate tasks from PRD
- `/taskmaster:parse-prd-with-research` - Enhanced parsing
- `/taskmaster:generate-tasks` - Create task files

#### 📝 Task Management
- `/taskmaster:list-tasks` - List all tasks
- `/taskmaster:list-tasks-by-status` - List tasks filtered by status
- `/taskmaster:list-tasks-with-subtasks` - List tasks with subtasks
- `/taskmaster:show-task` - Display task details
- `/taskmaster:add-task` - Create new task
- `/taskmaster:update-task` - Update single task
- `/taskmaster:update-tasks-from-id` - Update multiple tasks
- `/taskmaster:next-task` - Get next task recommendation

#### 🔄 Status Management
- `/taskmaster:to-pending` - Set task to pending
- `/taskmaster:to-in-progress` - Set task to in-progress
- `/taskmaster:to-done` - Set task to done
- `/taskmaster:to-review` - Set task to review
- `/taskmaster:to-deferred` - Set task to deferred
- `/taskmaster:to-cancelled` - Set task to cancelled

#### 🔍 Analysis & Breakdown
- `/taskmaster:analyze-complexity` - Analyze task complexity
- `/taskmaster:complexity-report` - View complexity report
- `/taskmaster:expand-task` - Break down complex task
- `/taskmaster:expand-all-tasks` - Expand all eligible tasks

#### 🔗 Dependencies
- `/taskmaster:add-dependency` - Add task dependency
- `/taskmaster:remove-dependency` - Remove dependency
- `/taskmaster:validate-dependencies` - Check for issues
- `/taskmaster:fix-dependencies` - Auto-fix dependency issues

#### 📦 Subtasks
- `/taskmaster:add-subtask` - Add subtask to task
- `/taskmaster:convert-task-to-subtask` - Convert task to subtask
- `/taskmaster:remove-subtask` - Remove subtask
- `/taskmaster:remove-subtasks` - Clear specific task subtasks
- `/taskmaster:remove-all-subtasks` - Clear all subtasks

#### 🗑️ Task Removal
- `/taskmaster:remove-task` - Remove task permanently

#### 🤖 Workflows
- `/taskmaster:smart-workflow` - Intelligent workflows
- `/taskmaster:command-pipeline` - Command chaining
- `/taskmaster:auto-implement-tasks` - Auto-implementation

#### 📊 Utilities
- `/taskmaster:analyze-project` - Project analysis
- `/taskmaster:project-status` - Project dashboard
- `/taskmaster:sync-readme` - Sync README with tasks
- `/taskmaster:learn` - Interactive learning
- `/taskmaster:tm-main` - Main Task Master interface

### Quick Start Examples

```
/taskmaster:list-tasks
/taskmaster:show-task 1.2
/taskmaster:add-task
/taskmaster:next-task
```

### Getting Started

1. Install: `/taskmaster:quick-install-taskmaster`
2. Initialize: `/taskmaster:init-project-quick`
3. Learn: `/taskmaster:learn`
4. Work: `/taskmaster:smart-workflow`

For detailed command info, run the specific command with `--help` or check command documentation.
"""
```

.gemini/commands/tm/init-project-quick.toml
```
description="Init Project Quick"
prompt = """
Quick initialization with auto-confirmation.

Arguments: $ARGUMENTS

Initialize a Task Master project without prompts, accepting all defaults.

## Quick Setup

```bash
task-master init -y
```

## What It Does

1. Creates `.taskmaster/` directory structure
2. Initializes empty `tasks.json`
3. Sets up default configuration
4. Uses directory name as project name
5. Skips all confirmation prompts

## Smart Defaults

- Project name: Current directory name
- Description: "Task Master Project"
- Model config: Existing environment vars
- Task structure: Standard format

## Next Steps

After quick init:
1. Configure AI models if needed:
   ```
   /taskmaster:models/setup
   ```

2. Parse PRD if available:
   ```
   /taskmaster:parse-prd <file>
   ```

3. Or create first task:
   ```
   /taskmaster:add-task create initial setup
   ```

Perfect for rapid project setup!
"""
```

.gemini/commands/tm/init-project.toml
```
description="Init Project"
prompt = """
Initialize a new Task Master project.

Arguments: $ARGUMENTS

Parse arguments to determine initialization preferences.

## Initialization Process

1. **Parse Arguments**
   - PRD file path (if provided)
   - Project name
   - Auto-confirm flag (-y)

2. **Project Setup**
   ```bash
   task-master init
   ```

3. **Smart Initialization**
   - Detect existing project files
   - Suggest project name from directory
   - Check for git repository
   - Verify AI provider configuration

## Configuration Options

Based on arguments:
- `quick` / `-y` → Skip confirmations
- `<file.md>` → Use as PRD after init
- `--name=<name>` → Set project name
- `--description=<desc>` → Set description

## Post-Initialization

After successful init:
1. Show project structure created
2. Verify AI models configured
3. Suggest next steps:
   - Parse PRD if available
   - Configure AI providers
   - Set up git hooks
   - Create first tasks

## Integration

If PRD file provided:
```
/taskmaster:init my-prd.md
→ Automatically runs parse-prd after init
```
"""
```

.gemini/commands/tm/install-taskmaster.toml
```
description="Install TaskMaster"
prompt = """
Check if Task Master is installed and install it if needed.

This command helps you get Task Master set up globally on your system.

## Detection and Installation Process

1. **Check Current Installation**
   ```bash
   # Check if task-master command exists
   which task-master || echo "Task Master not found"

   # Check npm global packages
   npm list -g task-master-ai
   ```

2. **System Requirements Check**
   ```bash
   # Verify Node.js is installed
   node --version

   # Verify npm is installed
   npm --version

   # Check Node version (need 16+)
   ```

3. **Install Task Master Globally**
   If not installed, run:
   ```bash
   npm install -g task-master-ai
   ```

4. **Verify Installation**
   ```bash
   # Check version
   task-master --version

   # Verify command is available
   which task-master
   ```

5. **Initial Setup**
   ```bash
   # Initialize in current directory
   task-master init
   ```

6. **Configure AI Provider**
   Ensure you have at least one AI provider API key set:
   ```bash
   # Check current configuration
   task-master models --status

   # If no API keys found, guide setup
   echo "You'll need at least one API key:"
   echo "- ANTHROPIC_API_KEY for Claude"
   echo "- OPENAI_API_KEY for GPT models"
   echo "- PERPLEXITY_API_KEY for research"
   echo ""
   echo "Set them in your shell profile or .env file"
   ```

7. **Quick Test**
   ```bash
   # Create a test PRD
   echo "Build a simple hello world API" > test-prd.txt

   # Try parsing it
   task-master parse-prd test-prd.txt -n 3
   ```

## Troubleshooting

If installation fails:

**Permission Errors:**
```bash
# Try with sudo (macOS/Linux)
sudo npm install -g task-master-ai

# Or fix npm permissions
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
```

**Network Issues:**
```bash
# Use different registry
npm install -g task-master-ai --registry https://registry.npmjs.org/
```

**Node Version Issues:**
```bash
# Install Node 20+ via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

## Success Confirmation

Once installed, you should see:
```
✅ Task Master installed
✅ Command 'task-master' available globally
✅ AI provider configured
✅ Ready to use slash commands!

Try: /taskmaster:init your-prd.md
```

## Next Steps

After installation:
1. Run `/taskmaster:status` to verify setup
2. Configure AI providers with `/taskmaster:setup-models`
3. Start using Task Master commands!
"""
```

.gemini/commands/tm/learn.toml
```
description="Learn"
prompt = """
Learn about Task Master capabilities through interactive exploration.

Arguments: $ARGUMENTS

## Interactive Task Master Learning

Based on your input, I'll help you discover capabilities:

### 1. **What are you trying to do?**

If $ARGUMENTS contains:
- "start" / "begin" → Show project initialization workflows
- "manage" / "organize" → Show task management commands
- "automate" / "auto" → Show automation workflows
- "analyze" / "report" → Show analysis tools
- "fix" / "problem" → Show troubleshooting commands
- "fast" / "quick" → Show efficiency shortcuts

### 2. **Intelligent Suggestions**

Based on your project state:

**No tasks yet?**
```
You'll want to start with:
1. /project:task-master:init <prd-file>
   → Creates tasks from requirements

2. /project:task-master:parse-prd <file>
   → Alternative task generation

Try: /project:task-master:init demo-prd.md
```

**Have tasks?**
Let me analyze what you might need...
- Many pending tasks? → Learn sprint planning
- Complex tasks? → Learn task expansion
- Daily work? → Learn workflow automation

### 3. **Command Discovery**

**By Category:**
- 📋 Task Management: list, show, add, update, complete
- 🔄 Workflows: auto-implement, sprint-plan, daily-standup
- 🛠️ Utilities: check-health, complexity-report, sync-memory
- 🔍 Analysis: validate-deps, show dependencies

**By Scenario:**
- "I want to see what to work on" → `/project:task-master:next`
- "I need to break this down" → `/project:task-master:expand <id>`
- "Show me everything" → `/project:task-master:status`
- "Just do it for me" → `/project:workflows:auto-implement`

### 4. **Power User Patterns**

**Command Chaining:**
```
/project:task-master:next
/project:task-master:start <id>
/project:workflows:auto-implement
```

**Smart Filters:**
```
/project:task-master:list pending high
/project:task-master:list blocked
/project:task-master:list 1-5 tree
```

**Automation:**
```
/project:workflows:pipeline init → expand-all → sprint-plan
```

### 5. **Learning Path**

Based on your experience level:

**Beginner Path:**
1. init → Create project
2. status → Understand state
3. next → Find work
4. complete → Finish task

**Intermediate Path:**
1. expand → Break down complex tasks
2. sprint-plan → Organize work
3. complexity-report → Understand difficulty
4. validate-deps → Ensure consistency

**Advanced Path:**
1. pipeline → Chain operations
2. smart-flow → Context-aware automation
3. Custom commands → Extend the system

### 6. **Try This Now**

Based on what you asked about, try:
[Specific command suggestion based on $ARGUMENTS]

Want to learn more about a specific command?
Type: /project:help <command-name>
"""
```

.gemini/commands/tm/list-tasks-by-status.toml
```
description="List Tasks By Status"
prompt = """
List tasks filtered by a specific status.

Arguments: $ARGUMENTS

Parse the status from arguments and list only tasks matching that status.

## Status Options
- `pending` - Not yet started
- `in-progress` - Currently being worked on
- `done` - Completed
- `review` - Awaiting review
- `deferred` - Postponed
- `cancelled` - Cancelled

## Execution

Based on $ARGUMENTS, run:
```bash
task-master list --status=$ARGUMENTS
```

## Enhanced Display

For the filtered results:
- Group by priority within the status
- Show time in current status
- Highlight tasks approaching deadlines
- Display blockers and dependencies
- Suggest next actions for each status group

## Intelligent Insights

Based on the status filter:
- **Pending**: Show recommended start order
- **In-Progress**: Display idle time warnings
- **Done**: Show newly unblocked tasks
- **Review**: Indicate review duration
- **Deferred**: Show reactivation criteria
- **Cancelled**: Display impact analysis
"""
```

.gemini/commands/tm/list-tasks-with-subtasks.toml
```
description="List Tasks With Subtasks"
prompt = """
List all tasks including their subtasks in a hierarchical view.

This command shows all tasks with their nested subtasks, providing a complete project overview.

## Execution

Run the Task Master list command with subtasks flag:
```bash
task-master list --with-subtasks
```

## Enhanced Display

I'll organize the output to show:
- Parent tasks with clear indicators
- Nested subtasks with proper indentation
- Status badges for quick scanning
- Dependencies and blockers highlighted
- Progress indicators for tasks with subtasks

## Smart Filtering

Based on the task hierarchy:
- Show completion percentage for parent tasks
- Highlight blocked subtask chains
- Group by functional areas
- Indicate critical path items

This gives you a complete tree view of your project structure.
"""
```

.gemini/commands/tm/list-tasks.toml
```
description="List Tasks"
prompt = """
List tasks with intelligent argument parsing.

Parse arguments to determine filters and display options:
- Status: pending, in-progress, done, review, deferred, cancelled
- Priority: high, medium, low (or priority:high)
- Special: subtasks, tree, dependencies, blocked
- IDs: Direct numbers (e.g., "1,3,5" or "1-5")
- Complex: "pending high" = pending AND high priority

Arguments: $ARGUMENTS

Let me parse your request intelligently:

1. **Detect Filter Intent**
   - If arguments contain status keywords → filter by status
   - If arguments contain priority → filter by priority
   - If arguments contain "subtasks" → include subtasks
   - If arguments contain "tree" → hierarchical view
   - If arguments contain numbers → show specific tasks
   - If arguments contain "blocked" → show blocked tasks only

2. **Smart Combinations**
   Examples of what I understand:
   - "pending high" → pending tasks with high priority
   - "done today" → tasks completed today
   - "blocked" → tasks with unmet dependencies
   - "1-5" → tasks 1 through 5
   - "subtasks tree" → hierarchical view with subtasks

3. **Execute Appropriate Query**
   Based on parsed intent, run the most specific task-master command

4. **Enhanced Display**
   - Group by relevant criteria
   - Show most important information first
   - Use visual indicators for quick scanning
   - Include relevant metrics

5. **Intelligent Suggestions**
   Based on what you're viewing, suggest next actions:
   - Many pending? → Suggest priority order
   - Many blocked? → Show dependency resolution
   - Looking at specific tasks? → Show related tasks
"""
```

.gemini/commands/tm/next-task.toml
```
description="Next Task"
prompt = """
Intelligently determine and prepare the next action based on comprehensive context.

This enhanced version of 'next' considers:
- Current task states
- Recent activity
- Time constraints
- Dependencies
- Your working patterns

Arguments: $ARGUMENTS

## Intelligent Next Action

### 1. **Context Gathering**
Let me analyze the current situation:
- Active tasks (in-progress)
- Recently completed tasks
- Blocked tasks
- Time since last activity
- Arguments provided: $ARGUMENTS

### 2. **Smart Decision Tree**

**If you have an in-progress task:**
- Has it been idle > 2 hours? → Suggest resuming or switching
- Near completion? → Show remaining steps
- Blocked? → Find alternative task

**If no in-progress tasks:**
- Unblocked high-priority tasks? → Start highest
- Complex tasks need breakdown? → Suggest expansion
- All tasks blocked? → Show dependency resolution

**Special arguments handling:**
- "quick" → Find task < 2 hours
- "easy" → Find low complexity task
- "important" → Find high priority regardless of complexity
- "continue" → Resume last worked task

### 3. **Preparation Workflow**

Based on selected task:
1. Show full context and history
2. Set up development environment
3. Run relevant tests
4. Open related files
5. Show similar completed tasks
6. Estimate completion time

### 4. **Alternative Suggestions**

Always provide options:
- Primary recommendation
- Quick alternative (< 1 hour)
- Strategic option (unblocks most tasks)
- Learning option (new technology/skill)

### 5. **Workflow Integration**

Seamlessly connect to:
- `/project:task-master:start [selected]`
- `/project:workflows:auto-implement`
- `/project:task-master:expand` (if complex)
- `/project:utils:complexity-report` (if unsure)

The goal: Zero friction from decision to implementation.
"""
```

.gemini/commands/tm/parse-prd-with-research.toml
```
description="Parse PRD With Research"
prompt = """
Parse PRD with enhanced research mode for better task generation.

Arguments: $ARGUMENTS (PRD file path)

## Research-Enhanced Parsing

Uses the research AI provider (typically Perplexity) for more comprehensive task generation with current best practices.

## Execution

```bash
task-master parse-prd --input=$ARGUMENTS --research
```

## Research Benefits

1. **Current Best Practices**
   - Latest framework patterns
   - Security considerations
   - Performance optimizations
   - Accessibility requirements

2. **Technical Deep Dive**
   - Implementation approaches
   - Library recommendations
   - Architecture patterns
   - Testing strategies

3. **Comprehensive Coverage**
   - Edge cases consideration
   - Error handling tasks
   - Monitoring setup
   - Deployment tasks

## Enhanced Output

Research mode typically:
- Generates more detailed tasks
- Includes industry standards
- Adds compliance considerations
- Suggests modern tooling

## When to Use

- New technology domains
- Complex requirements
- Regulatory compliance needed
- Best practices crucial
"""
```

.gemini/commands/tm/parse-prd.toml
```
description="Parse PRD"
prompt = """
Parse a PRD document to generate tasks.

Arguments: $ARGUMENTS (PRD file path)

## Intelligent PRD Parsing

Analyzes your requirements document and generates a complete task breakdown.

## Execution

```bash
task-master parse-prd --input=$ARGUMENTS
```

## Parsing Process

1. **Document Analysis**
   - Extract key requirements
   - Identify technical components
   - Detect dependencies
   - Estimate complexity

2. **Task Generation**
   - Create 10-15 tasks by default
   - Include implementation tasks
   - Add testing tasks
   - Include documentation tasks
   - Set logical dependencies

3. **Smart Enhancements**
   - Group related functionality
   - Set appropriate priorities
   - Add acceptance criteria
   - Include test strategies

## Options

Parse arguments for modifiers:
- Number after filename → `--num-tasks`
- `research` → Use research mode
- `comprehensive` → Generate more tasks

## Post-Generation

After parsing:
1. Display task summary
2. Show dependency graph
3. Suggest task expansion for complex items
4. Recommend sprint planning
"""
```

.gemini/commands/tm/project-status.toml
```
description="Project Status"
prompt = """
Enhanced status command with comprehensive project insights.

Arguments: $ARGUMENTS

## Intelligent Status Overview

### 1. **Executive Summary**
Quick dashboard view:
- 🏃 Active work (in-progress tasks)
- 📊 Progress metrics (% complete, velocity)
- 🚧 Blockers and risks
- ⏱️ Time analysis (estimated vs actual)
- 🎯 Sprint/milestone progress

### 2. **Contextual Analysis**

Based on $ARGUMENTS, focus on:
- "sprint" → Current sprint progress and burndown
- "blocked" → Dependency chains and resolution paths
- "team" → Task distribution and workload
- "timeline" → Schedule adherence and projections
- "risk" → High complexity or overdue items

### 3. **Smart Insights**

**Workflow Health:**
- Idle tasks (in-progress > 24h without updates)
- Bottlenecks (multiple tasks waiting on same dependency)
- Quick wins (low complexity, high impact)

**Predictive Analytics:**
- Completion projections based on velocity
- Risk of missing deadlines
- Recommended task order for optimal flow

### 4. **Visual Intelligence**

Dynamic visualization based on data:
```
Sprint Progress: ████████░░ 80% (16/20 tasks)
Velocity Trend: ↗️ +15% this week
Blocked Tasks:  🔴 3 critical path items

Priority Distribution:
High:   ████████ 8 tasks (2 blocked)
Medium: ████░░░░ 4 tasks
Low:    ██░░░░░░ 2 tasks
```

### 5. **Actionable Recommendations**

Based on analysis:
1. **Immediate actions** (unblock critical path)
2. **Today's focus** (optimal task sequence)
3. **Process improvements** (recurring patterns)
4. **Resource needs** (skills, time, dependencies)

### 6. **Historical Context**

Compare to previous periods:
- Velocity changes
- Pattern recognition
- Improvement areas
- Success patterns to repeat
"""
```

.gemini/commands/tm/quick-install-taskmaster.toml
```
description="Quick Install TaskMaster"
prompt = """
Quick install Task Master globally if not already installed.

Execute this streamlined installation:

```bash
# Check and install in one command
task-master --version 2>/dev/null || npm install -g task-master-ai

# Verify installation
task-master --version

# Quick setup check
task-master models --status || echo "Note: You'll need to set up an AI provider API key"
```

If you see "command not found" after installation, you may need to:
1. Restart your terminal
2. Or add npm global bin to PATH: `export PATH=$(npm bin -g):$PATH`

Once installed, you can use all the Task Master commands!

Quick test: Run `/taskmaster:help` to see all available commands.
"""
```

.gemini/commands/tm/remove-all-subtasks.toml
```
description="Remove All Subtasks"
prompt = """
Clear all subtasks from all tasks globally.

## Global Subtask Clearing

Remove all subtasks across the entire project. Use with extreme caution.

## Execution

```bash
task-master clear-subtasks --all
```

## Pre-Clear Analysis

1. **Project-Wide Summary**
   ```
   Global Subtask Summary
   ━━━━━━━━━━━━━━━━━━━━
   Total parent tasks: 12
   Total subtasks: 47
   - Completed: 15
   - In-progress: 8
   - Pending: 24

   Work at risk: ~120 hours
   ```

2. **Critical Warnings**
   - In-progress subtasks that will lose work
   - Completed subtasks with valuable history
   - Complex dependency chains
   - Integration test results

## Double Confirmation

```
⚠️  DESTRUCTIVE OPERATION WARNING ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This will remove ALL 47 subtasks from your project
Including 8 in-progress and 15 completed subtasks

This action CANNOT be undone

Type 'CLEAR ALL SUBTASKS' to confirm:
```

## Smart Safeguards

- Require explicit confirmation phrase
- Create automatic backup
- Log all removed data
- Option to export first

## Use Cases

Valid reasons for global clear:
- Project restructuring
- Major pivot in approach
- Starting fresh breakdown
- Switching to different task organization

## Process

1. Full project analysis
2. Create backup file
3. Show detailed impact
4. Require confirmation
5. Execute removal
6. Generate summary report

## Alternative Suggestions

Before clearing all:
- Export subtasks to file
- Clear only pending subtasks
- Clear by task category
- Archive instead of delete

## Post-Clear Report

```
Global Subtask Clear Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Removed: 47 subtasks from 12 tasks
Backup saved: .taskmaster/backup/subtasks-20240115.json
Parent tasks updated: 12
Time estimates adjusted: Yes

Next steps:
- Review updated task list
- Re-expand complex tasks as needed
- Check project timeline
```
"""
```

.gemini/commands/tm/remove-dependency.toml
```
description="Remove Dependency"
prompt = """
Remove a dependency between tasks.

Arguments: $ARGUMENTS

Parse the task IDs to remove dependency relationship.

## Removing Dependencies

Removes a dependency relationship, potentially unblocking tasks.

## Argument Parsing

Parse natural language or IDs:
- "remove dependency between 5 and 3"
- "5 no longer needs 3"
- "unblock 5 from 3"
- "5 3" → remove dependency of 5 on 3

## Execution

```bash
task-master remove-dependency --id=<task-id> --depends-on=<dependency-id>
```

## Pre-Removal Checks

1. **Verify dependency exists**
2. **Check impact on task flow**
3. **Warn if it breaks logical sequence**
4. **Show what will be unblocked**

## Smart Analysis

Before removing:
- Show why dependency might have existed
- Check if removal makes tasks executable
- Verify no critical path disruption
- Suggest alternative dependencies

## Post-Removal

After removing:
1. Show updated task status
2. List newly unblocked tasks
3. Update project timeline
4. Suggest next actions

## Safety Features

- Confirm if removing critical dependency
- Show tasks that become immediately actionable
- Warn about potential issues
- Keep removal history

## Example

```
/taskmaster:remove-dependency 5 from 3
→ Removed: Task #5 no longer depends on #3
→ Task #5 is now UNBLOCKED and ready to start
→ Warning: Consider if #5 still needs #2 completed first
```
"""
```

.gemini/commands/tm/remove-subtask.toml
```
description="Remove Subtask"
prompt = """
Remove a subtask from its parent task.

Arguments: $ARGUMENTS

Parse subtask ID to remove, with option to convert to standalone task.

## Removing Subtasks

Remove a subtask and optionally convert it back to a standalone task.

## Argument Parsing

- "remove subtask 5.1"
- "delete 5.1"
- "convert 5.1 to task" → remove and convert
- "5.1 standalone" → convert to standalone

## Execution Options

### 1. Delete Subtask
```bash
task-master remove-subtask --id=<parentId.subtaskId>
```

### 2. Convert to Standalone
```bash
task-master remove-subtask --id=<parentId.subtaskId> --convert
```

## Pre-Removal Checks

1. **Validate Subtask**
   - Verify subtask exists
   - Check completion status
   - Review dependencies

2. **Impact Analysis**
   - Other subtasks that depend on it
   - Parent task implications
   - Data that will be lost

## Removal Process

### For Deletion:
1. Confirm if subtask has work done
2. Update parent task estimates
3. Remove subtask and its data
4. Clean up dependencies

### For Conversion:
1. Assign new standalone task ID
2. Preserve all task data
3. Update dependency references
4. Maintain task history

## Smart Features

- Warn if subtask is in-progress
- Show impact on parent task
- Preserve important data
- Update related estimates

## Example Flows

```
/taskmaster:remove-subtask 5.1
→ Warning: Subtask #5.1 is in-progress
→ This will delete all subtask data
→ Parent task #5 will be updated
Confirm deletion? (y/n)

/taskmaster:remove-subtask 5.1 convert
→ Converting subtask #5.1 to standalone task #89
→ Preserved: All task data and history
→ Updated: 2 dependency references
→ New task #89 is now independent
```

## Post-Removal

- Update parent task status
- Recalculate estimates
- Show updated hierarchy
- Suggest next actions
"""
```

.gemini/commands/tm/remove-subtasks.toml
```
description="Remove Subtasks"
prompt = """
Clear all subtasks from a specific task.

Arguments: $ARGUMENTS (task ID)

Remove all subtasks from a parent task at once.

## Clearing Subtasks

Bulk removal of all subtasks from a parent task.

## Execution

```bash
task-master remove-subtasks --id=$ARGUMENTS
```

## Pre-Clear Analysis

1. **Subtask Summary**
   - Number of subtasks
   - Completion status of each
   - Work already done
   - Dependencies affected

2. **Impact Assessment**
   - Data that will be lost
   - Dependencies to be removed
   - Effect on project timeline
   - Parent task implications

## Confirmation Required

```
Remove Subtasks Confirmation
━━━━━━━━━━━━━━━━━━━━━━━━━
Parent Task: #5 "Implement user authentication"
Subtasks to remove: 4
- #5.1 "Setup auth framework" (done)
- #5.2 "Create login form" (in-progress)
- #5.3 "Add validation" (pending)
- #5.4 "Write tests" (pending)

⚠️  This will permanently delete all subtask data
Continue? (y/n)
```

## Smart Features

- Option to convert to standalone tasks
- Backup task data before clearing
- Preserve completed work history
- Update parent task appropriately

## Process

1. List all subtasks for confirmation
2. Check for in-progress work
3. Remove all subtasks
4. Update parent task
5. Clean up dependencies

## Alternative Options

Suggest alternatives:
- Convert important subtasks to tasks
- Keep completed subtasks
- Archive instead of delete
- Export subtask data first

## Post-Clear

- Show updated parent task
- Recalculate time estimates
- Update task complexity
- Suggest next steps

## Example

```
/taskmaster:remove-subtasks 5
→ Found 4 subtasks to remove
→ Warning: Subtask #5.2 is in-progress
→ Cleared all subtasks from task #5
→ Updated parent task estimates
→ Suggestion: Consider re-expanding with better breakdown
```
"""
```

.gemini/commands/tm/remove-task.toml
```
description="Remove Task"
prompt = """
Remove a task permanently from the project.

Arguments: $ARGUMENTS (task ID)

Delete a task and handle all its relationships properly.

## Task Removal

Permanently removes a task while maintaining project integrity.

## Argument Parsing

- "remove task 5"
- "delete 5"
- "5" → remove task 5
- Can include "-y" for auto-confirm

## Execution

```bash
task-master remove-task --id=<id> [-y]
```

## Pre-Removal Analysis

1. **Task Details**
   - Current status
   - Work completed
   - Time invested
   - Associated data

2. **Relationship Check**
   - Tasks that depend on this
   - Dependencies this task has
   - Subtasks that will be removed
   - Blocking implications

3. **Impact Assessment**
   ```
   Task Removal Impact
   ━━━━━━━━━━━━━━━━━━
   Task: #5 "Implement authentication" (in-progress)
   Status: 60% complete (~8 hours work)

   Will affect:
   - 3 tasks depend on this (will be blocked)
   - Has 4 subtasks (will be deleted)
   - Part of critical path

   ⚠️  This action cannot be undone
   ```

## Smart Warnings

- Warn if task is in-progress
- Show dependent tasks that will be blocked
- Highlight if part of critical path
- Note any completed work being lost

## Removal Process

1. Show comprehensive impact
2. Require confirmation (unless -y)
3. Update dependent task references
4. Remove task and subtasks
5. Clean up orphaned dependencies
6. Log removal with timestamp

## Alternative Actions

Suggest before deletion:
- Mark as cancelled instead
- Convert to documentation
- Archive task data
- Transfer work to another task

## Post-Removal

- List affected tasks
- Show broken dependencies
- Update project statistics
- Suggest dependency fixes
- Recalculate timeline

## Example Flows

```
/taskmaster:remove-task 5
→ Task #5 is in-progress with 8 hours logged
→ 3 other tasks depend on this
→ Suggestion: Mark as cancelled instead?
Remove anyway? (y/n)

/taskmaster:remove-task 5 -y
→ Removed: Task #5 and 4 subtasks
→ Updated: 3 task dependencies
→ Warning: Tasks #7, #8, #9 now have missing dependency
→ Run /taskmaster:fix-dependencies to resolve
```

## Safety Features

- Confirmation required
- Impact preview
- Removal logging
- Suggest alternatives
- No cascade delete of dependents
"""
```

.gemini/commands/tm/setup-models.toml
```
description="Setup Models"
prompt = """
Run interactive setup to configure AI models.

## Interactive Model Configuration

Guides you through setting up AI providers for Task Master.

## Execution

```bash
task-master models --setup
```

## Setup Process

1. **Environment Check**
   - Detect existing API keys
   - Show current configuration
   - Identify missing providers

2. **Provider Selection**
   - Choose main provider (required)
   - Select research provider (recommended)
   - Configure fallback (optional)

3. **API Key Configuration**
   - Prompt for missing keys
   - Validate key format
   - Test connectivity
   - Save configuration

## Smart Recommendations

Based on your needs:
- **For best results**: Claude + Perplexity
- **Budget conscious**: GPT-3.5 + Perplexity
- **Maximum capability**: GPT-4 + Perplexity + Claude fallback

## Configuration Storage

Keys can be stored in:
1. Environment variables (recommended)
2. `.env` file in project
3. Global `.taskmaster/config`

## Post-Setup

After configuration:
- Test each provider
- Show usage examples
- Suggest next steps
- Verify parse-prd works
"""
```

.gemini/commands/tm/show-task.toml
```
description="Show Task"
prompt = """
Show detailed task information with rich context and insights.

Arguments: $ARGUMENTS

## Enhanced Task Display

Parse arguments to determine what to show and how.

### 1. **Smart Task Selection**

Based on $ARGUMENTS:
- Number → Show specific task with full context
- "current" → Show active in-progress task(s)
- "next" → Show recommended next task
- "blocked" → Show all blocked tasks with reasons
- "critical" → Show critical path tasks
- Multiple IDs → Comparative view

### 2. **Contextual Information**

For each task, intelligently include:

**Core Details**
- Full task information (id, title, description, details)
- Current status with history
- Test strategy and acceptance criteria
- Priority and complexity analysis

**Relationships**
- Dependencies (what it needs)
- Dependents (what needs it)
- Parent/subtask hierarchy
- Related tasks (similar work)

**Time Intelligence**
- Created/updated timestamps
- Time in current status
- Estimated vs actual time
- Historical completion patterns

### 3. **Visual Enhancements**

```
📋 Task #45: Implement User Authentication
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: 🟡 in-progress (2 hours)
Priority: 🔴 High | Complexity: 73/100

Dependencies: ✅ #41, ✅ #42, ⏳ #43 (blocked)
Blocks: #46, #47, #52

Progress: ████████░░ 80% complete

Recent Activity:
- 2h ago: Status changed to in-progress
- 4h ago: Dependency #42 completed
- Yesterday: Task expanded with 3 subtasks
```

### 4. **Intelligent Insights**

Based on task analysis:
- **Risk Assessment**: Complexity vs time remaining
- **Bottleneck Analysis**: Is this blocking critical work?
- **Recommendation**: Suggested approach or concerns
- **Similar Tasks**: How others completed similar work

### 5. **Action Suggestions**

Context-aware next steps:
- If blocked → Show how to unblock
- If complex → Suggest expansion
- If in-progress → Show completion checklist
- If done → Show dependent tasks ready to start

### 6. **Multi-Task View**

When showing multiple tasks:
- Common dependencies
- Optimal completion order
- Parallel work opportunities
- Combined complexity analysis
"""
```

.gemini/commands/tm/smart-workflow.toml
```
description="Smart Workflow"
prompt = """
Execute an intelligent workflow based on current project state and recent commands.

This command analyzes:
1. Recent commands you've run
2. Current project state
3. Time of day / day of week
4. Your working patterns

Arguments: $ARGUMENTS

## Intelligent Workflow Selection

Based on context, I'll determine the best workflow:

### Context Analysis
- Previous command executed
- Current task states
- Unfinished work from last session
- Your typical patterns

### Smart Execution

If last command was:
- `status` → Likely starting work → Run daily standup
- `complete` → Task finished → Find next task
- `list pending` → Planning → Suggest sprint planning
- `expand` → Breaking down work → Show complexity analysis
- `init` → New project → Show onboarding workflow

If no recent commands:
- Morning? → Daily standup workflow
- Many pending tasks? → Sprint planning
- Tasks blocked? → Dependency resolution
- Friday? → Weekly review

### Workflow Composition

I'll chain appropriate commands:
1. Analyze current state
2. Execute primary workflow
3. Suggest follow-up actions
4. Prepare environment for coding

### Learning Mode

This command learns from your patterns:
- Track command sequences
- Note time preferences
- Remember common workflows
- Adapt to your style

Example flows detected:
- Morning: standup → next → start
- After lunch: status → continue task
- End of day: complete → commit → status
"""
```

.gemini/commands/tm/sync-readme.toml
```
description="Sync README"
prompt = """
Export tasks to README.md with professional formatting.

Arguments: $ARGUMENTS

Generate a well-formatted README with current task information.

## README Synchronization

Creates or updates README.md with beautifully formatted task information.

## Argument Parsing

Optional filters:
- "pending" → Only pending tasks
- "with-subtasks" → Include subtask details
- "by-priority" → Group by priority
- "sprint" → Current sprint only

## Execution

```bash
task-master sync-readme [--with-subtasks] [--status=<status>]
```

## README Generation

### 1. **Project Header**
```markdown
# Project Name

## 📋 Task Progress

Last Updated: 2024-01-15 10:30 AM

### Summary
- Total Tasks: 45
- Completed: 15 (33%)
- In Progress: 5 (11%)
- Pending: 25 (56%)
```

### 2. **Task Sections**
Organized by status or priority:
- Progress indicators
- Task descriptions
- Dependencies noted
- Time estimates

### 3. **Visual Elements**
- Progress bars
- Status badges
- Priority indicators
- Completion checkmarks

## Smart Features

1. **Intelligent Grouping**
   - By feature area
   - By sprint/milestone
   - By assigned developer
   - By priority

2. **Progress Tracking**
   - Overall completion
   - Sprint velocity
   - Burndown indication
   - Time tracking

3. **Formatting Options**
   - GitHub-flavored markdown
   - Task checkboxes
   - Collapsible sections
   - Table format available

## Example Output

```markdown
## 🚀 Current Sprint

### In Progress
- [ ] 🔄 #5 **Implement user authentication** (60% complete)
  - Dependencies: API design (#3 ✅)
  - Subtasks: 4 (2 completed)
  - Est: 8h / Spent: 5h

### Pending (High Priority)
- [ ] ⚡ #8 **Create dashboard UI**
  - Blocked by: #5
  - Complexity: High
  - Est: 12h
```

## Customization

Based on arguments:
- Include/exclude sections
- Detail level control
- Custom grouping
- Filter by criteria

## Post-Sync

After generation:
1. Show diff preview
2. Backup existing README
3. Write new content
4. Commit reminder
5. Update timestamp

## Integration

Works well with:
- Git workflows
- CI/CD pipelines
- Project documentation
- Team updates
- Client reports
"""
```

.gemini/commands/tm/tm-main.toml
```
description="Task Master Main"
prompt = """
# Task Master Command Reference

Comprehensive command structure for Task Master integration with Claude Code.

## Command Organization

Commands are organized hierarchically to match Task Master's CLI structure while providing enhanced Claude Code integration.

## Project Setup & Configuration

### `/taskmaster:init`
- `init-project` - Initialize new project (handles PRD files intelligently)
- `init-project-quick` - Quick setup with auto-confirmation (-y flag)

### `/taskmaster:models`
- `view-models` - View current AI model configuration
- `setup-models` - Interactive model configuration
- `set-main` - Set primary generation model
- `set-research` - Set research model
- `set-fallback` - Set fallback model

## Task Generation

### `/taskmaster:parse-prd`
- `parse-prd` - Generate tasks from PRD document
- `parse-prd-with-research` - Enhanced parsing with research mode

### `/taskmaster:generate`
- `generate-tasks` - Create individual task files from tasks.json

## Task Management

### `/taskmaster:list`
- `list-tasks` - Smart listing with natural language filters
- `list-tasks-with-subtasks` - Include subtasks in hierarchical view
- `list-tasks-by-status` - Filter by specific status

### `/taskmaster:set-status`
- `to-pending` - Reset task to pending
- `to-in-progress` - Start working on task
- `to-done` - Mark task complete
- `to-review` - Submit for review
- `to-deferred` - Defer task
- `to-cancelled` - Cancel task

### `/taskmaster:sync-readme`
- `sync-readme` - Export tasks to README.md with formatting

### `/taskmaster:update`
- `update-task` - Update tasks with natural language
- `update-tasks-from-id` - Update multiple tasks from a starting point
- `update-single-task` - Update specific task

### `/taskmaster:add-task`
- `add-task` - Add new task with AI assistance

### `/taskmaster:remove-task`
- `remove-task` - Remove task with confirmation

## Subtask Management

### `/taskmaster:add-subtask`
- `add-subtask` - Add new subtask to parent
- `convert-task-to-subtask` - Convert existing task to subtask

### `/taskmaster:remove-subtask`
- `remove-subtask` - Remove subtask (with optional conversion)

### `/taskmaster:clear-subtasks`
- `clear-subtasks` - Clear subtasks from specific task
- `clear-all-subtasks` - Clear all subtasks globally

## Task Analysis & Breakdown

### `/taskmaster:analyze-complexity`
- `analyze-complexity` - Analyze and generate expansion recommendations

### `/taskmaster:complexity-report`
- `complexity-report` - Display complexity analysis report

### `/taskmaster:expand`
- `expand-task` - Break down specific task
- `expand-all-tasks` - Expand all eligible tasks
- `with-research` - Enhanced expansion

## Task Navigation

### `/taskmaster:next`
- `next-task` - Intelligent next task recommendation

### `/taskmaster:show`
- `show-task` - Display detailed task information

### `/taskmaster:status`
- `project-status` - Comprehensive project dashboard

## Dependency Management

### `/taskmaster:add-dependency`
- `add-dependency` - Add task dependency

### `/taskmaster:remove-dependency`
- `remove-dependency` - Remove task dependency

### `/taskmaster:validate-dependencies`
- `validate-dependencies` - Check for dependency issues

### `/taskmaster:fix-dependencies`
- `fix-dependencies` - Automatically fix dependency problems

## Workflows & Automation

### `/taskmaster:workflows`
- `smart-workflow` - Context-aware intelligent workflow execution
- `command-pipeline` - Chain multiple commands together
- `auto-implement-tasks` - Advanced auto-implementation with code generation

## Utilities

### `/taskmaster:utils`
- `analyze-project` - Deep project analysis and insights

### `/taskmaster:setup`
- `install-taskmaster` - Comprehensive installation guide
- `quick-install-taskmaster` - One-line global installation

## Usage Patterns

### Natural Language
Most commands accept natural language arguments:
```
/taskmaster:add-task create user authentication system
/taskmaster:update mark all API tasks as high priority
/taskmaster:list show blocked tasks
```

### ID-Based Commands
Commands requiring IDs intelligently parse from $ARGUMENTS:
```
/taskmaster:show 45
/taskmaster:expand 23
/taskmaster:set-status/to-done 67
```

### Smart Defaults
Commands provide intelligent defaults and suggestions based on context.
"""
```

.gemini/commands/tm/to-cancelled.toml
```
description="To Cancelled"
prompt = """
Cancel a task permanently.

Arguments: $ARGUMENTS (task ID)

## Cancelling a Task

This status indicates a task is no longer needed and won't be completed.

## Valid Reasons for Cancellation

- Requirements changed
- Feature deprecated
- Duplicate of another task
- Strategic pivot
- Technical approach invalidated

## Pre-Cancellation Checks

1. Confirm no critical dependencies
2. Check for partial implementation
3. Verify cancellation rationale
4. Document lessons learned

## Execution

```bash
task-master set-status --id=$ARGUMENTS --status=cancelled
```

## Cancellation Impact

When cancelling:
1. **Dependency Updates**
   - Notify dependent tasks
   - Update project scope
   - Recalculate timelines

2. **Clean-up Actions**
   - Remove related branches
   - Archive any work done
   - Update documentation
   - Close related issues

3. **Learning Capture**
   - Document why cancelled
   - Note what was learned
   - Update estimation models
   - Prevent future duplicates

## Historical Preservation

- Keep for reference
- Tag with cancellation reason
- Link to replacement if any
- Maintain audit trail
"""
```

.gemini/commands/tm/to-deferred.toml
```
description="To Deferred"
prompt = """
Defer a task for later consideration.

Arguments: $ARGUMENTS (task ID)

## Deferring a Task

This status indicates a task is valid but not currently actionable or prioritized.

## Valid Reasons for Deferral

- Waiting for external dependencies
- Reprioritized for future sprint
- Blocked by technical limitations
- Resource constraints
- Strategic timing considerations

## Execution

```bash
task-master set-status --id=$ARGUMENTS --status=deferred
```

## Deferral Management

When deferring:
1. **Document Reason**
   - Capture why it's being deferred
   - Set reactivation criteria
   - Note any partial work completed

2. **Impact Analysis**
   - Check dependent tasks
   - Update project timeline
   - Notify affected stakeholders

3. **Future Planning**
   - Set review reminders
   - Tag for specific milestone
   - Preserve context for reactivation
   - Link to blocking issues

## Smart Tracking

- Monitor deferral duration
- Alert when criteria met
- Prevent scope creep
- Regular review cycles
"""
```

.gemini/commands/tm/to-done.toml
```
description="To Done"
prompt = """
Mark a task as completed.

Arguments: $ARGUMENTS (task ID)

## Completing a Task

This command validates task completion and updates project state intelligently.

## Pre-Completion Checks

1. Verify test strategy was followed
2. Check if all subtasks are complete
3. Validate acceptance criteria met
4. Ensure code is committed

## Execution

```bash
task-master set-status --id=$ARGUMENTS --status=done
```

## Post-Completion Actions

1. **Update Dependencies**
   - Identify newly unblocked tasks
   - Update sprint progress
   - Recalculate project timeline

2. **Documentation**
   - Generate completion summary
   - Update CLAUDE.md with learnings
   - Log implementation approach

3. **Next Steps**
   - Show newly available tasks
   - Suggest logical next task
   - Update velocity metrics

## Celebration & Learning

- Show impact of completion
- Display unblocked work
- Recognize achievement
- Capture lessons learned
"""
```

.gemini/commands/tm/to-in-progress.toml
```
description="To In Progress"
prompt = """
Start working on a task by setting its status to in-progress.

Arguments: $ARGUMENTS (task ID)

## Starting Work on Task

This command does more than just change status - it prepares your environment for productive work.

## Pre-Start Checks

1. Verify dependencies are met
2. Check if another task is already in-progress
3. Ensure task details are complete
4. Validate test strategy exists

## Execution

```bash
task-master set-status --id=$ARGUMENTS --status=in-progress
```

## Environment Setup

After setting to in-progress:
1. Create/checkout appropriate git branch
2. Open relevant documentation
3. Set up test watchers if applicable
4. Display task details and acceptance criteria
5. Show similar completed tasks for reference

## Smart Suggestions

- Estimated completion time based on complexity
- Related files from similar tasks
- Potential blockers to watch for
- Recommended first steps
"""
```

.gemini/commands/tm/to-pending.toml
```
description="To Pending"
prompt = """
Set a task's status to pending.

Arguments: $ARGUMENTS (task ID)

## Setting Task to Pending

This moves a task back to the pending state, useful for:
- Resetting erroneously started tasks
- Deferring work that was prematurely begun
- Reorganizing sprint priorities

## Execution

```bash
task-master set-status --id=$ARGUMENTS --status=pending
```

## Validation

Before setting to pending:
- Warn if task is currently in-progress
- Check if this will block other tasks
- Suggest documenting why it's being reset
- Preserve any work already done

## Smart Actions

After setting to pending:
- Update sprint planning if needed
- Notify about freed resources
- Suggest priority reassessment
- Log the status change with context
"""
```

.gemini/commands/tm/to-review.toml
```
description="To Review"
prompt = """
Set a task's status to review.

Arguments: $ARGUMENTS (task ID)

## Marking Task for Review

This status indicates work is complete but needs verification before final approval.

## When to Use Review Status

- Code complete but needs peer review
- Implementation done but needs testing
- Documentation written but needs proofreading
- Design complete but needs stakeholder approval

## Execution

```bash
task-master set-status --id=$ARGUMENTS --status=review
```

## Review Preparation

When setting to review:
1. **Generate Review Checklist**
   - Link to PR/MR if applicable
   - Highlight key changes
   - Note areas needing attention
   - Include test results

2. **Documentation**
   - Update task with review notes
   - Link relevant artifacts
   - Specify reviewers if known

3. **Smart Actions**
   - Create review reminders
   - Track review duration
   - Suggest reviewers based on expertise
   - Prepare rollback plan if needed
"""
```

.gemini/commands/tm/update-single-task.toml
```
description="Update Single Task"
prompt = """
Update a single specific task with new information.

Arguments: $ARGUMENTS

Parse task ID and update details.

## Single Task Update

Precisely update one task with AI assistance to maintain consistency.

## Argument Parsing

Natural language updates:
- "5: add caching requirement"
- "update 5 to include error handling"
- "task 5 needs rate limiting"
- "5 change priority to high"

## Execution

```bash
task-master update-task --id=<id> --prompt="<context>"
```

## Update Types

### 1. **Content Updates**
- Enhance description
- Add requirements
- Clarify details
- Update acceptance criteria

### 2. **Metadata Updates**
- Change priority
- Adjust time estimates
- Update complexity
- Modify dependencies

### 3. **Strategic Updates**
- Revise approach
- Change test strategy
- Update implementation notes
- Adjust subtask needs

## AI-Powered Updates

The AI:
1. **Understands Context**
   - Reads current task state
   - Identifies update intent
   - Maintains consistency
   - Preserves important info

2. **Applies Changes**
   - Updates relevant fields
   - Keeps style consistent
   - Adds without removing
   - Enhances clarity

3. **Validates Results**
   - Checks coherence
   - Verifies completeness
   - Maintains relationships
   - Suggests related updates

## Example Updates

```
/taskmaster:update/single 5: add rate limiting
→ Updating Task #5: "Implement API endpoints"

Current: Basic CRUD endpoints
Adding: Rate limiting requirements

Updated sections:
✓ Description: Added rate limiting mention
✓ Details: Added specific limits (100/min)
✓ Test Strategy: Added rate limit tests
✓ Complexity: Increased from 5 to 6
✓ Time Estimate: Increased by 2 hours

Suggestion: Also update task #6 (API Gateway) for consistency?
```

## Smart Features

1. **Incremental Updates**
   - Adds without overwriting
   - Preserves work history
   - Tracks what changed
   - Shows diff view

2. **Consistency Checks**
   - Related task alignment
   - Subtask compatibility
   - Dependency validity
   - Timeline impact

3. **Update History**
   - Timestamp changes
   - Track who/what updated
   - Reason for update
   - Previous versions

## Field-Specific Updates

Quick syntax for specific fields:
- "5 priority:high" → Update priority only
- "5 add-time:4h" → Add to time estimate
- "5 status:review" → Change status
- "5 depends:3,4" → Add dependencies

## Post-Update

- Show updated task
- Highlight changes
- Check related tasks
- Update suggestions
- Timeline adjustments
"""
```

.gemini/commands/tm/update-task.toml
```
description="Update Task"
prompt = """
Update tasks with intelligent field detection and bulk operations.

Arguments: $ARGUMENTS

## Intelligent Task Updates

Parse arguments to determine update intent and execute smartly.

### 1. **Natural Language Processing**

Understand update requests like:
- "mark 23 as done" → Update status to done
- "increase priority of 45" → Set priority to high
- "add dependency on 12 to task 34" → Add dependency
- "tasks 20-25 need review" → Bulk status update
- "all API tasks high priority" → Pattern-based update

### 2. **Smart Field Detection**

Automatically detect what to update:
- Status keywords: done, complete, start, pause, review
- Priority changes: urgent, high, low, deprioritize
- Dependency updates: depends on, blocks, after
- Assignment: assign to, owner, responsible
- Time: estimate, spent, deadline

### 3. **Bulk Operations**

Support for multiple task updates:
```
Examples:
- "complete tasks 12, 15, 18"
- "all pending auth tasks to in-progress"
- "increase priority for tasks blocking 45"
- "defer all documentation tasks"
```

### 4. **Contextual Validation**

Before updating, check:
- Status transitions are valid
- Dependencies don't create cycles
- Priority changes make sense
- Bulk updates won't break project flow

Show preview:
```
Update Preview:
─────────────────
Tasks to update: #23, #24, #25
Change: status → in-progress
Impact: Will unblock tasks #30, #31
Warning: Task #24 has unmet dependencies
```

### 5. **Smart Suggestions**

Based on update:
- Completing task? → Show newly unblocked tasks
- Changing priority? → Show impact on sprint
- Adding dependency? → Check for conflicts
- Bulk update? → Show summary of changes

### 6. **Workflow Integration**

After updates:
- Auto-update dependent task states
- Trigger status recalculation
- Update sprint/milestone progress
- Log changes with context

Result: Flexible, intelligent task updates with safety checks.
"""
```

.gemini/commands/tm/update-tasks-from-id.toml
```
description="Update Tasks From ID"
prompt = """
Update multiple tasks starting from a specific ID.

Arguments: $ARGUMENTS

Parse starting task ID and update context.

## Bulk Task Updates

Update multiple related tasks based on new requirements or context changes.

## Argument Parsing

- "from 5: add security requirements"
- "5 onwards: update API endpoints"
- "starting at 5: change to use new framework"

## Execution

```bash
task-master update --from=<id> --prompt="<context>"
```

## Update Process

### 1. **Task Selection**
Starting from specified ID:
- Include the task itself
- Include all dependent tasks
- Include related subtasks
- Smart boundary detection

### 2. **Context Application**
AI analyzes the update context and:
- Identifies what needs changing
- Maintains consistency
- Preserves completed work
- Updates related information

### 3. **Intelligent Updates**
- Modify descriptions appropriately
- Update test strategies
- Adjust time estimates
- Revise dependencies if needed

## Smart Features

1. **Scope Detection**
   - Find natural task groupings
   - Identify related features
   - Stop at logical boundaries
   - Avoid over-updating

2. **Consistency Maintenance**
   - Keep naming conventions
   - Preserve relationships
   - Update cross-references
   - Maintain task flow

3. **Change Preview**
   ```
   Bulk Update Preview
   ━━━━━━━━━━━━━━━━━━
   Starting from: Task #5
   Tasks to update: 8 tasks + 12 subtasks

   Context: "add security requirements"

   Changes will include:
   - Add security sections to descriptions
   - Update test strategies for security
   - Add security-related subtasks where needed
   - Adjust time estimates (+20% average)

   Continue? (y/n)
   ```

## Example Updates

```
/taskmaster:update-tasks-from-id 5: change database to PostgreSQL
→ Analyzing impact starting from task #5
→ Found 6 related tasks to update
→ Updates will maintain consistency
→ Preview changes? (y/n)

Applied updates:
✓ Task #5: Updated connection logic references
✓ Task #6: Changed migration approach
✓ Task #7: Updated query syntax notes
✓ Task #8: Revised testing strategy
✓ Task #9: Updated deployment steps
✓ Task #12: Changed backup procedures
```

## Safety Features

- Preview all changes
- Selective confirmation
- Rollback capability
- Change logging
- Validation checks

## Post-Update

- Summary of changes
- Consistency verification
- Suggest review tasks
- Update timeline if needed
"""
```

.gemini/commands/tm/validate-dependencies.toml
```
description="Validate Dependencies"
prompt = """
Validate all task dependencies for issues.

## Dependency Validation

Comprehensive check for dependency problems across the entire project.

## Execution

```bash
task-master validate-dependencies
```

## Validation Checks

1. **Circular Dependencies**
   - A depends on B, B depends on A
   - Complex circular chains
   - Self-dependencies

2. **Missing Dependencies**
   - References to non-existent tasks
   - Deleted task references
   - Invalid task IDs

3. **Logical Issues**
   - Completed tasks depending on pending
   - Cancelled tasks in dependency chains
   - Impossible sequences

4. **Complexity Warnings**
   - Over-complex dependency chains
   - Too many dependencies per task
   - Bottleneck tasks

## Smart Analysis

The validation provides:
- Visual dependency graph
- Critical path analysis
- Bottleneck identification
- Suggested optimizations

## Report Format

```
Dependency Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No circular dependencies found
⚠️  2 warnings found:
   - Task #23 has 7 dependencies (consider breaking down)
   - Task #45 blocks 5 other tasks (potential bottleneck)
❌ 1 error found:
   - Task #67 depends on deleted task #66

Critical Path: #1 → #5 → #23 → #45 → #50 (15 days)
```

## Actionable Output

For each issue found:
- Clear description
- Impact assessment
- Suggested fix
- Command to resolve

## Next Steps

After validation:
- Run `/taskmaster:fix-dependencies` to auto-fix
- Manually adjust problematic dependencies
- Rerun to verify fixes
"""
```

.gemini/commands/tm/view-models.toml
```
description="View Models"
prompt = """
View current AI model configuration.

## Model Configuration Display

Shows the currently configured AI providers and models for Task Master.

## Execution

```bash
task-master models
```

## Information Displayed

1. **Main Provider**
   - Model ID and name
   - API key status (configured/missing)
   - Usage: Primary task generation

2. **Research Provider**
   - Model ID and name
   - API key status
   - Usage: Enhanced research mode

3. **Fallback Provider**
   - Model ID and name
   - API key status
   - Usage: Backup when main fails

## Visual Status

```
Task Master AI Model Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Main:     ✅ claude-3-5-sonnet (configured)
Research: ✅ perplexity-sonar (configured)
Fallback: ⚠️  Not configured (optional)

Available Models:
- claude-3-5-sonnet
- gpt-4-turbo
- gpt-3.5-turbo
- perplexity-sonar
```

## Next Actions

Based on configuration:
- If missing API keys → Suggest setup
- If no research model → Explain benefits
- If all configured → Show usage tips
"""
```

</source_code>