"""Entity Resolution module for AI-powered record linkage."""

from .entity_resolver import EntityResolver, resolve_entities_quick
from .similarity_utils import (
    levenshtein_similarity,
    jaccard_string_similarity,
    soundex_similarity,
    normalize_company_name,
    safe_string,
    extract_domain,
    normalize_phone
)

__all__ = [
    'EntityResolver',
    'resolve_entities_quick',
    'levenshtein_similarity',
    'jaccard_string_similarity', 
    'soundex_similarity',
    'normalize_company_name',
    'safe_string',
    'extract_domain',
    'normalize_phone'
]
