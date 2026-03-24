from typing import List
from ..core import Entry, Relation
from .Lexicon import Lexicon


class Codex:
    def __init__(self, repository: Lexicon):
        self.repository = repository

    def create_entry(self, entry: Entry) -> Entry:
        """
        Caso de Uso: Validar reglas de negocio y persistir.
        Nota: 'entry' ya viene normalizado gracias a su __post_init__.
        """
        # 1. Validación de Regla de Negocio (El título es obligatorio para persistir)
        if not entry.title:
            raise ValueError("El título no puede estar vacío.")

        # 2. Verificación de duplicados en el repositorio (Integridad)
        existing = self.repository.get_by_title(entry.title)
        if existing and existing.id != entry.id:
            raise ValueError(f"Ya existe una página con el título '{entry.title}'.")

        # 3. Persistencia
        self.repository.save(entry)

        return entry

    def create_relation(self, relation: Relation):
        # 2. Validación de Existencia en el Repositorio
        # Seguimos necesitando verificar que los IDs que contiene la relación existan
        origin = self.repository.get_by_id(relation.from_id)
        target = self.repository.get_by_id(relation.to_id)
    
        if not origin or not target:
            raise ValueError("Ambas páginas (origen y destino) deben existir en el Lexicon.")
    
        # 3. Verificación de Duplicados (Opcional pero recomendado)
        if self.repository.check_relation(relation):
            raise ValueError(f"Ya existe una relación de tipo '{relation.connection_type}' entre estos nodos.")
    
        # 4. Persistencia del objeto
        self.repository.save_relation(relation)

    def get_backlinking_entries(self, entry_id: str) -> List[Entry]:
        # 1. Obtenemos todas las relaciones entrantes (una sola consulta)
        relations = self.repository.get_in_relations(entry_id)
        
        if not relations:
            return []

        # 2. Extraemos los IDs de origen de forma única
        # Usamos un set para evitar cargar la misma página dos veces si tuviera dos vínculos
        origin_ids = list({rel.from_id for rel in relations})

        # 3. HIDRATACIÓN EFICIENTE: 
        # Pedimos todas las entradas al repositorio de golpe (una sola consulta)
        return self.repository.get_by_ids(origin_ids)

    def edit_entry(self, entry_id: str, new_content: str) -> Entry:
        """
        Edita el contenido de una entrada existente de forma segura.
        Recibe el ID para garantizar que trabajamos sobre la versión persistida.
        """
        # 1. Recuperamos la versión REAL y COMPLETA del repositorio
        existing_entry = self.repository.get_by_id(entry_id)
        
        if not existing_entry:
            raise ValueError(f"No se puede editar: La entrada con ID '{entry_id}' no existe.")

        # 2. Aplicamos los cambios al objeto que recuperamos del repositorio
        # Esto preserva tags, metadata previa y fecha de creación
        existing_entry.update_content(new_content)

        # 3. Lógica de Metadatos: Auditoría (sobre el objeto real)
        edits = existing_entry.metadata.get("edit_count", 0)
        existing_entry.metadata["edit_count"] = edits + 1

        # 4. Persistencia del objeto actualizado
        self.repository.save(existing_entry)
        
        return existing_entry

    def delete_entry(self, entry_id: str):
        # 1. Verificar existencia (opcional según rendimiento)
        if not entry_id or not isinstance(entry_id, str):
            raise ValueError("Se requiere un ID de entrada válido (string).") # Si no existe, el trabajo ya está hecho

        existing = self.repository.get_by_id(entry_id)
        if not existing:
            raise ValueError(f"No se puede eliminar: La entrada con ID '{entry_id}' no existe.")

        try:
            success = self.repository.delete(entry_id)
            if not success:
            # Caso borde: alguien lo borró justo entre el paso 2 y 3
                raise RuntimeError(f"Error inesperado: No se pudo eliminar la entrada '{entry_id}'.")
        except Exception as e:
        # Aquí capturarías errores de conexión a DB, etc.
            raise RuntimeError(f"Fallo crítico en el repositorio al eliminar '{entry_id}': {str(e)}")

    def disconnect_entries(self, relation: Relation):
        relations_in_entries = self.repository.check_relation(relation)
        if not relations_in_entries:
            raise ValueError(f"No se encontró ninguna relación entre '{relation.from_id}' y '{relation.to_id}'.")
        self.repository.delete_relation(relation)

