from pathlib import Path
import importlib
from inspect import isclass
from typing import Tuple

from metaforge.parsers.metaforgeparser import MetaForgeParser

def load_parser_module(parser_file_path: Path) -> Tuple[str, MetaForgeParser]:
    spec =importlib.util.spec_from_file_location("parsers", str(parser_file_path))
    parser = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(parser)
    except Exception as ex:
        return str(ex), None

    for attribute_name in dir(parser):
        attribute = getattr(parser, attribute_name)
        if isclass(attribute) and issubclass(attribute, MetaForgeParser) \
           and attribute_name != 'MetaForgeParser':
            try:
                parser = attribute()
            except Exception as ex:
                return str(ex), None
            return None, parser
    
    return "Could not find a valid parser class that inherits from MetaForgeParser.", None