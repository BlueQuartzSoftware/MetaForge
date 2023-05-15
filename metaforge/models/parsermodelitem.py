from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from pathlib import Path

from metaforge.common.json_encoders import path_encoder
from metaforge.common.json_decoders import path_decoder
from metaforge.parsers.metaforgeparser import MetaForgeParser

@dataclass_json
@dataclass
class ParserModelItem:
    parser_path: Path = field(metadata=config(encoder=path_encoder, decoder=path_decoder))
    default: bool = False
    enabled: bool = True