from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pathlib import Path

from metaforge.common.json_encoders import path_encoder, listofpaths_encoder
from metaforge.common.json_decoders import path_decoder, listofpaths_decoder
from metaforge.parsers.metaforgeparser import MetaForgeParser

@dataclass_json
@dataclass
class EzParser:
  def __init__(self, parser_path, parser):
    self.parser_path: Path = parser_path
    self.parser: MetaForgeParser = parser