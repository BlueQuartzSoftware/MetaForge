from pathlib import Path
import exifread

def parse_header_as_dict(filepath: Path) -> dict:
  # Open image file for reading (binary mode)
  try:
    f = open(filepath, 'rb')
  except OSError:
    print ("Unable to open/read file: ", filepath.name)
    return None

  tags = exifread.process_file(f, details=False)

  # Print the tag/ value pairs
  meta_dict = {}
  for tag in tags.keys():
    key: str = tag.split(' ', 1)[1]
    value: str = tags[tag].printable

    if '\n' in value or '=' in value:
      value_lines = [x.strip() for x in value.split('\n')]

      for value_line in value_lines:
        key_value = [x.strip() for x in value_line.split('=')]
        if len(key_value) == 2:
          print("\"%s\": \"%s\"" % (key_value[0], key_value[1]))
          meta_dict[key_value[0]] = key_value[1]
    else:
      print("\"%s\": \"%s\"" % (key, value))
      meta_dict[key] = value

  return meta_dict