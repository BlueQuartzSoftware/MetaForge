from genericpath import exists
from ezmodel.ezmetadataentry import EzMetadataEntry
from ezmodel.ezmetadatamodel import EzMetadataModel
from parsers.ang import parse_header_as_dict

from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests

import json
from typing import List



# Set teh path of the file to store the JSON of the model
ez_file_path = '/Users/mjackson/Desktop/MultiPhase.ez'

# Read the EzMetadataModel from the json file
model = EzMetadataModel.from_json_file(ez_file_path)

# Set the path of the data file to use to build the EzMetadataModel
data_file_path = '/Volumes/970-1/Data/Ang_Data/12_strain/Scan_10074.ang'

# Convert the ANG file into a dictionary
ang_dict = parse_header_as_dict(data_file_path)


# Sync the the EzMetadataModel from the ANG header dictionary
missing_entries: List[EzMetadataEntry] = model.update_model_values_from_dict(ang_dict)
if len(missing_entries) != 0:
  print('Not all values that appear in the Template file were in the input data file.')
  for e in missing_entries:
    print(f'{e.source_path}')


unit_test_model = EzMetadataModel()
# Grab a "Source.FILE" from the ANG model
unit_test_model.append(model.entries[0])

# Override the Source Value and set a new one
entry = model.entries[1]
entry.override_source_value = True
entry.ht_value = "HT Overridden Value"
entry.enabled = True
unit_test_model.append(entry)

# Override the HT_Name with a new one
entry = model.entries[2]
entry.ht_name = "Custom HT Name"
entry.ht_annotation = "Overridden y-star HT Name"
unit_test_model.append(entry)

# Override the HT_Name with a new one
entry = model.entries[3]
entry.ht_name = "Custom HT Name"
entry.ht_value = "HT Overridden Value"
entry.ht_annotation = "Overridden z-star HT Name and Value. Really should be just a 'custom' entry"
unit_test_model.append(entry)

# Create a Custom Entry
custom = EzMetadataEntry()
custom.source_type = EzMetadataEntry.SourceType.CUSTOM
custom.ht_name = "Facility"
custom.ht_value = "BQ"
custom.ht_annotation = "Custom Template Value"
custom.enabled = True
custom.override_source_value = False
unit_test_model.append(custom)


# Write the EzMetadataModel to the json file
unit_test_model.to_json_file(ez_file_path)


# Use the template to upload to HyperThought
# Set your API Access Key which you would get from HyperThought Web site
accessKey = 'eyJhY2Nlc3NUb2tlbiI6ICJkYjg0YTU3MmEwOWI0N2Y1YTM4ODcxZjA3NmZmZDYyOCIsICJyZWZyZXNoVG9rZW4iOiAiZWY0MWVlNzY0NTYyNGY4MWI4MGIzMGQ1ZjhlYzJiNWEiLCAiZXhwaXJlc0luIjogMjU3MiwgImV4cGlyZXNBdCI6ICIyMDIxLTA2LTI0VDE1OjI4OjI2LTA0OjAwIiwgImJhc2VVcmwiOiAiaHR0cHM6Ly9odC5ibHVlcXVhcnR6Lm5ldCIsICJjbGllbnRJZCI6ICIwODc3NjAiLCAiY2xpZW50U2VjcmV0IjogIjJjMzJhYmYyMDBlZGE3MTkxNDQxM2YyYTEwNTE5YmI0YzAzMWZmYjgxOTYwNDQ5OTVlODgxOWVjIn0='
# Create an HtAuthController to hold the API key
auth_control = htauthcontroller.HTAuthorizationController(accessKey)

# Upload to a folder created at the root level of the user's HT home.
path = ","

# Set the remote directory to create. This DOES NOT check if that folder already exists
remoteDirPath = "Unit_Test"

project_json = ht_requests.list_projects(auth_control)

# Just get the first Folder from the projects
folder_json = project_json[1]
project_folder_0_pk = folder_json["content"]["pk"]
project_folder_0_title = folder_json["content"]["title"]

sub_folder_list = ht_requests.get_item_dict_from_ht_path(auth_control, 
              ht_path='/',
              ht_space = 'project',
              ht_space_id=project_folder_0_pk)

folderlist = ht_requests._list_location_contents(auth_control, ht_id_path = path)
for j in folderlist:
  print(j)

remote_exists = False
remote_folder_uuid = ""
print("Checking if remote folder {remoteDirPath} exists")
for f in folderlist:
  if f["content"]["name"] is remoteDirPath:
    remote_exists = True
    remote_folder_uuid = f["content"]["pk"]
    print(f'name: {f["content"]["name"]}  UUID: {f["content"]["pk"]}')
  
if not remote_exists:
  print("Remote Folder does not exist.. creating remote folder {remoteDirPath}")
  remote_folder_uuid = ht_requests.create_folder(auth_control, folder_name = remoteDirPath, ht_id_path= path)

# Extract the Meta-Data from the Template/Model
metadataJson = ht_utilities.ezmodel_to_ht_metadata(unit_test_model)

# Pick your data files to upload
filelist = "/Users/mjackson/Downloads/011.ang"

# Perform the upload.
file_id, file_name = ht_requests.upload_file(auth_control, filelist, 'user', None, "," + remote_folder_uuid + ",", metadataJson)

print("Upload completed")
