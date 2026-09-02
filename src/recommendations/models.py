from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Recommendation:
    finding_id: str
    suggested_action: Dict[str, Any]
