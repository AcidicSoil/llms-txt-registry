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