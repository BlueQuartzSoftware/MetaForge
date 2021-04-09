from enum import Enum
import os
import platform
import urllib3

import requests

from . import ht_requests_errors as ht_rerrors

PATH_SEPERATOR = '/'
ID_ROOT_PATH = ','
ID_PATH_SEPARATOR = ','
MAX_ERROR_CODE = 300

# Disable insecure request warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ItemType(Enum):
    """
    Enum describing types of file system items
    """
    folders = 1
    folders_and_files = 2


def list_location_contents(auth_control, ht_space='user',
                           ht_space_id=None, ht_id_path=ID_ROOT_PATH,
                           item_type=ItemType.folders_and_files):
    """
    Return file and folder items from a location in HyperThought.

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info
        needed to call the HyperThought endpoint.
    ht_space
        The space type that you would like to use in HyperThought.
        This must be set to 'group', 'project', or 'user'.
    ht_space_id
        The id of a group or project, or the username for a user.
        If the value is None, it will default to the current user's
        username.
    ht_id_path
        The path to the location inside a given space in HyperThought.

        Example: a path for '/folder1/folder2/folder3' would look like
        ',folder1_uuid,folder2_uuid,folder3_uuid,'
    item_type
        An enum value for the type of file system items to return.
        A None value will default to ItemType.folders_and_files.

    Returns
    -------
    List
        A list of file system items, represented as dicts, from
        HyperThought corresponding to files and folders at the given
        HyperThought path in the given space.
    """

    # Set default space_id parameter
    if ht_space == 'user' and ht_space_id is None:
        ht_space_id = auth_control.get_username()

    # Validate parameters.
    _validate_parameters(ht_space=ht_space, ht_space_id=ht_space_id,
                         ht_id_path=ht_id_path, item_type=item_type)

    # Build the request URL
    files_url = f'{auth_control.base_url}/api/files/'

    # Gather other data needed for the request
    auth_header = auth_control.get_auth_header()
    cookies = auth_control.cookies
    request_data = {'path': ht_id_path}

    if item_type == ItemType.folders:
        request_data['type'] = 'Folder'

    if ht_space == 'user':
        request_data['method'] = 'user_files'
    elif ht_space == 'project':
        request_data['method'] = 'project_files'
        request_data['project'] = ht_space_id
    else:
        request_data['method'] = 'group_files'
        request_data['group'] = ht_space_id

    # Send the request to HyperThought
    r = requests.get(files_url, headers=auth_header, cookies=cookies,
                     params=request_data, verify=False)

    # Report any errors that are above the max error code
    if r.status_code >= MAX_ERROR_CODE:
        ht_rerrors.report_error(r)

    output = r.json()
    return output


def list_projects(auth_control):
    """
    List projects that the currently logged in user can access in HyperThought.

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info
        needed to call the HyperThought endpoint.

    Returns
    -------
    List
        A list of projects with their metadata and other details, represented
        as dicts
    """

    # Build the request URL
    url = f'{auth_control.base_url}/api/projects/project/'

    cookies = auth_control.cookies
    auth_header = auth_control.get_auth_header()

    # Send the request to HyperThought
    response = requests.get(url, headers=auth_header,
                            cookies=cookies, verify=False)

    # Report any errors that are above the max error code
    if response.status_code >= MAX_ERROR_CODE:
        ht_rerrors.report_error(response=response)

    response_json = response.json()
    return response_json


