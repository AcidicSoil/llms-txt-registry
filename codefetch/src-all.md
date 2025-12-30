<filetree>
Project Structure:
├── .github
│   └── workflows
│       └── lint.yml
├── scripts
│   ├── refresh.py
│   └── setup_hooks.sh
├── src
│   ├── artifact_ingest
│   │   ├── __init__.py
│   │   ├── index.py
│   │   └── ingest.py
│   ├── generator_runner
│   │   ├── __init__.py
│   │   └── runner.py
│   ├── git_sync
│   │   ├── __init__.py
│   │   └── status.py
│   ├── registry_config
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── models.py
│   ├── reporting
│   │   ├── __init__.py
│   │   └── report.py
│   └── __init__.py
├── tests
│   ├── test_index.py
│   ├── test_ingest.py
│   ├── test_registry_config.py
│   ├── test_reporting.py
│   └── test_runner.py
├── requirements.txt
└── sources.json

</filetree>

<source_code>
requirements.txt
```
pydantic>=2.0
```

sources.json
```
{
  "version": "1.0",
  "profiles": {
    "default": {
      "name": "default",
      "timeout": 300
    }
  },
  "sources": [
    {
      "id": "tanstack-router",
      "url": "https://github.com/tanstack/router",
      "type": "repo",
      "profile": "default"
    },
    {
      "id": "supabase",
      "url": "https://github.com/supabase/supabase",
      "type": "repo",
      "profile": "default"
    }
  ]
}
```

scripts/refresh.py
```
#!/usr/bin/env python3
import argparse
import sys
import os
import uuid
import logging
from pathlib import Path

# Ensure src is in path
sys.path.append(str(Path(__file__).parent.parent))

from src.registry_config.loader import load_manifest, save_manifest
from src.reporting.report import RunReport, SourceResult
from src.generator_runner.runner import GeneratorRunner
from src.artifact_ingest.ingest import ingest_artifacts
from src.artifact_ingest.index import generate_registry_index
from src.git_sync.status import check_stale_artifacts

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("refresh")

def main():
    parser = argparse.ArgumentParser(description="Refresh the llms-txt registry artifacts.")
    parser.add_argument("--manifest", default="sources.json", help="Path to sources.json")
    parser.add_argument("--docs-root", default="docs", help="Path to docs directory")
    parser.add_argument("--only", help="Only refresh a specific source ID")
    parser.add_argument("--api-base", default="http://localhost:1234/v1", help="LM Studio API base")
    parser.add_argument("--check", action="store_true", help="Only check for stale artifacts and exit")
    
    args = parser.parse_args()

    if args.check:
        if check_stale_artifacts(args.manifest, args.docs_root):
            logger.warning("STALE: sources.json was modified but no artifacts in docs/ were updated.")
            sys.exit(1)
        else:
            logger.info("VALID: No stale artifacts detected.")
            sys.exit(0)

    manifest = load_manifest(args.manifest)
    if not manifest.sources:
        logger.error("No sources found in manifest.")
        return

    docs_root = Path(args.docs_root)
    runner = GeneratorRunner(output_root=Path(".taskmaster/tmp"), api_base=args.api_base)
    report = RunReport(run_id=str(uuid.uuid4()))

    sources_to_run = manifest.sources
    if args.only:
        sources_to_run = [s for s in sources_to_run if s.id == args.only]
        if not sources_to_run:
            logger.error(f"Source ID '{args.only}' not found in manifest.")
            return

    try:
        for source in sources_to_run:
            if not source.enabled and not args.only:
                logger.info(f"Skipping disabled source: {source.id}")
                report.record_result(SourceResult(id=source.id, status="skipped", duration=0))
                continue

            logger.info(f"Processing source: {source.id} ({source.url})")
            profile = manifest.profiles.get(source.profile) if source.profile else None
            
            gen_result = runner.run_source(source, profile)
            
            if gen_result["status"] == "success":
                ingested = ingest_artifacts(
                    source.id, 
                    gen_result["temp_dir"], 
                    docs_root, 
                    model_used=gen_result.get("model_used")
                )
                
                # Update manifest metadata
                source.last_refreshed = gen_result.get("timestamp") or report.start_time
                source.last_model_used = gen_result.get("model_used")
                
                report.record_result(SourceResult(
                    id=source.id,
                    status="success",
                    duration=gen_result["duration"],
                    model_used=gen_result.get("model_used"),
                    artifacts_generated=ingested
                ))
                logger.info(f"SUCCESS: {source.id} - {len(ingested)} artifacts generated.")
            else:
                report.record_result(SourceResult(
                    id=source.id,
                    status="failure",
                    duration=gen_result["duration"],
                    error=gen_result.get("error")
                ))
                logger.error(f"FAILURE: {source.id} - {gen_result.get('error')}")

    finally:
        report.finalize()
        report.to_json()
        save_manifest(manifest, args.manifest)
        
        # Generate Index
        try:
            generate_registry_index(docs_root)
            logger.info("Registry index generated at docs/index.json")
        except Exception as e:
            logger.error(f"Failed to generate registry index: {e}")
            
        logger.info(f"Run complete. Report saved to refresh-report.json")

if __name__ == "__main__":
    main()
```

