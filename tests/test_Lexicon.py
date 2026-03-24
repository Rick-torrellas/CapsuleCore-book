from typing import List, Optional
from dataclasses import dataclass
import pytest

from CapsuleCore_book.capsule.Lexicon import Lexicon

@dataclass
class Entry:
    id: str
    content: str
    tags: List[str]

@dataclass
class Relation:
    from_id: str
    to_id: str

class MemoryLexicon(Lexicon):
    def __init__(self):
        self.entries = {}
        self.relations = []

    def save(self, entry: Entry) -> None:
        self.entries[entry.id] = entry

    def get_by_id(self, entry_id: str) -> Optional[Entry]:
        return self.entries.get(entry_id)

    def find_by_tag(self, tag: str) -> List[Entry]:
        return [e for e in self.entries.values() if tag in e.tags]

    def delete(self, entry_id: str) -> bool:
        if entry_id in self.entries:
            del self.entries[entry_id]
            return True
        return False

    def add_relation(self, relation: Relation) -> None:
        self.relations.append(relation)

    def get_backlinks(self, entry_id: str) -> List[Relation]:
        return [r for r in self.relations if r.to_id == entry_id]

    def remove_relation(self, relation: Relation) -> None:
        if relation in self.relations:
            self.relations.remove(relation)


class TestLexicon:
    
    @pytest.fixture
    def lexicon(self):
        """Fixture para obtener una instancia limpia en cada test."""
        return MemoryLexicon()

    def test_save_and_get_by_id(self, lexicon):
        entry = Entry(id="1", content="Hola Mundo", tags=["test"])
        lexicon.save(entry)
        
        result = lexicon.get_by_id("1")
        assert result is not None
        assert result.content == "Hola Mundo"
        assert result.id == "1"

    def test_find_by_tag(self, lexicon):
        e1 = Entry(id="1", content="Uno", tags=["python", "dev"])
        e2 = Entry(id="2", content="Dos", tags=["python"])
        lexicon.save(e1)
        lexicon.save(e2)

        results = lexicon.find_by_tag("python")
        assert len(results) == 2
        
        results_dev = lexicon.find_by_tag("dev")
        assert len(results_dev) == 1
        assert results_dev[0].id == "1"

    def test_delete_entry(self, lexicon):
        entry = Entry(id="del_me", content="Temp", tags=[])
        lexicon.save(entry)
        
        deleted = lexicon.delete("del_me")
        assert deleted is True
        assert lexicon.get_by_id("del_me") is None

    def test_relations_and_backlinks(self, lexicon):
        rel = Relation(from_id="A", to_id="B")
        lexicon.add_relation(rel)
        
        backlinks = lexicon.get_backlinks("B")
        assert len(backlinks) == 1
        assert backlinks[0].from_id == "A"

    def test_remove_relation(self, lexicon):
        rel = Relation(from_id="A", to_id="B")
        lexicon.add_relation(rel)
        lexicon.remove_relation(rel)
        
        assert len(lexicon.get_backlinks("B")) == 0