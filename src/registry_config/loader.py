import json
from pathlib import Path
from typing import Optional
from .models import Manifest

def load_manifest(path: str = "sources.json") -> Manifest:
    """Load and validate the source manifest."""
    p = Path(path)
    if not p.exists():
        return Manifest()
    
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    return Manifest.model_validate(data)

def save_manifest(manifest: Manifest, path: str = "sources.json") -> None:
    """Save the manifest to disk with consistent formatting."""
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(manifest.model_dump(exclude_none=True), f, indent=2)
        f.write("\n")
