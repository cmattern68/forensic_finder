from __future__ import annotations
from typing import Optional, List, Dict
from enum import IntEnum
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from forensic_finder.config import ConfigurationModel
from tabulate import tabulate
from rich import print


class Exif(BaseModel):
    software: Optional[str] = Field(default=None, alias="Software")
    make: Optional[str] = Field(default=None, alias="Make")
    model: Optional[str] = Field(default=None, alias="Model")
    creation_date: Optional[datetime] = Field(default=None, alias="DateTime")

    @field_validator('creation_date', check_fields=False, mode="before")
    def load_ext(cls, v):
        if v is None:
            return None
        try:
            dt = datetime.strptime(v, "%Y:%m:%d %H:%M:%S")
            return dt
        except ValueError as e:
            return None


class ProcessParamSchema(BaseModel):
    folders: list
    config: ConfigurationModel


class RecoveringStatus(IntEnum):
    RECOVERED = 1
    IGNORED = 2
    CORRUPTED = 3
    INFECTED = 4


class RecoveringSchema(BaseModel):
    nb_files_processed: int = 0
    nb_files_recovered: int = 0
    nb_files_ignored: int = 0
    nb_files_corrupted: int = 0
    nb_files_infected: Optional[int] = None

    def __add__(self, other: RecoveringSchema):
        return RecoveringSchema(
            nb_files_processed=self.nb_files_processed + other.nb_files_processed,
            nb_files_recovered=self.nb_files_recovered + other.nb_files_recovered,
            nb_files_ignored=self.nb_files_ignored + other.nb_files_ignored,
            nb_files_corrupted=self.nb_files_corrupted + other.nb_files_corrupted,
            nb_files_infected=(None if self.nb_files_infected is None or other.nb_files_infected is None else (self.nb_files_infected + other.nb_files_infected))
        )

    def add(self, status: RecoveringStatus):
        self.nb_files_processed += 1
        if status == RecoveringStatus.RECOVERED:
            self.nb_files_recovered += 1
        elif status == RecoveringStatus.CORRUPTED:
            self.nb_files_corrupted += 1
        elif status == RecoveringStatus.INFECTED:
            self.nb_files_infected += 1
        else:
            self.nb_files_ignored += 1


class FinderResult(BaseModel):
    total: RecoveringSchema
    details: Dict[str, RecoveringSchema] = {}

    def merge(self, result: FinderResult):
        self.total += result.total
        for result_detail_ext in result.details:
            if result_detail_ext not in self.details:
                self.details[result_detail_ext] = RecoveringSchema()
            self.details[result_detail_ext] += result.details[result_detail_ext]

    def add_result(self, ext: str, status: RecoveringStatus):
        self.total.add(status)
        if ext not in self.details:
            self.details[ext] = RecoveringSchema()
        self.details[ext].add(status)

    def show(self):
        headers = [
            "extension", "files processed", "files recovered", "files ignored", "files corrupted"
        ]
        results = []
        for key, detail in self.details.items():
            results.append(
                [
                    key,
                    detail.nb_files_processed,
                    detail.nb_files_recovered,
                    detail.nb_files_ignored,
                    detail.nb_files_corrupted
                ]
            )
        results.append(
            [
                "total",
                self.total.nb_files_processed,
                self.total.nb_files_recovered,
                self.total.nb_files_ignored,
                self.total.nb_files_corrupted
            ]
        )
        print(tabulate(results, headers=headers, tablefmt='fancy_grid'))