=================
Vivarium AI Tools
=================

Vivarium AI Tools is a VS Code agent plugin for the vivarium ecosystem. It
provides AI-assisted development workflows including code review, design
document creation, and PR management.

Agents
======

**User-invocable:**

- ``code_reviewer`` — orchestrates parallel code review across 5 specialist sub-agents
- ``design-brainstormer`` — structured brainstorming through collaborative dialogue (read-only)
- ``design-doc-writer`` — writes formal RST design documents from approved designs

**Sub-agents (invoked by orchestrators):**

- ``review_maintainability``
- ``review_dry``
- ``review_design``
- ``review_tests``
- ``review_documentation``

Skills
======

- ``brainstorming`` — structured ideation process with multi-agent pattern reference
- ``design-doc`` — RST design document generation from team template
- ``pull-request`` — PR creation using repo-specific templates and ``gh`` CLI

Repository Layout
=================

Follows the `VS Code agent plugin <https://code.visualstudio.com/docs/copilot/customization/agent-plugins>`_
convention with `agentskills.io <https://agentskills.io/specification>`_ skill format::

    plugin.json              # Plugin metadata
    agents/                  # Custom agent definitions
    skills/                  # Agent skills (agentskills.io spec)
      brainstorming/
      design-doc/
      pull-request/

Using as a local plugin
=======================

To register this as a local plugin in VS Code, add this path to ``chat.pluginLocations`` in settings:

.. code-block:: json

   {
     "chat.pluginLocations": {
       "/your/path/to/vivarium_ai_tools": true
     }
   }

Then reload VS Code and verify the plugin appears in the Agent Plugins UI.