def create_folder(auth_control, folder_name, ht_space='user', ht_space_id=None,
                  ht_id_path=ID_ROOT_PATH, metadata=None):
    """
    Create a folder in HyperThought.

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info
        needed to call the HyperThought endpoint.
    folder_name
        The name of the folder that you want to create.
    ht_space
        The space type that you would like to use in HyperThought.
        This must be set to 'group', 'project', or 'user'.
    ht_space_id
        The id of a group or project, or the username for a user.
        If the value is None, it will default to the current user's
        username.
    ht_id_path
        The path to the location inside a given space in HyperThought.

        Example: a path for '/folder1/folder2/folder3' would look like
        ',folder1_uuid,folder2_uuid,folder3_uuid,'
    metadata
        The metadata for the folder, which will be attached to the new folder
        in HyperThought.

    Returns
    -------
    The id of the new folder.
    """

    # Set default space_id parameter
    if ht_space == 'user' and ht_space_id is None:
        ht_space_id = auth_control.get_username()

    # Validate parameters
    _validate_parameters(name=folder_name, ht_space=ht_space,
                         ht_space_id=ht_space_id, ht_id_path=ht_id_path,
                         metadata=metadata)

    # Build the request URL
    url = f'{auth_control.base_url}/api/files/create-folder/'

    # Gather other data needed for the request
    request_data = {
        'space': ht_space,
        'space_id': ht_space_id,
        'path': ht_id_path,
        'name': folder_name,
        'metadata': metadata,
    }

    cookies = auth_control.cookies
    auth_header = auth_control.get_auth_header()

    # Send the request to HyperThought
    response = requests.post(url, headers=auth_header, cookies=cookies,
                             json=request_data, verify=False)

    # Report any errors that are above the max error code
    if response.status_code >= MAX_ERROR_CODE:
        ht_rerrors.report_error(response=response)

    response_json = response.json()
    folder_id = response_json['document']['content']['pk']
    return folder_id


def upload_file(auth_control, local_path, ht_space='user', ht_space_id=None,
                ht_id_path=ID_ROOT_PATH, metadata=None):
    """
    Upload a file to HyperThought.

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info needed to call
        the HyperThought endpoint.
    local_path
        The path to a file on the local file system.
    ht_space
        The space type that you would like to use in HyperThought.
        This must be set to 'group', 'project', or 'user'.
    ht_space_id
        The id of a group or project, or the username for a user.
        If the value is None, it will default to the current user's
        username.
    ht_id_path
        The path to the location inside a given space in HyperThought.

        Example: a path for '/folder1/folder2/folder3' would look like
        ',folder1_uuid,folder2_uuid,folder3_uuid,'
    metadata
        The metadata for the file, which will be attached to the file
        in HyperThought.

    Returns
    -------
    Tuple
        A tuple that contains the file id and the file name.
    """

    # Set default space_id parameter
    if ht_space == 'user' and ht_space_id is None:
        ht_space_id = auth_control.get_username()

    # Validate the parameters.
    _validate_parameters(local_path=local_path, ht_space=ht_space,
                         ht_space_id=ht_space_id, ht_id_path=ht_id_path,
                         metadata=metadata)

    # Create an upload URL and then upload the file.
    active_local_path = _get_active_path(local_path)
    name = active_local_path.split(os.path.sep)[-1]
    size = os.path.getsize(active_local_path)

    url, file_id = _create_upload_url(auth_control,
                                      ht_space=ht_space,
                                      ht_space_id=ht_space_id,
                                      name=name,
                                      size=size,
                                      ht_id_path=ht_id_path,
                                      metadata=metadata)

    _upload_file(auth_control, url, active_local_path)

    file_name = _finalize_upload(auth_control, file_id)

    # Return the file id and file name
    return (file_id, file_name)


def _create_upload_url(auth_control, name, size, ht_space='user',
                       ht_space_id=None, ht_id_path=ID_ROOT_PATH,
                       metadata=None):
    """
    Create an upload URL to use to upload a file.

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info needed to call
        the HyperThought endpoint.
    name
        The name of the file.
    size
        The size of the file in bytes.
    ht_space
        The space type that you would like to use in HyperThought.
        This must be set to 'group', 'project', or 'user'.
    ht_space_id
        The id of a group or project, or the username for a user.
        If the value is None, it will default to the current user's
        username.
    ht_id_path
        The path to the location inside a given space in HyperThought.

        Example: a path for '/folder1/folder2/folder3' would look like
        ',folder1_uuid,folder2_uuid,folder3_uuid,'
    metadata
        The metadata for the file, which will be attached to the file
        in HyperThought.

    Returns
    -------
    Tuple
        A tuple containing the url to use to upload the file, and the file id
        for the file to be uploaded.
    """

    # Set default space_id parameter
    if ht_space == 'user' and ht_space_id is None:
        ht_space_id = auth_control.get_username()

    # Validate the parameters.
    _validate_parameters(ht_space=ht_space, ht_space_id=ht_space_id,
                         ht_id_path=ht_id_path, metadata=metadata)

    # Gather other data needed for the request
    url = f'{auth_control.base_url}/api/files/generate-upload-url/'

    auth_header = auth_control.get_auth_header()
    cookies = auth_control.cookies

    request_data = {
        'space': ht_space,
        'space_id': ht_space_id,
        'path': ht_id_path,
        'name': name,
        'size': size,
        'metadata': metadata,
    }

    # Send the request to HyperThought
    response = requests.post(url, headers=auth_header, cookies=cookies,
                             json=request_data, verify=False)

    # Report any errors that are above the max error code
    if response.status_code >= MAX_ERROR_CODE:
        ht_rerrors.report_error(response)

    # Grab URL and file id from response
    response_json = response.json()
    url = response_json['url']
    file_id = response_json['fileId']

    # Prepend the base URL to the front of the URL, if needed
    if not url.startswith(auth_control.base_url):
        if not url.startswith('/'):
            url = f'/{url}'
        url = f'{auth_control.base_url}{url}'

    return url, file_id