scripts/setup_hooks.sh
```
#!/bin/bash
HOOK_FILE=".git/hooks/pre-push"

echo "Installing pre-push hook..."

cat <<EOF > "$HOOK_FILE"
#!/bin/bash
# Task Master Registry - Pre-push Hook
# Validates that artifacts are updated if sources.json changed.

python3 scripts/refresh.py --check
RESULT=\$?

if [ \$RESULT -ne 0 ]; then
  echo "Error: Stale artifacts detected. Please run 'scripts/refresh.py' and commit the changes before pushing."
  exit 1
fi

exit 0
EOF

chmod +x "$HOOK_FILE"
echo "Hook installed successfully at $HOOK_FILE"
```

src/__init__.py
```
```

tests/test_index.py
```
import json
from pathlib import Path
from src.artifact_ingest.index import generate_registry_index

def test_generate_index(tmp_path):
    docs_root = tmp_path / "docs"
    docs_root.mkdir()
    
    # Source 1 with artifacts and metadata
    src1 = docs_root / "src1"
    src1.mkdir()
    (src1 / "llms.txt").touch()
    (src1 / "metadata.json").write_text(json.dumps({"model_used": "gpt-4"}))
    
    # Source 2 with artifacts only
    src2 = docs_root / "src2"
    src2.mkdir()
    (src2 / "foo-llms.txt").touch()
    
    # Source 3 empty
    (docs_root / "src3").mkdir()
    
    index = generate_registry_index(docs_root)
    
    assert len(index) == 2
    
    s1 = next(s for s in index if s["id"] == "src1")
    assert s1["model_used"] == "gpt-4"
    assert "src1/llms.txt" in s1["artifacts"]
    
    s2 = next(s for s in index if s["id"] == "src2")
    assert "src2/foo-llms.txt" in s2["artifacts"]
    assert "model_used" not in s2
    
    assert (docs_root / "index.json").exists()
```

tests/test_ingest.py
```
import json
from pathlib import Path
from src.artifact_ingest.ingest import ingest_artifacts

def test_ingest_artifacts(tmp_path):
    # Setup source dir
    temp_dir = tmp_path / "temp"
    temp_dir.mkdir()
    artifact = temp_dir / "foo-llms.txt"
    artifact.write_bytes(b"Hello\r\nWorld") # CRLF
    
    docs_root = tmp_path / "docs"
    docs_root.mkdir()
    
    ingested = ingest_artifacts("test-src", temp_dir, docs_root, model_used="gpt-4")
    
    # Check location
    target_file = docs_root / "test-src" / "foo-llms.txt"
    assert target_file.exists()
    assert str(target_file.relative_to(docs_root)) in ingested
    
    # Check normalization
    assert target_file.read_bytes() == b"Hello\nWorld"
    
    # Check metadata
    meta_file = docs_root / "test-src" / "metadata.json"
    assert meta_file.exists()
    meta = json.loads(meta_file.read_text())
    assert meta["source_id"] == "test-src"
    assert meta["model_used"] == "gpt-4"
    assert len(meta["artifacts"]) == 1
```

