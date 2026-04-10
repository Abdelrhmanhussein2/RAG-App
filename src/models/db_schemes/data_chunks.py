from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DataChunk(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _id: Optional[str] = None
    chunk_text: str = Field(..., min_length=1)
    chunk_order: int = Field(..., ge=0)
    chunk_project_id: str
    chunk_asset_id: str


    class config:
        arbitrary_types_allowed=True

    @classmethod
    def get_indecies(cls):
        return [
            {
                "key": [("chunk_project_id", 1)],
                "name": "chunk_project_id_index",
                "unique": False
            }
        ]