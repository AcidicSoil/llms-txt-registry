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
