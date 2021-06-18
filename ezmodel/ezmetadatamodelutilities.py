from ezmodel.ezmetadataentry import EzMetadataEntry
from ezmetadatamodel import EzMetadataModel
from parsers.ang import parse_header_as_dict

# Paths (change these!)
data_file_path = '/Users/joeykleingers/Downloads/011.ang'
json_file_path = '011.json'

# Parse the data file header
model_dict = parse_header_as_dict(data_file_path)

# Create a EzMetadataModel from the header dictionary
model = EzMetadataModel.create_model(model_dict, data_file_path, EzMetadataEntry.SourceType.FILE)

custom0 = EzMetadataEntry()
custom0.source_type = EzMetadataEntry.SourceType.CUSTOM
custom0.ht_name = "Facility"
custom0.ht_value = "BQ"
custom0.enabled = False
model.append(custom0)

print(f'{model.size()}')
print(f'{model.enabled_count()}')

# Write the EzMetadataModel to the json file
model.to_json_file(json_file_path)

# # Read the EzMetadataModel from the json file
reloaded_model = EzMetadataModel.from_json_file(json_file_path)

# # Write the EzMetadataModel to a json string
model_string = reloaded_model.to_json_string()

print(model)