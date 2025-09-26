import hashlib
import secrets
from typing import Any, Dict, List, Union

def generate_random_string(length: int = 32) -> str:
    """Generate a random string of specified length."""
    return secrets.token_hex(length // 2)

def mask_string(s: str, show_first: int = 2, show_last: int = 2) -> str:
    """Mask a string for privacy, showing only first and last few characters."""
    if len(s) <= show_first + show_last:
        return "*" * len(s)
    
    return s[:show_first] + "*" * (len(s) - show_first - show_last) + s[-show_last:]

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary."""
    items: List[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)