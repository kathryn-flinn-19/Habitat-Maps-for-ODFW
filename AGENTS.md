# AGENTS.md

Context for AI coding tools working in this repository. This file points at the project docs; it does not copy them. If anything here disagrees with those docs, the docs win. Fix this file.

Owner: AI Coordinator (Jae Grunwald). Other tool-specific files (e.g. `CLAUDE.md`, `.cursor/rules`) must only point here.

## Project in one line

An accessible tool for ODFW wildlife experts to view USGS and ML species range/habitat maps and annotate errors. Accessibility (WCAG 2.2 AA, keyboard-only use) is a top priority.

## Commands

Use the exact commands in [CONTRIBUTING.md → Local checks](CONTRIBUTING.md#local-checks). <!-- TODO(Quality Owner): keep in sync once commands exist. -->

## Rules AI tools must follow

These come from the team charter and are not optional.

1. **Allowed uses only:** debugging, and generic boilerplate (empty test environments, empty Svelte app scaffolds, config). Do not write project-specific features unless a team member explicitly asks and will review and cite the result.
2. **Confidentiality:** never request, read, or process ODFW client data, including expert annotations. Public data such as USGS layers is fine. If you encounter client data, stop and tell the user.
3. **Citation:** any AI-generated code must carry a comment citing the tool (see CONTRIBUTING.md → Branches and commits).
4. **Boundaries:** respect the interfaces and data model in `docs/design.md`. Changing an interface means updating `docs/design.md` in the same change and flagging it for the people on both sides.
5. **Tests:** use synthetic annotations in tests and fixtures, never real ones.
6. **Docs:** if a change alters behavior, update `docs/requirements.md` or `docs/design.md` in the same PR.

## To be added as the project develops

| Item | Owner |
|------|-------|
| Stack and repository layout summary (link to design.md) | Team, via PM |
| Language-specific style rules not covered by the linter | Quality Owner (Adison) |
| Test framework notes and fixture locations | Testing & QA Lead (Jae) |
| Build, deploy, and rollback commands | Quality Owner (Adison) |
