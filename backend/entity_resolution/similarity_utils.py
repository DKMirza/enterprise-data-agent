"""
Similarity utility functions for entity resolution.
Provides various string matching algorithms and normalization techniques.
"""

from typing import List, Tuple, Union, Dict, Optional, Set
import re
import math
from difflib import SequenceMatcher


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def levenshtein_similarity(s1: str, s2: str) -> float:
    """Calculate similarity ratio based on Levenshtein distance (0.0 to 1.0)."""
    if not s1 or not s2:
        return 0.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein_distance(s1.lower(), s2.lower())
    return 1.0 - (distance / max_len)


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets of tokens."""
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def tokenize(text: str) -> Set[str]:
    """Tokenize text into lowercase words."""
    if not text:
        return set()
    # Split on non-alphanumeric characters and filter empty strings
    tokens = re.findall(r'\b[a-zA-Z0-9]+\b', str(text).lower())
    return set(tokens)


def jaccard_string_similarity(s1: str, s2: str) -> float:
    """Calculate Jaccard similarity between two strings based on token sets."""
    tokens1 = tokenize(s1)
    tokens2 = tokenize(s2)
    return jaccard_similarity(tokens1, tokens2)


def ngram_similarity(s1: str, s2: str, n: int = 2) -> float:
    """Calculate similarity based on n-gram overlap."""
    if not s1 or not s2:
        return 0.0
    
    def get_ngrams(text: str, n: int) -> Set[tuple]:
        text = text.lower().replace(' ', '')
        return set(zip(*[text[i:] for i in range(n)]))
    
    ngrams1 = get_ngrams(s1, n)
    ngrams2 = get_ngrams(s2, n)
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    return intersection / union if union > 0 else 0.0


def soundex(name: str) -> str:
    """Generate Soundex code for a name (phonetic matching)."""
    if not name:
        return ""
    
    name = name.upper()
    first_letter = name[0]
    
    # Map letters to digits based on phonetic similarity
    soundex_map = {
        'BFPV': '1', 'CGJKQSXZ': '2', 'DT': '3', 
        'L': '4', 'MN': '5', 'R': '6'
    }
    
    # Convert to Soundex code
    result = [first_letter]
    last_code = None
    
    for char in name[1:]:
        code = None
        for pattern, digit in soundex_map.items():
            if char in pattern:
                code = digit
                break
        
        if code and code != last_code:
            result.append(code)
        
        last_code = code
    
    # Pad or truncate to 4 characters
    return (result + ['0'] * 3)[:4]


def soundex_similarity(name1: str, name2: str) -> float:
    """Compare two names using Soundex algorithm."""
    if not name1 or not name2:
        return 0.0
    
    code1 = soundex(name1)
    code2 = soundex(name2)
    
    # Exact match = 1.0, partial match based on character similarity
    if code1 == code2:
        return 1.0
    
    # Calculate character-level similarity for partial matches
    matches = sum(1 for c1, c2 in zip(code1, code2) if c1 == c2)
    return matches / 4


def extract_domain(email: str) -> str:
    """Extract domain from email address."""
    if not email or '@' not in str(email):
        return ""
    return str(email).split('@')[-1].lower().strip()


def normalize_phone(phone: str) -> str:
    """Normalize phone number to digits only."""
    if not phone:
        return ""
    # Remove all non-digit characters
    return re.sub(r'\D', '', str(phone))


def normalize_company_name(name: str) -> str:
    """Normalize company name for comparison."""
    if not name:
        return ""
    
    # Convert to lowercase
    normalized = str(name).lower().strip()
    
    # Remove common business suffixes
    patterns = [
        r'\b(corp|corporation|incorporated|inc\.?|llc|l\.l\.c\.?|ltd|limited|co\.?|company)\b',
        r'\s+',  # Multiple spaces to single space
        r'^\s+|\s+$'  # Leading/trailing whitespace
    ]
    
    for pattern in patterns:
        normalized = re.sub(pattern, '', normalized)
    
    return normalized.strip()


def safe_string(value) -> str:
    """Safely convert any value to string."""
    if value is None:
        return ""
    if isinstance(value, float):
        import math
        if math.isnan(value):
            return ""
    return str(value).strip()
