**0.2.0**

 - Restructure as a Claude Code plugin with a self-hosted marketplace.
   Components (``agents/``, ``commands/``) live at the plugin root per
   Claude plugin conventions, with manifest at ``.claude-plugin/plugin.json``
   and marketplace catalog at ``.claude-plugin/marketplace.json``. VS Code
   Copilot reads the same layout natively. Tool names mapped from Copilot
   vocabulary to Claude vocabulary. Slash commands ``/viv:code-review`` and
   ``/viv:debug-regression`` added for Claude Code (plugin namespace ``viv``).
 - Tighten review sub-agents: ``_review_maintainability``, ``_review_dry``,
   ``_review_design``, ``_review_tests``, and ``_review_documentation`` no
   longer declare ``Bash``. They analyze code via ``Read``, ``Grep``, and
   ``Glob`` only; the orchestrator gathers PR context and passes it in.
   Documented recommended ``permissions.deny`` snippet for users running in
   bypass/auto modes.
 - Fix orchestrator subagent-spawning tool field: ``code_reviewer`` and
   ``model_regression_debugger`` now declare
   ``Agent(_review_maintainability, _review_dry, ...)`` and
   ``Agent(_diff_analyzer, _hypothesis_tester)`` respectively, using the
   documented allowlist syntax. Replaces the incorrect ``Task`` tool name and
   the redundant ``agents:`` stowaway field (which was confusing the Copilot
   parser).

**0.1.0 - 7/29/25**

 - Initial repository setup
