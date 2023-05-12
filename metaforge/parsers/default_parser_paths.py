from metaforge.common.constants import K_METAFORGE_PKG_ROOT

K_DEFAULT_PARSERS_DIR_PATH = K_METAFORGE_PKG_ROOT / 'parsers'

K_DEFAULT_PARSER_PATHS = [
    K_DEFAULT_PARSERS_DIR_PATH / 'ang_parser.py',
    K_DEFAULT_PARSERS_DIR_PATH / 'ctf_parser.py',
    K_DEFAULT_PARSERS_DIR_PATH / 'fei_tiff_parser.py',
    K_DEFAULT_PARSERS_DIR_PATH / 'h5_parser.py',
    K_DEFAULT_PARSERS_DIR_PATH / 'ini_parser.py',
    K_DEFAULT_PARSERS_DIR_PATH / 'json_parser.py',
    K_DEFAULT_PARSERS_DIR_PATH / 'xml_parser.py',
]