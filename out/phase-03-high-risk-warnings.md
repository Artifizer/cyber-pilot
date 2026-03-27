# Phase 3 — High-risk warnings

## Enabled Warning IDs

| ID | Name | Description |
|----|------|-------------|
| W0718 | broad-exception-caught | Catching too general exception `Exception` |
| W1510 | subprocess-run-check | `subprocess.run` without `check` argument |
| W0707 | raise-missing-from | Exception not chained with `from` |
| W0404 | reimported | Module reimported |
| W0212 | protected-access | Access to protected member of a client class |
| W0603 | global-statement | Using the `global` statement |
| W0612 | unused-variable | Unused variable |
| W0613 | unused-argument | Unused function argument |
| W0611 | unused-import | Unused import |

## Summary

All Phase 3 warning IDs are clean in `make pylint`.
All 2106 tests pass (0 failures, 2 skipped).

37 files changed: 153 insertions, 169 deletions (net −16 lines).

## Fix Categories

### W0718 — broad-exception-caught (bulk of changes)

Narrowed `except Exception` to specific exception tuples across ~60 call sites:

- **File I/O**: `OSError`
- **Parsing (TOML/JSON/YAML)**: `ValueError`, `KeyError`, `tomllib.TOMLDecodeError`
- **Path resolution**: `ValueError`, `OSError`
- **Dict/config access**: `KeyError`
- **Network/download** (`_download_kit_from_github`): callers catch `RuntimeError` (the function's documented contract)
- **Mixed I/O + parsing**: `(OSError, ValueError, KeyError)`
- **With `RuntimeError` from download helpers**: `(OSError, ValueError, KeyError, RuntimeError)`

Two legitimate safety-net catches retained as `except Exception` with inline disable + explanation:
- `kit.py:1553` — per-kit update loop must not crash on any single kit failure
- `migrate.py:1913` — rollback must trigger on any failure during migration

### W0707 — raise-missing-from

Chained exceptions with `from exc` in `workspace_init.py`.

### W0611 — unused-import

Removed unused imports from 14 files: `json`, `os`, `Tuple`, `Dict`, `Optional`, `field`, `argparse`, `AutodetectRule`, `_gen_readme`, `find_project_root`, `find_cypilot_directory`, `load_artifacts_meta`, `ui`.

### W0612 — unused-variable

Removed or renamed with `_` prefix: `gen_dir` → `_gen_dir` in `migrate.py` and `update.py`, `_args`/`_copy_report` in `agents.py`.

### W0613 — unused-argument

Renamed unused arguments with leading underscore: `_argv` in deprecated `cmd_kit_migrate`, `_cypilot_dir` in `_register_kit_in_core_toml`, `_v2_systems`/`_gen_dir`/`_all_warnings` in migrate helpers.

### W0603 — global-statement

Added explanatory comments to existing `global` disables in `ui.py` and `context.py` (singleton patterns).

### W0212 — protected-access

Added explanatory comments to existing disables in `context.py` (module-level helpers accessing same-module internals).

### W1510, W0404

No violations found in the codebase for these IDs.

## Production Files Modified

| File | Changes |
|------|---------|
| `pyproject.toml` | Enabled Phase 3 warning IDs |
| `src/cypilot_proxy/cache.py` | Narrowed broad exceptions |
| `src/cypilot_proxy/cli.py` | Narrowed broad exceptions |
| `src/cypilot_proxy/resolve.py` | Narrowed broad exceptions |
| `skills/.../cli.py` | Added explanation to import-outside-toplevel disable |
| `skills/.../commands/adapter_info.py` | Removed unused import; narrowed exceptions |
| `skills/.../commands/agents.py` | Removed unused import; narrowed exceptions; renamed unused vars |
| `skills/.../commands/get_content.py` | Removed unused imports |
| `skills/.../commands/init.py` | Removed unused imports; narrowed exceptions; renamed unused arg |
| `skills/.../commands/kit.py` | Narrowed exceptions; renamed unused args; safety-net disable |
| `skills/.../commands/list_id_kinds.py` | Removed unused import |
| `skills/.../commands/list_ids.py` | Removed unused import; narrowed exception |
| `skills/.../commands/migrate.py` | Removed unused imports; narrowed exceptions; renamed unused args/vars; safety-net disable |
| `skills/.../commands/self_check.py` | Removed unused imports; narrowed exceptions |
| `skills/.../commands/toc.py` | Removed unused import |
| `skills/.../commands/update.py` | Removed unused imports/var; narrowed exceptions |
| `skills/.../commands/validate.py` | Narrowed exceptions; removed unused import |
| `skills/.../commands/validate_kits.py` | Removed unused import; narrowed exception |
| `skills/.../commands/validate_toc.py` | Removed unused import |
| `skills/.../commands/workspace_init.py` | Chained exception with `from exc` |
| `skills/.../utils/artifacts_meta.py` | Narrowed exceptions |
| `skills/.../utils/codebase.py` | Narrowed exceptions |
| `skills/.../utils/constraints.py` | Added explanation to unused-argument disable |
| `skills/.../utils/context.py` | Added explanations to protected-access/global-statement disables |
| `skills/.../utils/coverage.py` | Removed unused import |
| `skills/.../utils/diff_engine.py` | Narrowed exceptions |
| `skills/.../utils/document.py` | Narrowed exceptions |
| `skills/.../utils/files.py` | Narrowed exceptions |
| `skills/.../utils/fixing.py` | Narrowed exceptions |
| `skills/.../utils/git_utils.py` | Narrowed exceptions |
| `skills/.../utils/ui.py` | Added explanation to global-statement disable |
| `skills/.../utils/workspace.py` | Narrowed exceptions |

## Test Files Modified

| File | Changes |
|------|---------|
| `tests/test_adapter_info.py` | Updated mock to raise `OSError` instead of `RuntimeError` |
| `tests/test_artifacts_meta.py` | Updated mocks: `ValueError` for parsing, `OSError` for file I/O |
| `tests/test_cli_py_coverage.py` | Updated mocks to realistic exception types; fixed `_FakeCtx` missing `adapter_dir`; corrected mock target for validate self-check test |
| `tests/test_diff_engine.py` | Updated mocks: `OSError` for subprocess, `ValueError` for TOC regen |
| `tests/test_files_utils.py` | Updated mocks to raise `OSError` for file read operations |

## Inline Pylint Disables (with explanations)

All `# pylint: disable` comments include an explanation:

| File | Line | Disable | Reason |
|------|------|---------|--------|
| `cli.py` | 224 | `import-outside-toplevel` | Lazy import only needed in JSON output mode |
| `kit.py` | 1553 | `broad-exception-caught` | Per-kit safety net — must not crash the update loop |
| `migrate.py` | 1913 | `broad-exception-caught` | Rollback safety net — must trigger on any failure |
| `constraints.py` | 2016 | `unused-argument` | Public API parameter reserved for future system-scoped validation |
| `context.py` | 579,584,591,601,605,611,631 | `protected-access` | Module-level helpers are part of SourceContext implementation |
| `context.py` | 836,847,855 | `global-statement` | Module-level singleton pattern for CLI context |
| `ui.py` | 37 | `global-statement` | Module-level output mode flag toggled once at CLI startup |

## Residual Backlog (deferred to later phases)

- **Refactor-category warnings** (R-family): not enabled in this phase
- **Convention-category warnings** (C-family): not enabled in this phase
- **`_download_kit_from_github` internal `except Exception`** (lines 104, 114): re-raises as `RuntimeError` with proper chaining — legitimate catch-and-wrap pattern inside a network+extraction helper
- **Complexity and duplicate-code**: Phase 4+ scope

## Verification

```text
make pylint  → exit 0, zero warnings
make test    → 2106 passed, 0 failed, 2 skipped
```
