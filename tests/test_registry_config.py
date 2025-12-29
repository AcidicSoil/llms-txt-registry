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
