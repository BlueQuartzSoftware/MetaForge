from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

@dataclass_json
@dataclass
class EzMetadataEntry:
    class SourceType(Enum):
        FILE = 1
        CUSTOM = 2

    source_path: str = ""
    source_value: str = ""
    ht_name: str = ""
    ht_value: str = ""
    ht_annotation: str = ""
    ht_units: str = ""
    source_type: SourceType = SourceType.FILE
    override_source_value: bool = False
    editable: bool = True
    required: bool = False
    should_extract: bool = True
