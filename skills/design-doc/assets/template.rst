.. This template is used by the design-doc skill to generate design documents.
.. Replace all placeholder text (in angle brackets or ALL CAPS) with actual content.
.. Delete sections that do not apply, but justify the deletion in a comment.

=============
DOCUMENT TITLE
=============

.. list-table::
   :widths: 30 70

   * - **Target release**
     - RELEASE_VERSION
   * - **Epic**
     - EPIC_LINK
   * - **Document status**
     - DRAFT
   * - **Document owner**
     - OWNER_NAME
   * - **Designer**
     - DESIGNER_NAME
   * - **Developers**
     - DEVELOPER_NAMES
   * - **QA**
     - QA_NAMES

.. contents:: Table of Contents
   :depth: 2

Goals
=====

STATE_GOALS_HERE

Background and strategic fit
=============================

STATE_BACKGROUND_HERE

Assumptions
===========

STATE_ASSUMPTIONS_HERE

Requirements
============

.. list-table::
   :header-rows: 1
   :widths: 5 15 40 15 25

   * - #
     - Title
     - User Story
     - Importance
     - Notes
   * - 1
     - TITLE
     - As a <type of user>, I want <goal> so that <reason>.
     - Must have / Nice to have
     - NOTES

Current state (if applicable)
=============================

DESCRIBE_CURRENT_STATE_OR_DELETE

User interaction and design
===========================

DESCRIBE_USER_INTERACTION

Performance Implications
========================

Discuss how this implementation is expected to impact asymptotic runtime or
memory performance of framework code or model runs, and as needed incorporate
profiling tasks into the implementation process.

Questions
=========

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Question
     - Outcome
   * - QUESTION_TEXT
     - OUTCOME_TEXT

Not Doing
=========

STATE_WHAT_IS_OUT_OF_SCOPE

Tasks
=====

.. list-table::
   :header-rows: 1
   :widths: 10 15 10 25 10 10 20

   * - Ticket
     - Title
     - Priority
     - Description
     - Story points
     - Est. time (days)
     - Est. time - waiting (days)
   * - TBD
     - TITLE
     - Critical / Major / Minor / Trivial
     - DESCRIPTION
     - X.01
     - HEAD_DOWN_DAYS
     - TOTAL_INCLUDING_WAITING

Time estimate
=============

The entirety of this effort is anticipated to take a single engineer:
STATE_ESTIMATE
