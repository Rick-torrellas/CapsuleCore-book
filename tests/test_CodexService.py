import pytest
from unittest.mock import MagicMock

from CapsuleCore_book.capsule.CodexService import CodexService

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return CodexService(repository=mock_repo)

def test_ingest_normalizes_tags(service, mock_repo):
    # Setup
    entry = MagicMock(id="1", tags=["  MAGIC  ", "magic", "SpelL"])
    mock_repo.get_by_id.return_value = None
    
    # Action
    service.ingest(entry)
    
    # Assert: Etiquetas en minúsculas, sin espacios y únicas
    assert entry.tags == ["magic", "spell"]
    mock_repo.save.assert_called_once_with(entry)

def test_ingest_raises_error_if_duplicate(service, mock_repo):
    entry = MagicMock(id="123")
    mock_repo.get_by_id.return_value = entry # Simula que ya existe
    
    with pytest.raises(ValueError, match="Esta página ya existe"):
        service.ingest(entry)

def test_get_incoming_connections(service, mock_repo):
    # Setup: Una relación que viene de 'A' hacia 'B'
    entry_id = "B"
    mock_relation = MagicMock(from_id="A")
    mock_repo.get_backlinks.return_value = [mock_relation]
    
    # Simular que el repo encuentra la entrada 'A'
    entry_a = MagicMock(id="A")
    mock_repo.get_by_id.side_effect = lambda id: entry_a if id == "A" else None
    
    # Action
    results = service.get_incoming_connections(entry_id)
    
    # Assert
    assert len(results) == 1
    assert results[0].id == "A"

def test_create_page_empty_title_raises_error(service):
    with pytest.raises(ValueError, match="título no puede estar vacío"):
        service.create_page(title="   ", content="...")

def test_edit_page_updates_metadata_counter(service, mock_repo):
    # Setup
    entry_id = "42"
    mock_entry = MagicMock(id=entry_id, metadata={"edit_count": 5})
    mock_repo.get_by_id.return_value = mock_entry
    
    # Action
    service.edit_page(entry_id, "Nuevo contenido")
    
    # Assert
    mock_entry.update_content.assert_called_with("Nuevo contenido")
    assert mock_entry.metadata["edit_count"] == 6
    mock_repo.save.assert_called_once()

def test_connect_pages_same_id_raises_error(service):
    with pytest.raises(ValueError, match="consigo misma"):
        service.connect_pages("A", "A", "link")

def test_delete_page_cleans_relations(service, mock_repo):
    # Setup
    entry_id = "ghost_page"
    mock_repo.get_by_id.return_value = MagicMock()
    
    # Action
    service.delete_page(entry_id)
    
    # Assert
    mock_repo.remove_all_relations_to.assert_called_once_with(entry_id)
    mock_repo.delete.assert_called_once_with(entry_id)

