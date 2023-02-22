from __future__ import annotations

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum, unique
from typing import List


@dataclass_json
@dataclass
class EzMetadataEntry:
    unique_id: int = 0
    parent: int = -1
    children: List[int] = field(default_factory=list)

    @unique
    class SourceType(int, Enum):
        FILE = 1
        CUSTOM = 2

    source_path: str = ""
    source_value: str = ""
    ht_name: str = ""
    ht_value: str = ""
    ht_annotation: str = ""
    ht_units: str = ""
    source_type: EzMetadataEntry.SourceType = SourceType.FILE
    override_source_value: bool = False
    editable: bool = True
    required: bool = False
    enabled: bool = True
