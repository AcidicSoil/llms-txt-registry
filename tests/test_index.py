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
