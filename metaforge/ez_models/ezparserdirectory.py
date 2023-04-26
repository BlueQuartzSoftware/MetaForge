from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from pathlib import Path
from typing import List

from metaforge.common.json_encoders import path_encoder, listofpaths_encoder
from metaforge.common.json_decoders import path_decoder, listofpaths_decoder

@dataclass_json
@dataclass
class EzParserDirectory:
    directory_path: Path = field(metadata=config(encoder=path_encoder, decoder=path_decoder))
    parser_paths: List[Path] = field(metadata=config(encoder=listofpaths_encoder, decoder=listofpaths_decoder), default_factory=list)
    default: bool = False
    enabled: bool = True