def _upload_file(auth_control, upload_url, local_path):
    """
    Upload the given file from local_path using the given upload url.

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info needed to call
        the HyperThought endpoint.
    upload_url
        The url to which the file should be uploaded.
    local_path
        The local path to the file to be uploaded.

    Returns
    -------
    None
    """

    # Validate the parameters.
    _validate_parameters(ht_url=upload_url, local_path=local_path)

    # Gather other data needed for the request
    with open(local_path, 'rb') as file_handle:
        byte_data = file_handle.read()

    request_data = {
        'url': upload_url,
        'data': byte_data,
        'verify': False,
        'cookies': auth_control.cookies,
        'headers': auth_control.get_auth_header()
    }

    file_name = local_path.strip(PATH_SEPERATOR).split(PATH_SEPERATOR)[-1]
    c_disp_str = f"inline;filename={file_name}"
    request_data['headers']['Content-Disposition'] = c_disp_str

    # Send the request to HyperThought
    response = requests.put(**request_data)

    # Report any errors that are above the max error code
    if response.status_code >= MAX_ERROR_CODE:
        ht_rerrors.report_error(response)


def _finalize_upload(auth_control, file_id):
    """
    Finalize the upload by converting the file from temporary (invisible) to
    permanent (visible).

    NOTE: The file should be completely uploaded before executing this method!

    Parameters
    ----------
    auth_control
        HTAuthorizationController object used to get all the info needed to call
        the HyperThought endpoint.
    file_id
        The file id in HyperThought.

    Returns
    -------
    String
        The file name that was converted from temporary to permanent.
    """

    # Build up the request URL
    base_url = auth_control.base_url.rstrip('/')
    update_url = '{}/api/files/temp-to-perm/'.format(base_url)

    # Gather other data needed for the request
    headers = auth_control.get_auth_header()
    cookies = auth_control.cookies
    request_data = {'file_ids': [file_id]}

    # Send the request to HyperThought
    response = requests.patch(update_url, headers=headers, cookies=cookies,
                              json=request_data, verify=False)

    # Report any errors that are above the max error code
    if response.status_code >= MAX_ERROR_CODE:
        ht_rerrors.report_error(response)

    # Retrieve the file name from the response
    file_name = None
    response_json = response.json()

    updated_files = response_json['updated']
    if file_id in updated_files:
        file_name = updated_files[file_id]

    return file_name


