from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from forensic_finder.config import ConfigurationModel
from forensic_finder.lib.utils import transform_datetime


class Exif(BaseModel):
    software: Optional[str] = Field(default=None, alias="Software")
    make: Optional[str] = Field(default=None, alias="Make")
    model: Optional[str] = Field(default=None, alias="Model")
    datetime: Optional[str] = Field(default=None, alias="DateTime")


class ProcessParamSchema(BaseModel):
    folders: list
    config: ConfigurationModel


class FinderResult(BaseModel):
    pass
