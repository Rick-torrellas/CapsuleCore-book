from dataclasses import field
from typing import Dict, Any
from dataclasses import dataclass
  

@dataclass
class Relation:
    from_id: str
    to_id: str
    connection_type: str = "relation" 
    metadata: Dict[str, Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.from_id or not self.to_id:
            raise ValueError("Una relación debe tener definidos ambos IDs (origen y destino).")

        if self.from_id == self.to_id:
            raise ValueError("Relación circular no permitida en el modelo.")
