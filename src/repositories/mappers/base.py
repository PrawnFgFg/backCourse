from pydantic import BaseModel
from typing import TypeVar

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None
    
    
    @classmethod
    def map_to_domain_entithy(self, db_model):
        return self.schema.model_validate(db_model, from_attributes=True)
    
    
    @classmethod
    def map_to_persistence_entity(self, schema):
        return self.db_model(**schema.model_dump())