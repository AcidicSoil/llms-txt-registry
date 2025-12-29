import json
from pathlib import Path
from typing import List, Dict, Optional

def generate_registry_index(docs_root: Path, output_path: Path = None):
    """
    Scan docs_root for sources and generate an index.json.
    """
    index = []
    
    # Iterate over directories in docs_root
    for source_dir in docs_root.iterdir():
        if not source_dir.is_dir():
            continue
            
        metadata_path = source_dir / "metadata.json"
        source_data = {
            "id": source_dir.name,
            "artifacts": []
        }
        
        # Try to load metadata if it exists
        if metadata_path.exists():
            try:
                meta = json.loads(metadata_path.read_text(encoding="utf-8"))
                source_data["last_refreshed"] = meta.get("last_refreshed")
                source_data["model_used"] = meta.get("model_used")
                source_data["description"] = meta.get("description") # If we added this to metadata
            except Exception:
                pass
        
        # Scan for artifacts directly to be sure
        # Match llms.txt, project-llms.txt, project-llms-ctx.txt, etc.
        patterns = ["llms.txt", "*-llms*.txt"]
        found_artifacts = set()
        
        for pattern in patterns:
            for artifact in source_dir.glob(pattern):
                found_artifacts.add(str(artifact.relative_to(docs_root)))
        
        source_data["artifacts"] = sorted(list(found_artifacts))
            
        if source_data["artifacts"]:
            index.append(source_data)
            
    if output_path is None:
        output_path = docs_root / "index.json"
        
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
        
    return index