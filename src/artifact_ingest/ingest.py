import shutil
import json
import time
from pathlib import Path
from typing import List, Dict, Optional

def normalize_line_endings(path: Path):
    """Ensure file uses LF line endings."""
    content = path.read_bytes()
    normalized = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    path.write_bytes(normalized)

def ingest_artifacts(
    source_id: str, 
    temp_dir: Path, 
    docs_root: Path, 
    model_used: Optional[str] = None
) -> List[str]:
    """Normalize and move artifacts to docs/<id>/, and generate metadata."""
    target_dir = docs_root / source_id
    target_dir.mkdir(parents=True, exist_ok=True)
    
    ingested_files = []
    
    # Find all *-llms*.txt files in the temp dir
    for artifact in temp_dir.glob("**/*-llms*.txt"):
        # Normalize and copy
        normalize_line_endings(artifact)
        
        target_path = target_dir / artifact.name
        shutil.copy2(artifact, target_path)
        ingested_files.append(str(target_path.relative_to(docs_root)))

    # Generate metadata.json
    metadata = {
        "source_id": source_id,
        "last_refreshed": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model_used": model_used or "unknown",
        "artifacts": ingested_files
    }
    
    with (target_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        f.write("\n")
        
    return ingested_files
