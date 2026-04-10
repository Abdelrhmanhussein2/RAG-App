from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class asset(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id: str = Field(..., min_length=1)
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(..., ge=0)
    asset_pushed_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def get_indecies(cls):
        return [
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_index",
                "unique": False
            }
        ]