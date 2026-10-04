from pydantic import BaseModel, Field
from typing import Optional


class Publication(BaseModel):
    pmid: str
    title: str
    abstract: Optional[str] = None

    authors: list[str] = Field(default_factory=list)

    journal: Optional[str] = None
    publication_year: Optional[int] = None

    doi: Optional[str] = None

    keywords: list[str] = Field(default_factory=list)

    source: str = "PubMed"