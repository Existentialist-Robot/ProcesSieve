# AGENTS.md

`.repo-relation.yaml` (startup tier 0) declares this file as tier 1. `README.md` is the orientation
page (what the engine does, its stack, data model, setup and API); `schema.yaml` and the `Makefile`
are read on demand.

## Architecture review and writer boundary

Changes to this repository's architecture record (the `architecture:` block of
`.repo-relation.yaml`, and this section) follow one review boundary:

- They are made in the author's own worktree on a review branch, and only that branch is pushed.
- The sanctioned writer named by `.repo-relation.yaml` (`canonical_home`, `writers`) merges them,
  after an independent review by a reviewer other than the author.
- No change here publishes architecture metadata about any other repository.
