=================
Vivarium AI Tools
=================

Vivarium AI Tools is a Claude Code plugin providing custom agent
workflows for vivarium development. The repository is structured as
both a plugin and a single-plugin marketplace, so Claude Code users can
install it via the marketplace mechanism. VS Code GitHub Copilot reads
the same Claude-format components natively.

It includes:

**Code Reviewer**

- ``code_reviewer`` — orchestrator that delegates to specialist sub-agents
- ``_review_maintainability`` - sub-agent that reviews readability, documentation, implicit assumptions, and coupling
- ``_review_dry`` - sub-agent that identifies duplicated logic, missed abstractions, and repeated patterns
- ``_review_design`` - sub-agent that evaluates data structure choices, algorithmic efficiency, API surface, and representation trade-offs
- ``_review_tests`` - sub-agent that assesses test coverage, test quality, edge cases, and test naming and structure
- ``_review_documentation`` - sub-agent that checks docstring quality, accuracy, and completeness, as well as comments and changelog updates

Slash command (Claude Code only): ``/viv:code-review <PR or description>``.

**Regression Debugger**

- ``model_regression_debugger`` — orchestrator that traces data pipeline changes across repos to find the cause of simulation regressions
- ``_diff_analyzer`` — sub-agent that analyzes diffs in a single repo (run in parallel for multi-repo changes)
- ``_hypothesis_tester`` — sub-agent that tests a single hypothesis about a regression cause

Slash command (Claude Code only): ``/viv:debug-regression <symptom and context>``.

Repository Layout
=================

- ``.claude-plugin/plugin.json``: plugin manifest (auto-detected by VS Code Copilot)
- ``.claude-plugin/marketplace.json``: marketplace catalog so Claude Code can install this as a plugin
- ``agents/``: 9 custom agent definitions (orchestrators + sub-agents)
- ``commands/``: Claude Code slash commands that delegate to the orchestrators
- project metadata files copied from ``vivarium_dependencies``

Installing in Claude Code
=========================

Add the marketplace and install the plugin:

.. code-block:: shell

   /plugin marketplace add ihmeuw/vivarium_ai_tools
   /plugin install viv@vivarium-ai-tools

For local development against a checked-out copy:

.. code-block:: shell

   /plugin marketplace add /path/to/vivarium_ai_tools
   /plugin install viv@vivarium-ai-tools

Once installed, agents are invocable as ``@code_reviewer`` and
``@model_regression_debugger``. Slash commands are namespaced under the
plugin name: ``/viv:code-review`` and ``/viv:debug-regression``.

Installing in VS Code GitHub Copilot
====================================

Add this path to ``chat.pluginLocations`` in settings:

.. code-block:: json

   {
     "chat.pluginLocations": {
       "/your/path/to/vivarium_ai_tools": true
     }
   }

Then reload VS Code and verify the plugin appears in the Agent Plugins
UI. The agents will appear in the Copilot agent picker. Slash commands
are intentionally Claude-only — Copilot's agent picker is the
equivalent surface there.
