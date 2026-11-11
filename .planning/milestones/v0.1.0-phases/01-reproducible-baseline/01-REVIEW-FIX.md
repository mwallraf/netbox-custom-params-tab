---
phase: 01-reproducible-baseline
review: 01-REVIEW.md
status: verified
fixed: [CR-01, CR-02, WR-01]
remaining: []
---

# Phase 1: Review Fix Verification

Reviewed the current fixes in sandbox.py, lifecycle_sandbox.py, legacy_tests.py,
and test_lifecycle.py. Original findings remain preserved in 01-REVIEW.md.

## Fixed Issues

### CR-01: Reset inspects a different Docker environment from the one it mutates

**Resolution:** Fixed. Compose mutations, Docker metadata inspection, and legacy
runner subprocesses now call the same `sandbox.docker_environment()` builder.
It consistently removes ambient DOCKER_/COMPOSE_ overrides and applies the local
project environment. The regression sets nondefault DOCKER_HOST/DOCKER_CONTEXT
and compares the actual environment passed to both subprocess paths.

### CR-02: Resource validation never checks actual service volume bindings

**Resolution:** Fixed. The rendered service set is restricted. Each service's
mounts must match an exact type/source/destination/read-only map. Database/cache
mounts must use the designated named volumes; application binds must resolve to
the canonical existing repository paths without symlink redirection. Unknown,
duplicate and subpath mounts are rejected. Named volume driver options and
unsafe namespace overrides are also rejected. Foreign database-bind and
symlinked-source regression tests pass.

### WR-01: Persistence verification silently recreates the record it is meant to verify

**Resolution:** Fixed. The initial sentinel gets an unpredictable marker. Later
reads use `Site.objects.get()` without creation and compare the marker, primary
key and read-only native seed snapshot. A recreated deterministic database no
longer reproduces the random marker. Missing sentinel reads fail. The regression
checks that the verification path contains only the read operation and calls the
read-only seed snapshot.

## Remaining Issues

None found in these three corrections. This is a focused fix review, not a new
audit of unrelated feature code.

## Verification

`python3 -m unittest discover -s tests/sandbox -p test_lifecycle.py -v`:
10 tests passed. No Docker calls, escalations, source edits or commits were made
by this reviewer. The parent owns the separate live lifecycle rerun; its result
is not claimed here.