def _validate_metadata(metadata):
    """
    Check the given metadata to make sure it is the proper type
    and has the expected content.

    Parameters
    ----------
    metadata
        The metadata attached to a file/folder in HyperThought.

        1. Must be convertable to a list, each list item convertable to a dict.
        2. Each list item must include the keys 'keyName' and 'value'
        3. The 'value' key must have 'type' and 'link' subkeys.
        4. The 'type' subkey must have a value of either 'string' or 'link'.
        5. 'unit' and 'annotation' keys are optional.
        6. No other keys are allowed.

    Returns
    -------
    None
    """

    try:
        metadata = list(metadata)
    except TypeError:
        raise TypeError('METADATA INVALID: Metadata must ' +
                        'be convertable into a list.')

    for meta_item in metadata:
        try:
            dict(meta_item)
        except TypeError:
            raise TypeError('METADATA INVALID: Metadata item ' +
                            'must be convertable into a dict.')

        key_name_str = 'keyName'
        if key_name_str not in meta_item:
            raise ValueError("METADATA INVALID: Metadata item must include " +
                             f"a key named '{key_name_str}'.")

        value_str = 'value'
        if value_str not in meta_item:
            raise ValueError("METADATA INVALID: Metadata item must include " +
                             f"a key named '{value_str}'.")

        type_str = 'type'
        if type_str not in meta_item[value_str]:
            raise ValueError("METADATA INVALID: Metadata item must include a " +
                             f"key named '{value_str}' with a subkey named " +
                             f"'{type_str}'.")

        link_str = 'link'
        str_str = 'string'
        valid_types = (link_str, str_str)
        if meta_item[value_str][type_str] not in valid_types:
            raise ValueError(f"METADATA INVALID:  Item ['{value_str}']" +
                             f"['{type_str}'] must be one of '{link_str}, " +
                             f"{str_str}'.")

        if link_str not in meta_item[value_str]:
            raise ValueError("METADATA INVALID:  Metadata item must have a " +
                             f"key {value_str} with subkey '{link_str}'.")

        unit_str = 'unit'
        ann_str = 'annotation'
        valid_keys = {key_name_str, value_str, unit_str, ann_str}

        meta_item_keys = set(meta_item.keys())
        invalid_keys = meta_item_keys - valid_keys

        if invalid_keys:
            invalid_keys_str = ', '.join(invalid_keys)
            raise ValueError("METADATA INVALID:  Invalid keys for metadata " +
                             f"item {invalid_keys_str}.")


def _validate_parameters(name=None, ht_space=None, ht_space_id=None,
                         ht_id_path=None, metadata=None, ht_url=None,
                         local_path=None, item_type=None):
    """
    Check the given parameters to make sure they are the proper types
    and have the expected content.

    Parameters
    ----------
    name
        The name of a file/folder in HyperThought.

        Must be a string.
    ht_space
        A HyperThought space type.

        Must have a value of either 'group', 'project', or 'user'.
    ht_space_id
        The id of a group or project, or the username for a user.

        Must be a string.
    ht_id_path
        The path to the location inside a given space in HyperThought.

        Must be a string, and start and end with a comma.
    metadata
        The metadata attached to a file/folder in HyperThought.

        1. Must be convertable to a list, each list item convertable to a dict.
        2. Each list item must include the keys 'keyName' and 'value'
        3. The 'value' key must have 'type' and 'link' subkeys.
        4. The 'type' subkey must have a value of either 'string' or 'link'.
        5. 'unit' and 'annotation' keys are optional.
        6. No other keys are allowed.
    ht_url
        The url to a HyperThought endpoint.

        Must be a string.
    local_path
        The local path to a file on the file system.

        Must be a string, and the path must exist.

    item_type
        An enum value for the type of file system item.

        Must be an instance of ItemType.

    Returns
    -------
    None
    """

    # Validate name
    if name is not None:
        assert isinstance(name, str)

    # Validate space
    if ht_space is not None:
        assert ht_space in ('group', 'project', 'user')

    # Validate space_id
    if ht_space_id is not None:
        assert isinstance(ht_space_id, str)

    # Validate path
    if ht_id_path is not None:
        assert isinstance(ht_id_path, str)
        assert ht_id_path.startswith(ID_PATH_SEPARATOR)
        assert ht_id_path.endswith(ID_PATH_SEPARATOR)

    if metadata is not None:
        _validate_metadata(metadata)

    if ht_url is not None:
        assert isinstance(ht_url, str)

    if local_path is not None:
        assert isinstance(local_path, str)
        assert os.path.exists(local_path)

    if item_type is not None:
        assert isinstance(item_type, ItemType)


def _get_active_path(path):
    """Get the active path.

    Parameters
    ----------
    path
        A local file system path.

    Returns
    -------
    String
        The active path.
    """

    if platform.system() != 'Windows':
        return path

    windows_path_prefix = '//?/'
    path = path.lstrip(windows_path_prefix)
    return f'{windows_path_prefix}{path}'.replace(PATH_SEPERATOR, os.path.sep)
