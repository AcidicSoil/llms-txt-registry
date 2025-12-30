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