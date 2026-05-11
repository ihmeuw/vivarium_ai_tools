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

Security model and recommended deny rules
=========================================

The 9 agents in this plugin have the following shell access:

- The 5 ``_review_*`` sub-agents have **no Bash access at all**. They are
  fed PR context by the orchestrator and analyze code with ``Read``,
  ``Grep``, and ``Glob`` only.
- ``code_reviewer``, ``model_regression_debugger``, ``_diff_analyzer``,
  and ``_hypothesis_tester`` declare ``Bash`` to run ``git`` and ``gh``
  commands. In practice, every operation they perform is a read-only git
  command (``git diff``, ``git log``, ``git show``, ``git status``),
  which Claude Code auto-approves via its built-in read-only command
  allowlist — no prompts, no scoping needed.

For destructive or out-of-scope commands, Claude Code's default
permission system prompts you before execution, so a prompt-injected
agent cannot silently run ``rm``, ``curl``, or similar without your
approval.

If you run with ``defaultMode: bypassPermissions`` or ``auto``, or
otherwise want an explicit deny floor that cannot be bypassed by an
errant prompt-allow, add this snippet to ``~/.claude/settings.json``:

.. code-block:: json

   {
     "permissions": {
       "deny": [
         "Bash(git push *)",
         "Bash(git reset --hard *)",
         "Bash(git rebase *)",
         "Bash(git clean -fd *)",
         "Bash(gh repo delete *)",
         "Bash(gh auth logout *)",
         "Bash(gh pr close *)"
       ]
     }
   }

Deny rules take precedence over allow rules and over hook decisions, so
these will block the listed commands in every permission mode.

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
