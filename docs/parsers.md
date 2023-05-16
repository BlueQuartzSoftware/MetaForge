Adding Parsers
==============

MetaForge supports the addition of new parsers at runtime, the bundled parsers
reuse the same mechanism. The `parsers` subdirectory contains the default bundled
parsers using the naming convention of `format_parser.py`, e.g. `h5_parser.py`.
More parsers can be added from the `File->Preferences` menu.

At a high level you should realize that the parsers using the typing extensions
for Python. This means that the expected types are declared for input and
return values. You should also keep in mind that everything must be output to a
string for the application to display and upload to the server. So the dict is
dict of strings where all keys and values are of the type string, this means
that the parser is responsible for mapping that, including numerics that should
be output as strings.

Developing a Parser
-------------------

When developing a parser you can look at the `example_parser.py` file for a
quick guide with some documentation. This is a good starting point, or if you
want something more concrete the `ini_parser.py` and `h5_parser.py` offer
working examples. All parsers must derive from the `MetaForgeParser` class and
implement several standard methods.

The `self.ext_list` claims the extensions that the parser supports, if you do
not list the file extensions then the parser will not be used to open files
with that extension. The `human_label` is what will be shown in the user
interface to choose the parser, the `version` and `uuid` are used internally.
The functions `supported_file_extensions` and `accepts_extension` are used to
see if a given file can be loaded.

The main method in the parser is the `parse_header_as_dict`. The primary role
of this method is to read the file and create a Python dict that will be passed
to the user interface so that templates can be developed to ingest metadata.
This is the primary entrypoint to the parser and what it returns should be
consistent given the same inputs.

Depending on the parser this might be a very simple mapping, or involve some
degree of interpretation in order to map what the file format contains to a
consistent dictionary. You will often start with an empty dictionary and
build it up iteratively as the file contents are interpreted. If using helper
methods to separate out different elements of the metadata it might be best
achieved by making the dict a member variable initialized to an empty dict.

```python
def __init__(self) -> None:
  self.ext_list: list = ('.h5')
  self.file_dict: object = {}
```

For some formats you might then process them line-by-line, use a Python module
that can already process the format and output a dict, or implement something
like a visitor pattern to walk a tree. Once you are done parsing the metadata
the dict should be returned.

```python
def parse_header_as_dict(self, filepath: Path) -> dict:
  # Do some thing to create your dict here...
  return self.file_dict
```

Exposing Trees in Metadata
--------------------------

A lot of metadata uses trees to expose and group related data. This is
represented in a directory like notation in the key name, with a recently
established convention to use the `.attrs` suffix to represent attributes. This
results in the interface displaying a tree structure on the left, and the right
has shows the key as "Source" and the value as "Source Value". These can then
be mapped by templates to the desired key names. So the path `mydata` would have
a `mydata.attrs` prefix for attributes on the `mydata` node.

The existing formats expose strings as strings, map single numeric values to
numeric values, and small arrays using the `[1, 2, 3, 4]` notation commonly
used by Python to output arrays to strings/terminals. The maximum length of 16
numbers in an array accommodates anything up to and including a 4x4 array
commonly used in an array of metadata.

Summary
-------

Simple formats can be added with just a few lines of code and the import of an
existing library capable of reading the metadata of interest. The main goal is
to summarize all useful metadata and avoid loading any of the large data where
possible. This will make the parser operate more quickly in the case of mixed
formats containing large binary data with metadata embedded such as TIFFs,
HDF5 files, and an array of microscope data files.
