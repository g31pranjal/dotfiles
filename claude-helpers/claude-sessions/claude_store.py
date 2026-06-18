"""claude_store - Read and modify Claude Code's on-disk session data.

This is the only module that knows about the layout of ~/.claude/projects/
(transcript .jsonl files) and ~/.claude/sessions/ (live process metadata).
Display formatting and CLI wiring live in `claude-sessions`.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
SESSIONS_DIR = Path.home() / ".claude" / "sessions"

# User records whose content starts with one of these are synthetic
# (slash-command artifacts and resume-replay scaffolding), not typed input.
SYNTHETIC_PREFIXES = (
    "<local-command-caveat>",
    "<local-command-stdout>",
    "<local-command-stderr>",
    "<command-name>",
    "<command-message>",
    "<command-args>",
)


# ---- path helpers -----------------------------------------------------------

def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def encode_cwd(cwd):
    """Same encoding Claude Code uses for ~/.claude/projects/<dir>: / and _ -> -."""
    return cwd.replace("/", "-").replace("_", "-")


def normalize_cwd(s):
    p = Path(s).expanduser()
    if not p.is_absolute():
        p = Path.cwd() / p
    s = str(p).rstrip("/")
    return s or "/"


# ---- transcript readers -----------------------------------------------------

def user_text(rec):
    content = rec.get("message", {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                return part.get("text", "")
    return ""


def is_synthetic_user(rec):
    if rec.get("isMeta"):
        return True
    return user_text(rec).lstrip().startswith(SYNTHETIC_PREFIXES)


def session_summary(jsonl_path):
    cwd = None
    custom_title = None
    first_msg = None
    msg_count = 0
    last_ts = None
    resumed = None  # True if first user record was synthetic; False once we see a real one

    with jsonl_path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            rec_type = rec.get("type")

            if rec_type == "custom-title":
                custom_title = rec.get("customTitle")
                continue

            if rec_type in ("user", "assistant"):
                msg_count += 1
                ts = rec.get("timestamp")
                if ts:
                    last_ts = ts

            if rec_type == "user":
                if cwd is None:
                    cwd = rec.get("cwd")
                if first_msg is None:
                    synthetic = is_synthetic_user(rec)
                    if resumed is None:
                        resumed = synthetic
                    if not synthetic:
                        first_msg = user_text(rec)

    cwd_inferred = cwd is None
    if cwd_inferred:
        cwd = jsonl_path.parent.name

    return {
        "session_id": jsonl_path.stem,
        "cwd": cwd,
        "cwd_inferred": cwd_inferred,
        "title": custom_title,
        "first_msg": first_msg or "",
        "msg_count": msg_count,
        "last_ts": last_ts,
        "mtime": jsonl_path.stat().st_mtime,
        "resumed": bool(resumed),
    }


def get_sessions(cwd_filter=None):
    """Read every transcript under PROJECTS_DIR and return a list of summaries,
    most-recent first. Pass `cwd_filter` (any user-style path; will be
    normalized) to limit to sessions whose recorded cwd matches.
    """
    target = normalize_cwd(cwd_filter) if cwd_filter else None
    rows = []
    for p in PROJECTS_DIR.glob("*/*.jsonl"):
        s = session_summary(p)
        if target is not None and (s["cwd"] or "") != target:
            continue
        rows.append(s)
    rows.sort(key=lambda r: r["last_ts"] or "", reverse=True)
    return rows


# ---- PID readers ------------------------------------------------------------

def _process_is_claude(pid):
    """Return True if pid is a running process whose command line contains 'claude'."""
    try:
        out = subprocess.run(
            ["ps", "-p", str(pid), "-o", "args="],
            capture_output=True, text=True, timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    if out.returncode != 0:
        return False
    cmd = out.stdout.strip()
    return bool(cmd) and "claude" in cmd.lower()


def get_session_to_process_maps(cwd_filter=None):
    """Return (active, dead) where each maps sessionId -> list of dicts
    {pid, cwd, started_ms}. Active = process exists and looks like claude.
    Dead = process is gone, or PID was recycled by something non-claude.

    Pass `cwd_filter` (any user-style path; will be normalized) to limit the
    result to sessions whose registered cwd matches.
    """
    target = normalize_cwd(cwd_filter) if cwd_filter else None
    active = {}
    dead = {}
    if not SESSIONS_DIR.is_dir():
        return active, dead
    for f in SESSIONS_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        pid = data.get("pid")
        sid = data.get("sessionId")
        if not isinstance(pid, int) or not sid:
            continue

        entry_cwd = data.get("cwd")
        if target is not None and (entry_cwd or "") != target:
            continue

        entry = {"pid": pid, "cwd": entry_cwd, "started_ms": data.get("startedAt")}

        try:
            os.kill(pid, 0)
            exists = True
        except ProcessLookupError:
            exists = False
        except PermissionError:
            raise RuntimeError(
                f"PID {pid} (sessionId {sid}) exists but is owned by another user — "
                f"cannot verify it's a claude process"
            )

        if not exists or not _process_is_claude(pid):
            dead.setdefault(sid, []).append(entry)
            continue

        active.setdefault(sid, []).append(entry)

    # Sort each list by pid for stable display.
    for d in (active, dead):
        for sid in d:
            d[sid].sort(key=lambda e: e["pid"])

    return active, dead


# ---- delete -----------------------------------------------------------------

def confirm(prompt):
    try:
        ans = input(f"{prompt} [y/N] ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    return ans in ("y", "yes")


def delete_session_id(sid, force):
    matches = list(PROJECTS_DIR.glob(f"*/{sid}.jsonl"))
    if not matches:
        die(f"no session found with id: {sid}")
    rc = 0
    for path in matches:
        if not force and not confirm(f"Delete {path}?"):
            print(f"Skipped {path}")
            continue
        try:
            path.unlink()
            print(f"Deleted {path}")
        except OSError as e:
            print(f"Failed to delete {path}: {e}", file=sys.stderr)
            rc = 1
    return rc


def delete_cwd(cwd_input, force):
    cwd = normalize_cwd(cwd_input)
    folder = PROJECTS_DIR / encode_cwd(cwd)
    if not folder.is_dir():
        die(f"no session folder for cwd: {cwd}\n  (looked for: {folder})")
    count = len(list(folder.glob("*.jsonl")))
    if count == 0:
        die(f"no sessions in folder: {folder}")
    if not force and not confirm(f"Delete {count} session(s) at {folder}?"):
        print("Cancelled.")
        return 0
    try:
        shutil.rmtree(folder)
    except OSError as e:
        die(f"failed to delete {folder}: {e}")
    print(f"Deleted {folder} ({count} session(s))")
    return 0