tests/test_registry_config.py
```
import pytest
from pathlib import Path
import json
from src.registry_config.models import Manifest, Source, GeneratorProfile
from src.registry_config.loader import load_manifest
from pydantic import ValidationError

def test_source_validation_slug():
    # Valid slug
    s = Source(id="valid-slug", url="https://example.com")
    assert s.id == "valid-slug"

    # Invalid slug (uppercase)
    with pytest.raises(ValidationError):
        Source(id="Invalid-Slug", url="https://example.com")

    # Invalid slug (spaces)
    with pytest.raises(ValidationError):
        Source(id="invalid slug", url="https://example.com")

def test_manifest_duplicate_ids():
    sources = [
        Source(id="s1", url="https://a.com"),
        Source(id="s1", url="https://b.com")
    ]
    with pytest.raises(ValidationError) as exc:
        Manifest(sources=sources)
    assert "Duplicate source IDs" in str(exc.value)

def test_load_manifest(tmp_path):
    manifest_file = tmp_path / "sources.json"
    data = {
        "version": "1.0",
        "profiles": {
            "default": {"name": "default", "timeout": 60}
        },
        "sources": [
            {"id": "test-source", "url": "https://example.com", "profile": "default"}
        ]
    }
    manifest_file.write_text(json.dumps(data))
    
    manifest = load_manifest(str(manifest_file))
    assert len(manifest.sources) == 1
    assert manifest.sources[0].id == "test-source"
    assert manifest.profiles["default"].timeout == 60

def test_load_missing_manifest():
    manifest = load_manifest("non_existent.json")
    assert isinstance(manifest, Manifest)
    assert len(manifest.sources) == 0
```

tests/test_reporting.py
```
import json
from pathlib import Path
from src.reporting.report import RunReport, SourceResult

def test_report_lifecycle():
    report = RunReport(run_id="test-run")
    assert report.start_time > 0
    assert report.end_time is None
    
    result = SourceResult(id="s1", status="success", duration=1.5)
    report.record_result(result)
    
    assert report.summary["success"] == 1
    assert report.results["s1"] == result
    
    report.finalize()
    assert report.end_time >= report.start_time

def test_atomic_write(tmp_path):
    report_file = tmp_path / "report.json"
    report = RunReport(run_id="test-run")
    report.record_result(SourceResult(id="s1", status="success", duration=1.0))
    report.finalize()
    
    report.to_json(str(report_file))
    
    assert report_file.exists()
    content = json.loads(report_file.read_text())
    assert content["run_id"] == "test-run"
    assert content["summary"]["success"] == 1
```

tests/test_runner.py
```
import subprocess
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.generator_runner.runner import GeneratorRunner
from src.registry_config.models import Source

@patch("subprocess.run")
def test_runner_success(mock_run, tmp_path):
    runner = GeneratorRunner(output_root=tmp_path)
    source = Source(id="test-src", url="https://github.com/test/repo")
    
    # Mock successful result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Success"
    mock_run.return_value = mock_result
    
    # Create fake artifact
    (tmp_path / "temp_work" / "test-src").mkdir(parents=True)
    (tmp_path / "temp_work" / "test-src" / "test-llms.txt").touch()
    
    result = runner.run_source(source)
    
    assert result["status"] == "success"
    assert "test-llms.txt" in result["artifacts"][0]
    
    # Verify command structure
    args, kwargs = mock_run.call_args
    cmd = args[0]
    assert cmd[0] == "lmstudio-llmstxt"
    assert cmd[1] == "https://github.com/test/repo"
    assert "--output-dir" in cmd
    assert "--stamp" in cmd

@patch("subprocess.run")
def test_runner_failure(mock_run, tmp_path):
    runner = GeneratorRunner(output_root=tmp_path)
    source = Source(id="test-src", url="https://github.com/test/repo")
    
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Error"
    mock_run.return_value = mock_result
    
    result = runner.run_source(source)
    assert result["status"] == "failure"
    assert result["error"] == "Error"

@patch("subprocess.run")
def test_runner_timeout(mock_run, tmp_path):
    runner = GeneratorRunner(output_root=tmp_path)
    source = Source(id="test-src", url="https://github.com/test/repo")
    
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=300)
    
    result = runner.run_source(source)
    assert result["status"] == "failure"
    assert "timed out" in result["error"]
```

.github/workflows/lint.yml
```
name: Lint and Validate

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest

    - name: Run Unit Tests
      run: |
        PYTHONPATH=. pytest tests/

    - name: Validate sources.json
      run: |
        python3 -c "from src.registry_config.loader import load_manifest; load_manifest('sources.json'); print('Manifest valid.')"

    - name: Verify Directory Structure
      run: |
        if [ ! -d "docs" ]; then echo "docs/ directory missing"; exit 1; fi
        if [ ! -d "src" ]; then echo "src/ directory missing"; exit 1; fi
        if [ ! -f "scripts/refresh.py" ]; then echo "refresh script missing"; exit 1; fi
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
        """Execute the lmstudio-llmstxt CLI for a single source."""
        start_time = time.time()
        
        # Determine model
        model = source.last_model_used or (profile.model if profile else None)
        
        # Prepare command
        cmd = ["lmstudio-llmstxt", str(source.url)]
        
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
                    "model_used": model # This might be auto-detected by the tool if not passed
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