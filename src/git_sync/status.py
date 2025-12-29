import subprocess
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

def get_staged_changes() -> List[str]:
    """Return a list of staged files using git status --porcelain."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        return [line[3:].strip() for line in result.stdout.splitlines() if line.startswith("M ") or line.startswith("A ")]
    except Exception as e:
        logger.error(f"Failed to get git status: {e}")
        return []

def check_stale_artifacts(manifest_path: str = "sources.json", docs_root: str = "docs") -> bool:
    """
    Heuristic check: if sources.json is modified but docs/ isn't changed in the same commit,
    it might be stale.
    """
    staged = get_staged_changes()
    if manifest_path in staged:
        # Check if any file in docs/ is also staged
        docs_changes = [f for f in staged if f.startswith(docs_root)]
        if not docs_changes:
            return True # Stale
    return False
