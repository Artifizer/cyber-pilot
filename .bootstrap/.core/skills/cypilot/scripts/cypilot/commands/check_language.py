"""check-language command — scan Markdown artifacts for disallowed Unicode scripts."""

import argparse
from pathlib import Path
from typing import List

from ..utils import error_codes as EC
from ..utils.ui import ui


def cmd_check_language(argv: List[str]) -> int:
    """Scan Markdown files for characters outside the allowed language set.

    Exit codes:
        0 — all files pass
        1 — configuration / path error
        2 — one or more language violations found
    """
    p = argparse.ArgumentParser(
        prog="check-language",
        description=(
            "Scan Markdown artifacts for characters outside the allowed Unicode "
            "script set.  Language policy is read from workspace config "
            "([validation] allowed_content_languages) or set via --languages."
        ),
    )
    p.add_argument(
        "paths",
        nargs="*",
        metavar="path",
        help="Files or directories to scan (default: project architecture/ folder)",
    )
    p.add_argument(
        "--languages",
        default=None,
        metavar="CODES",
        help="Comma-separated language codes to allow, e.g. 'en' or 'en,ru'. "
             "Overrides workspace config.",
    )
    p.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        dest="exclude",
        help=(
            "Glob pattern for paths to skip (relative to each scan root). "
            "Repeatable: --exclude 'translations/**' --exclude 'specs/i18n/*.md'. "
            "Merged with check_language_ignore_paths from workspace config."
        ),
    )
    p.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress summary header; show violations only.",
    )
    args = p.parse_args(argv)

    from ..utils.content_language import (
        SUPPORTED_LANGUAGES,
        build_allowed_ranges,
        scan_paths,
    )

    # ── Resolve allowed languages ────────────────────────────────────────────
    if args.languages is not None:
        raw_langs = [lang_code.strip().lower() for lang_code in args.languages.split(",") if lang_code.strip()]
        unknown = [lang_code for lang_code in raw_langs if lang_code not in SUPPORTED_LANGUAGES]
        if unknown:
            ui.result({
                "status": "ERROR",
                "message": (
                    f"Unknown language code(s): {', '.join(unknown)}. "
                    f"Supported: {', '.join(SUPPORTED_LANGUAGES)}"
                ),
            })
            return 1
        allowed_langs = raw_langs
    else:
        allowed_langs = _read_config_languages()

    # ── Resolve ignore globs ─────────────────────────────────────────────────
    ignore_globs: List[str] = list(args.exclude) + _read_config_ignore_paths()

    # ── Resolve scan roots ───────────────────────────────────────────────────
    if args.paths:
        roots = [Path(pth) for pth in args.paths]
    else:
        roots = _default_roots()

    missing = [str(r) for r in roots if not r.exists()]
    if missing:
        ui.result({
            "status": "ERROR",
            "message": f"Path(s) not found: {', '.join(missing)}",
        })
        return 1

    # ── Scan ─────────────────────────────────────────────────────────────────
    allowed_ranges = build_allowed_ranges(allowed_langs)
    from ..utils.content_language import LangScanError
    try:
        violations = scan_paths(roots, allowed_ranges, ignore_globs=ignore_globs or None)
    except LangScanError as exc:
        ui.result({
            "status": "ERROR",
            "message": str(exc),
        })
        return 1

    files_scanned = _count_md_files(roots)

    if not violations:
        result = {
            "status": "PASS",
            "allowed_languages": allowed_langs,
            "files_scanned": files_scanned,
            "violation_count": 0,
        }
        if ignore_globs:
            result["ignore_globs"] = ignore_globs
        ui.result(result, human_fn=lambda d: _human_result(d, quiet=args.quiet))
        return 0

    # Group violations by file for reporting
    by_file: dict = {}
    for v in violations:
        by_file.setdefault(str(v.path), []).append(v)

    violation_items = []
    for file_path, file_violations in by_file.items():
        for v in file_violations:
            violation_items.append({
                "path": file_path,
                "line": v.lineno,
                "chars": v.bad_chars_preview(),
                "preview": v.line_preview(),
                "code": EC.CONTENT_LANGUAGE_VIOLATION,
            })

    result = {
        "status": "FAIL",
        "allowed_languages": allowed_langs,
        "files_scanned": files_scanned,
        "violation_count": len(violations),
        "file_count": len(by_file),
        "violations": violation_items,
    }
    if ignore_globs:
        result["ignore_globs"] = ignore_globs
    ui.result(result, human_fn=lambda d: _human_result(d, quiet=args.quiet))
    return 2


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_config_languages() -> List[str]:
    """Read allowed_content_languages from workspace config; fall back to ['en']."""
    try:
        from ..utils.context import get_context
        from ..utils.workspace import find_workspace_config

        ctx = get_context()
        if ctx is None:
            return ["en"]
        _ws_cfg, _ = find_workspace_config(ctx.project_root)
        if _ws_cfg is not None and _ws_cfg.validation is not None:  # type: ignore[union-attr]
            langs = _ws_cfg.validation.allowed_content_languages  # type: ignore[union-attr]
            if langs:
                return langs
    except Exception:
        pass
    return ["en"]


