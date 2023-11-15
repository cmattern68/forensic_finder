from pydantic import BaseModel
from forensic_finder.config import ConfigurationModel


class ProcessParamSchema(BaseModel):
    folders: list
    config: ConfigurationModel

class FinderResult(BaseModel):
    pass