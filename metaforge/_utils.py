from typing import Generator
from pathlib import Path

def file_line_generator(file_path: Path) -> Generator[str, None, None]:
  with file_path.open('r') as file:
    line: str
    for line in file:
      yield line
