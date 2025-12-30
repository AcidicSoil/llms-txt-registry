<filetree>
Project Structure:
└── src
    ├── artifact_ingest
    │   ├── __init__.py
    │   ├── index.py
    │   └── ingest.py
    ├── generator_runner
    │   ├── __init__.py
    │   └── runner.py
    ├── git_sync
    │   ├── __init__.py
    │   └── status.py
    ├── registry_config
    │   ├── __init__.py
    │   ├── loader.py
    │   └── models.py
    ├── reporting
    │   ├── __init__.py
    │   └── report.py
    └── __init__.py

</filetree>

<source_code>
src/__init__.py
```
```

src/artifact_ingest/__init__.py
```
```

src/artifact_ingest/index.py
```
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
```

src/artifact_ingest/ingest.py
```
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
```

src/git_sync/__init__.py
```
```

src/git_sync/status.py
```
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
```

src/generator_runner/__init__.py
```
```

src/generator_runner/runner.py
```
import subprocess
import os
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict
from ..registry_config.models import Source, GeneratorProfile

logger = logging.getLogger(__name__)

class GeneratorRunner:
    def __init__(self, output_root: Path, api_base: str = "http://localhost:1234/v1"):
        self.output_root = output_root
        self.api_base = api_base

    def run_source(self, source: Source, profile: Optional[GeneratorProfile] = None) -> Dict[str, any]:
        """Execute the lmstxt CLI for a single source."""
        start_time = time.time()
        
        # Determine model
        model = source.last_model_used or (profile.model if profile else None)
        
        # Prepare command - UPDATED to use 'lmstxt'
        cmd = ["lmstxt", str(source.url)]
        
        # We target a temporary output directory inside the root for isolation
        temp_out = self.output_root / "temp_work" / source.id
        temp_out.mkdir(parents=True, exist_ok=True)
        
        cmd.extend(["--output-dir", str(temp_out)])
        
        if model:
            cmd.extend(["--model", model])
        
        if self.api_base:
            cmd.extend(["--api-base", self.api_base])
            
        cmd.append("--stamp") # Always stamp for registry
        
        # Set environment variables (e.g. for CTX generation)
        env = os.environ.copy()
        env["ENABLE_CTX"] = "1" 
        
        try:
            logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=profile.timeout if profile else 300
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                # Success - scan for generated artifacts
                artifacts = [str(p.relative_to(temp_out)) for p in temp_out.glob("**/*-llms*.txt")]
                return {
                    "status": "success",
                    "duration": duration,
                    "artifacts": artifacts,
                    "temp_dir": temp_out,
                    "stdout": result.stdout,
                    "model_used": model
                }
            else:
                return {
                    "status": "failure",
                    "duration": duration,
                    "error": result.stderr or result.stdout,
                    "temp_dir": temp_out
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "failure",
                "duration": time.time() - start_time,
                "error": "Execution timed out",
                "temp_dir": temp_out
            }
        except Exception as e:
            return {
                "status": "failure",
                "duration": time.time() - start_time,
                "error": str(e),
                "temp_dir": temp_out
            }
```

src/registry_config/__init__.py
```
```

src/registry_config/loader.py
```
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
```

src/registry_config/models.py
```
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, AnyHttpUrl
import re

SLUG_REGEX = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

class GeneratorProfile(BaseModel):
    name: str = Field(..., description="Unique name of the profile")
    description: Optional[str] = None
    timeout: int = Field(default=300, description="Execution timeout in seconds")
    headers: Dict[str, str] = Field(default_factory=dict, description="Custom headers for the request")
    model: Optional[str] = Field(default=None, description="Preferred model identifier")

class Source(BaseModel):
    id: str = Field(..., description="Unique URL-safe slug ID for the source")
    url: AnyHttpUrl = Field(..., description="URL of the repository or documentation site")
    type: str = Field(default="repo", description="Type of source: 'repo' or 'site'")
    profile: Optional[str] = Field(default=None, description="Name of the generator profile to use")
    enabled: bool = Field(default=True, description="Whether this source should be processed")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    
    # Metadata fields (updated during refresh)
    last_refreshed: Optional[str] = Field(default=None, description="ISO 8601 timestamp of last successful refresh")
    last_model_used: Optional[str] = Field(default=None, description="Model used for the last generation")

    @field_validator('id')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not SLUG_REGEX.match(v):
            raise ValueError(f"ID '{v}' must be a URL-safe slug (lowercase alphanumeric with hyphens)")
        return v

class Manifest(BaseModel):
    version: str = Field(default="1.0", description="Manifest schema version")
    profiles: Dict[str, GeneratorProfile] = Field(default_factory=dict, description="Shared generator profiles")
    sources: List[Source] = Field(default_factory=list, description="List of documentation sources")

    @field_validator('sources')
    @classmethod
    def validate_unique_ids(cls, v: List[Source]) -> List[Source]:
        ids = [s.id for s in v]
        if len(ids) != len(set(ids)):
            from collections import Counter
            duplicates = [item for item, count in Counter(ids).items() if count > 1]
            raise ValueError(f"Duplicate source IDs found: {duplicates}")
        return v
```

src/reporting/__init__.py
```
```

src/reporting/report.py
```
from __future__ import annotations
import json
import time
import os
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Optional

@dataclass
class SourceResult:
    id: str
    status: str  # "success", "failure", "skipped"
    duration: float
    model_used: Optional[str] = None
    error: Optional[str] = None
    artifacts_generated: List[str] = field(default_factory=list)

@dataclass
class RunReport:
    run_id: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    results: Dict[str, SourceResult] = field(default_factory=dict)
    summary: Dict[str, int] = field(default_factory=lambda: {"success": 0, "failure": 0, "skipped": 0})

    def record_result(self, result: SourceResult):
        self.results[result.id] = result
        self.summary[result.status] += 1

    def finalize(self):
        self.end_time = time.time()

    def to_json(self, path: str = "refresh-report.json"):
        data = asdict(self)
        target_path = Path(path)
        
        # Atomic write: write to temp file then rename
        dir_name = target_path.parent
        with tempfile.NamedTemporaryFile("w", dir=str(dir_name) if dir_name.name else ".", delete=False, encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2)
            tmp.write("\n")
            tmp_path = Path(tmp.name)
            
        os.replace(tmp_path, target_path)
```

</source_code>