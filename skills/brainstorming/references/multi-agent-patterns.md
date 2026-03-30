# Multi-Agent Workflow Patterns

Reference catalog for reasoning about agent decomposition during design.
Adapted from Google ADK patterns for the VS Code agent plugin context.

## When to Use Multiple Agents

Use multiple agents when you need to:
- **Isolate tool permissions** between stages (read-only brainstorming vs. write implementation)
- **Parallelize** independent work (fan-out to N repos or N review specialists)
- **Isolate context** so one stage's verbose output doesn't consume another's instruction budget

Use a single agent when:
- No tool partitioning is needed
- Work is sequential and context flows naturally
- The task is a single coherent procedure

## Patterns

### Sequential Pipeline (Handoffs)
Agent A finishes → hands off to Agent B → Agent B finishes → hands off to Agent C.
Each agent has its own tools and instructions. Context carries forward via the handoff.

**Use when:** Stages need different tool permissions or personas.
**VS Code mechanism:** `handoffs` in agent frontmatter with `send: true`.

Example: brainstorming (read-only) → doc writing (file write) → PR creation (github tools)

### Parallel Fan-Out / Gather
Orchestrator spawns N sub-agents simultaneously. Each works independently.
Orchestrator gathers and synthesizes results.

**Use when:** Independent tasks that benefit from parallelism or context isolation.
**VS Code mechanism:** `agents` in frontmatter + `runSubagent` tool.

Example: code review (5 specialist reviewers in parallel), change propagation (N repos)

### Generator / Critic Loop
Generator produces output. Critic evaluates against criteria. Loop until passing.

**Use when:** Output quality needs validation against hard criteria.
**VS Code mechanism:** Single agent with iterative prompting, or sub-agent as critic.

Example: TDD (write tests → implement → run tests → fix → repeat)

### Coordinator / Dispatcher
Central agent analyzes intent and routes to the right specialist.

**Use when:** Multiple specialist agents exist and the right one depends on user input.
**VS Code mechanism:** Parent agent with `agents` list; model picks based on descriptions.

### Hierarchical Decomposition
Parent breaks large task into sub-tasks, delegates to child agents, synthesizes results.

**Use when:** Task is too large for one agent's context window.
**VS Code mechanism:** Nested sub-agents.

## Decision Framework

Ask in order:
1. Does this need different tool permissions at different stages? → **Sequential pipeline**
2. Are there independent parallel tasks? → **Fan-out / gather**
3. Does output need iterative validation? → **Generator / critic**
4. Is intent ambiguous with multiple specialists? → **Coordinator**
5. Is the task too large for one context? → **Hierarchical**
6. None of the above? → **Single agent with skills**
