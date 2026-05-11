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

**0.1.0 - 7/29/25**

 - Initial repository setup
