# Phase 1: Reproducible baseline - Discussion Log

> Audit trail only. Downstream planning/research must use 01-CONTEXT.md.

**Date:** 2026-11-06
**Phase:** 1-reproducible-baseline
**Areas discussed:** compatibility, deployments/data, Git workflow, Docker,
configuration/secrets, isolation/lifecycle, completion criteria.

## Initial discussion

The user was offered four areas: NetBox compatibility, existing installations
and data, source checkout, and development workflow. They answered all four
in one free-text response rather than selecting a subset.

## NetBox compatibility

**Question:** Existing NetBox version or initial target?

**Options presented:** Existing deployment version; Choose initial target.

**User response:** NetBox v4.7.x is the minimum requirement. Create a dedicated project sandbox separate from the NetBox already running on this workstation.

## Existing installations and data

**Question:** Is the plugin deployed, and must configuration/data be preserved?

**Options presented:** Preserve existing installations/data; Fresh project sandbox.

**User response:** Completely new and not in use. No existing application data/configuration needs preservation; dummy data may be generated in the new sandbox.

## Source checkout

**Question:** How should source development proceed?

**Options presented:** Main project checkout; Existing worktree.

**User response:** Fix current Git issues first. Use a branch per milestone, with no worktrees.

## Development workflow

**Question:** How should the sandbox be orchestrated and what is Phase 1 done?

**Options presented:** Docker-based workflow; Local environment.

**User response:** Docker is standard for running and testing NetBox. Create Makefile orchestration for installation. NetBox must run with the plugin installed; plugin features need not work yet. Generate passwords/tokens automatically. Use .env for configuration and/or native plugin parameters at agent discretion.

## Final clarification and confirmation

**Proposal:** Isolate the sandbox using a separate Compose project, volumes,
network and configurable localhost port. Preserve data/credentials on stop/start;
provide an explicit reset. Completion means boot, migrations, registered plugin,
and working admin login; feature failures can be recorded and deferred.

**User response:** “agreed, save context”.

## Agent's Discretion

Environment vs plugin-parameter split, exact patch/image after research, available
port, naming, credential generation, dummy data, and safe Git consolidation steps.

## Deferred Ideas

Existing feature phases remain unchanged. No additional feature requests.
