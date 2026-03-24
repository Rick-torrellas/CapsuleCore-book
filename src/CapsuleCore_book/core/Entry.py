from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid


@dataclass(kw_only=True)
class Entry:
    content: str
    title: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    # El diccionario de metadatos para flexibilidad total
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Normalizar título: quitar espacios laterales
        if self.title:
            self.title = self.title.strip()
        
        # Normalizar tags: minúsculas, sin espacios y sin duplicados
        if self.tags:
            self.tags = list(set(t.lower().strip() for t in self.tags))

    def update_content(self, new_content: str):
        self.content = new_content
        self.updated_at = datetime.now()
