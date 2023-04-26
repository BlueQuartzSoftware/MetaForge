from pathlib import Path
import yaml
import importlib
from inspect import isclass

from metaforge.ez_models.ezparserdirectory import EzParserDirectory
from metaforge.parsers.metaforgeparser import MetaForgeParser
from metaforge.common.constants import K_PARSER_YAML_FILE_NAME, K_PARSER_YAML_KEY

def create_parser_directory(parser_folder_path: Path) -> EzParserDirectory:
    yaml_file_path = parser_folder_path / K_PARSER_YAML_FILE_NAME
    if not yaml_file_path.exists():
        # Create skeleton yaml file
        with open(str(yaml_file_path), 'w') as fp:
            fp.write(generate_skeleton_parser_yaml_file())
        return EzParserDirectory(parser_folder_path)

    with yaml_file_path.open("r") as yml:
        yaml_data: dict = yaml.safe_load(yml)
        if K_PARSER_YAML_KEY not in yaml_data or yaml_data[K_PARSER_YAML_KEY] is None:
            return EzParserDirectory(parser_folder_path)
        return EzParserDirectory(parser_folder_path, [parser_folder_path / file_name for file_name in yaml_data[K_PARSER_YAML_KEY]])

def generate_skeleton_parser_yaml_file() -> str:
    return f"---\n# List the relative path to each parser script below.  Some examples are provided.\n{K_PARSER_YAML_KEY}:\n  # - example_parser.py\n  # - /subfolder/example_parser2.py"

def load_parser_module(parser_file_path: Path):
    spec =importlib.util.spec_from_file_location("parsers", str(parser_file_path))
    parser = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(parser)
    except:
        return None

    for attribute_name in dir(parser):
        attribute = getattr(parser, attribute_name)
        if isclass(attribute) and issubclass(attribute, MetaForgeParser) \
           and attribute_name != 'MetaForgeParser':
            return attribute()
    return None