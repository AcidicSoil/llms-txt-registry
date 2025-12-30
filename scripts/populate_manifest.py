#!/usr/bin/env python3
import sys
import json
import re
import shutil
from pathlib import Path

# Ensure src is in path
sys.path.append(str(Path(__file__).parent.parent))

from src.registry_config.loader import load_manifest, save_manifest
from src.registry_config.models import Source

def to_slug(text: str) -> str:
    """Convert mixed case/space text to a slug."""
    # Convert camelCase to hyphen-separated
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    # Replace invalid chars with hyphen
    return re.sub(r'[^a-z0-9]+', '-', s2).strip('-')

def scan_and_populate(manifest_path="sources.json", docs_root="docs"):
    manifest = load_manifest(manifest_path)
    existing_ids = {s.id for s in manifest.sources}
    docs_path = Path(docs_root)
    
    if not docs_path.exists():
        print(f"Docs directory '{docs_root}' does not exist.")
        return

    added_count = 0
    renamed_count = 0
    
    # Sort folders for stable ordering
    # We list first to avoid modification issues during iteration if we rename
    items = sorted([x for x in docs_path.iterdir() if x.is_dir() and not x.name.startswith(".")])

    for item in items:
        original_name = item.name
        slug_id = to_slug(original_name)
        
        # If directory name doesn't match slug, rename it for consistency
        if original_name != slug_id:
            new_path = item.parent / slug_id
            if new_path.exists():
                print(f"Skipping rename of '{original_name}' -> '{slug_id}' because target exists.")
                # We'll just skip this one or use the existing target in next pass
                continue
                
            print(f"Renaming directory: {original_name} -> {slug_id}")
            shutil.move(str(item), str(new_path))
            item = new_path
            renamed_count += 1

        if slug_id in existing_ids:
            continue
            
        # Attempt to guess URL from artifacts
        url = f"https://github.com/TODO/{slug_id}"
        
        # Simple heuristic: check if there is an llms.txt and see if it has a github link
        # We check common name patterns
        potential_files = [
            item / f"{slug_id}-llms.txt",
            item / f"{original_name}-llms.txt",
            item / "llms.txt"
        ]
        
        for llms_file in potential_files:
            if llms_file.exists():
                try:
                    content = llms_file.read_text(encoding="utf-8", errors="ignore")
                    match = re.search(r'https://github\.com/[\w-]+/[\w.-]+', content[:1000])
                    if match:
                        url = match.group(0)
                        break
                except Exception:
                    pass

        print(f"Found new artifact directory: {slug_id}")
        
        try:
            new_source = Source(
                id=slug_id,
                url=url,
                type="repo",
                profile="default",
                enabled=False,
                tags=["imported"]
            )
            
            manifest.sources.append(new_source)
            existing_ids.add(slug_id)
            added_count += 1
        except Exception as e:
            print(f"Error adding source {slug_id}: {e}")

    if added_count > 0 or renamed_count > 0:
        save_manifest(manifest, manifest_path)
        print(f"\nSummary:")
        print(f"- Renamed directories: {renamed_count}")
        print(f"- Added sources: {added_count}")
        print(f"- Updated: {manifest_path}")
        print("\nNOTE: New sources are set to 'enabled: false'. Please review their URLs and enable them.")
    else:
        print("No new sources found in docs/ directory.")

if __name__ == "__main__":
    scan_and_populate()