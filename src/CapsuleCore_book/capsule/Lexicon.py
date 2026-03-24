from abc import ABC, abstractmethod

from ..core import Entry, Relation
from typing import List, Optional


class Lexicon(ABC):
    @abstractmethod
    def save(self, entry: Entry) -> None:
        """Guarda una entrada en el repositorio."""
        pass

    @abstractmethod
    def save_relation(self, relation: Relation) -> None:
        # guarda una relacion 
        pass

    @abstractmethod
    def get_in_relations(self, entry_id: str) -> List[Relation]:
        """Retorna todas las relaciones donde 'to_id' es el ID proporcionado."""
        pass

    @abstractmethod
    def get_out_relations(self, entry_id: str) -> List[Relation]:
        """Retorna todas las relaciones donde 'from_id' es el ID proporcionado."""
        pass

    @abstractmethod
    def get_by_title(self, title: str) -> Optional[Entry]:
        """Busca una entrada exactamente por su título."""
        pass

    @abstractmethod
    def get_by_id(self, entry_id: str) -> Optional[Entry]:
        """Busca una entrada por su ID."""
        pass

    @abstractmethod
    def get_by_ids(self, entry_ids: List[str]) -> List[Entry]:
        """Recupera múltiples entradas de forma eficiente en una sola consulta."""
        pass

    @abstractmethod
    def get_by_tag(self, tag: str) -> List[Entry]:
        """Retorna todas las entradas que contienen el tag proporcionado."""
        pass

    @abstractmethod
    def delete_relation(self,relation: Relation)-> bool:
        """elimina una relimacion especifica"""
        pass

    def delete(self, entry_id: str) -> bool:
        """
        Elimina de forma atómica:
        1. Todas las relaciones donde from_id == entry_id.
        2. Todas las relaciones donde to_id == entry_id.
        3. El objeto Entry con dicho ID.
        Retorna True si se eliminó algo, False si no existía.
        """
    pass
        
    @abstractmethod
    def check_relation(self, relation: Relation) -> bool:
        """Verifica si existe una relación específica."""
        pass


