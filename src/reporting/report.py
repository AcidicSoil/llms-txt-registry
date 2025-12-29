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