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