def _read_config_ignore_paths() -> List[str]:
    """Read check_language_ignore_paths from workspace config; fall back to []."""
    try:
        from ..utils.context import get_context
        from ..utils.workspace import find_workspace_config

        ctx = get_context()
        if ctx is None:
            return []
        _ws_cfg, _ = find_workspace_config(ctx.project_root)
        if _ws_cfg is not None and _ws_cfg.validation is not None:  # type: ignore[union-attr]
            paths = _ws_cfg.validation.check_language_ignore_paths  # type: ignore[union-attr]
            if paths:
                return list(paths)
    except Exception:
        pass
    return []


def _default_roots() -> List[Path]:
    """Return the default scan root (architecture/ under project root)."""
    try:
        from ..utils.context import get_context

        ctx = get_context()
        if ctx is not None:
            return [ctx.project_root / "architecture"]
    except Exception:
        pass
    return [Path.cwd() / "architecture"]


def _count_md_files(roots: List[Path]) -> int:
    count = 0
    for root in roots:
        if root.is_file():
            if root.suffix.lower() == ".md":
                count += 1
        elif root.is_dir():
            count += sum(1 for _ in root.rglob("*.md"))
    return count


# ---------------------------------------------------------------------------
# Human formatter
# ---------------------------------------------------------------------------

def _human_result(data: dict, quiet: bool = False) -> None:
    status = data.get("status", "")
    allowed = data.get("allowed_languages", [])

    if not quiet:
        ui.header("check-language")
        ui.detail("Allowed languages", ", ".join(allowed))
        n_files = data.get("files_scanned", 0)
        ui.detail("Files scanned", str(n_files))
        ui.blank()

    if status == "PASS":
        ui.success("No language violations found.")
        ui.blank()
        return

    if status == "ERROR":
        ui.error(str(data.get("message", "Unknown error")))
        ui.blank()
        return

    n_viol = data.get("violation_count", 0)
    n_file_count = data.get("file_count", 0)
    ui.warn(f"FAIL  {n_viol} violation(s) in {n_file_count} file(s)")
    ui.blank()

    violations = data.get("violations", [])
    by_file: dict = {}
    for v in violations:
        by_file.setdefault(v["path"], []).append(v)

    for file_path, file_violations in by_file.items():
        ui.substep(f"  {ui.relpath(file_path)}  ({len(file_violations)} line(s))")
        for v in file_violations:
            ui.substep(f"    line {v['line']:>4}  [{v['chars']}]  {v['preview']}")
        ui.blank()

    ui.hint("Fix: rewrite flagged content in the allowed language(s).")
    ui.hint(
        "To allow additional scripts, add to .cypilot-workspace.toml:\n"
        "  [validation]\n"
        "  allowed_content_languages = [\"en\", \"ru\"]"
    )
    ui.hint(
        "To ignore specific paths (e.g. translation specs), use --exclude or add to config:\n"
        "  [validation]\n"
        "  check_language_ignore_paths = [\"translations/**\", \"specs/i18n/*.md\"]\n"
        "To ignore a single file, add  <!-- cpt-lang: ignore -->  anywhere in the file."
    )
    if data.get("ignore_globs"):
        ui.detail("Active ignore globs", ", ".join(data["ignore_globs"]))
    ui.blank()
