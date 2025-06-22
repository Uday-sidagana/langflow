import json
from typing import Any

from composio import Action

from langflow.base.composio.composio_base import ComposioBaseComponent
from langflow.inputs import (
    BoolInput,
    IntInput,
    MessageTextInput,
)
from langflow.logging import logger


class ComposioGoogleDriveAPIComponent(ComposioBaseComponent):
    display_name: str = "GoogleDrive"
    description: str = "GOOGLEDRIVE API"
    icon = "GoogleDrive"
    documentation: str = "https://docs.composio.dev"
    app_name = "googledrive"
    
    _actions_data: dict = {"GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE": {
      "display_name": "Add File Sharing Preference",
      "action_fields": [
        "GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_domain",
        "GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_email_address",
        "GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_file_id",
        "GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_role",
        "GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_type"
      ],
      
    },
    "GOOGLEDRIVE_COPY_FILE": {
      "display_name": "Copy File",
      "action_fields": [
        "GOOGLEDRIVE_COPY_FILE_file_id",
        "GOOGLEDRIVE_COPY_FILE_new_title"
      ]
    },
    "GOOGLEDRIVE_CREATE_FILE_FROM_TEXT": {
      "display_name": "Create A File From Text",
      "action_fields": [
        "GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_file_name",
        "GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_mime_type",
        "GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_parent_id",
        "GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_text_content"
      ]
    },
    "GOOGLEDRIVE_CREATE_FOLDER": {
      "display_name": "Create A Folder",
      "action_fields": [
        "GOOGLEDRIVE_CREATE_FOLDER_folder_name",
        "GOOGLEDRIVE_CREATE_FOLDER_parent_id"
      ]
    },
    "GOOGLEDRIVE_DELETE_FOLDER_OR_FILE": {
      "display_name": "Delete Folder Or File",
      "action_fields": [
        "GOOGLEDRIVE_DELETE_FOLDER_OR_FILE_file_id"
      ]
    },
    "GOOGLEDRIVE_DOWNLOAD_FILE": {
      "display_name": "Download A File From Google Drive",
      "action_fields": [
        "GOOGLEDRIVE_DOWNLOAD_FILE_file_id",
        "GOOGLEDRIVE_DOWNLOAD_FILE_mime_type"
      ],
    },
    "GOOGLEDRIVE_EDIT_FILE": {
      "display_name": "Edit File",
      "action_fields": [
        "GOOGLEDRIVE_EDIT_FILE_content",
        "GOOGLEDRIVE_EDIT_FILE_file_id",
        "GOOGLEDRIVE_EDIT_FILE_mime_type"
      ],
      "get_result_field": True,
      "result_field": "data",
    },
    "GOOGLEDRIVE_FIND_FILE": {
      "display_name": "Find Files",
      "action_fields": [
        "GOOGLEDRIVE_FIND_FILE_folder_id",
        "GOOGLEDRIVE_FIND_FILE_full_text_contains",
        "GOOGLEDRIVE_FIND_FILE_full_text_not_contains",
        "GOOGLEDRIVE_FIND_FILE_include_items_from_all_drives",
        "GOOGLEDRIVE_FIND_FILE_mime_type",
        "GOOGLEDRIVE_FIND_FILE_modified_after",
        "GOOGLEDRIVE_FIND_FILE_name_contains",
        "GOOGLEDRIVE_FIND_FILE_name_exact",
        "GOOGLEDRIVE_FIND_FILE_name_not_contains",
        "GOOGLEDRIVE_FIND_FILE_page_size",
        "GOOGLEDRIVE_FIND_FILE_page_token",
        "GOOGLEDRIVE_FIND_FILE_starred",
        "GOOGLEDRIVE_FIND_FILE_supports_all_drives"
      ],
       "get_result_field": True,
      "result_field": "files",
    },
    "GOOGLEDRIVE_FIND_FOLDER": {
      "display_name": "Find Folder",
      "action_fields": [
        "GOOGLEDRIVE_FIND_FOLDER_full_text_contains",
        "GOOGLEDRIVE_FIND_FOLDER_full_text_not_contains",
        "GOOGLEDRIVE_FIND_FOLDER_modified_after",
        "GOOGLEDRIVE_FIND_FOLDER_name_contains",
        "GOOGLEDRIVE_FIND_FOLDER_name_exact",
        "GOOGLEDRIVE_FIND_FOLDER_name_not_contains",
        "GOOGLEDRIVE_FIND_FOLDER_starred"
      ],
      "get_result_field": True,
      "result_field": "folders",
    },
    "GOOGLEDRIVE_PARSE_FILE": {
      "display_name": "Export Or Download A File",
      "action_fields": [
        "GOOGLEDRIVE_PARSE_FILE_file_id",
        "GOOGLEDRIVE_PARSE_FILE_mime_type"
      ]
    }
    }
    
    _all_fields = {field for action_data in _actions_data.values() for field in action_data["action_fields"]}
    
    _bool_variables = {
        "GOOGLEDRIVE_FIND_FILE_include_items_from_all_drives",
        "GOOGLEDRIVE_FIND_FILE_starred",
        "GOOGLEDRIVE_FIND_FILE_supports_all_drives",
        "GOOGLEDRIVE_FIND_FOLDER_starred",
    }
    
    inputs = [
        *ComposioBaseComponent._base_inputs,
        MessageTextInput(
        name="GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_domain",
        display_name="Domain",
        info="Domain to grant permission to (e.g., 'example.com'). Required if 'type' is 'domain'.",
        show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_email_address",
            display_name="Email Address",
            info="Email address of the user or group. Required if 'type' is 'user' or 'group'.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_file_id",
            display_name="File Id",
            info="Unique identifier of the file to update sharing settings for.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_role",
            display_name="Role",
            info="Permission role to grant.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE_type",
            display_name="Type",
            info="Type of grantee for the permission.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_COPY_FILE_file_id",
            display_name="File Id",
            info="The unique identifier for the file on Google Drive that you want to copy. This ID can be retrieved from the file's shareable link or via other Google Drive API calls.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_COPY_FILE_new_title",
            display_name="New Title",
            info="The title to assign to the new copy of the file. If not provided, the copied file will have the same title as the original, prefixed with 'Copy of '.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_file_name",
            display_name="File Name",
            info="Desired name for the new file on Google Drive.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_mime_type",
            display_name="Mime Type",
            info="MIME type for the new file, determining how Google Drive interprets its content.",
            show=False,
            value="text/plain",
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_parent_id",
            display_name="Parent Id",
            info="ID of the parent folder in Google Drive; if omitted, the file is created in the root of 'My Drive'.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_CREATE_FILE_FROM_TEXT_text_content",
            display_name="Text Content",
            info="Plain text content to be written into the new file.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_CREATE_FOLDER_folder_name",
            display_name="Folder Name",
            info="Name for the new folder.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_CREATE_FOLDER_parent_id",
            display_name="Parent Id",
            info="ID or name of the parent folder. If a name is provided, the action attempts to find it. If an ID is provided, it must be a valid Google Drive folder ID. If omitted, the folder is created in the Drive root.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_DELETE_FOLDER_OR_FILE_file_id",
            display_name="File Id",
            info="The unique identifier (ID) of the folder or file to be permanently deleted from Google Drive.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_DOWNLOAD_FILE_file_id",
            display_name="File Id",
            info="The unique identifier of the file to be downloaded from Google Drive. This ID can typically be found in the file's URL in Google Drive or obtained from API calls that list files.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_DOWNLOAD_FILE_mime_type",
            display_name="Mime Type",
            info="Target MIME type for exporting Google Workspace documents (e.g., Google Doc, Sheet, Slide). ONLY use if the file is a native Google Workspace format; specifying it is highly recommended for successful export. MUST be omitted for non-Google Workspace files (e.g., PDFs, images), which are downloaded in their native format.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_EDIT_FILE_content",
            display_name="Content",
            info="New textual content to overwrite the existing file; will be UTF-8 encoded for upload.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_EDIT_FILE_file_id",
            display_name="File Id",
            info="Identifier of the Google Drive file to update.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_EDIT_FILE_mime_type",
            display_name="Mime Type",
            info="MIME type of the 'content' being uploaded; must accurately represent its format.",
            show=False,
            value="text/plain",
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_folder_id",
            display_name="Folder Id",
            info="ID of the folder to search within. If omitted, searches the root folder ('My Drive').",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_full_text_contains",
            display_name="Full Text Contains",
            info="Searches file content for this text (case-insensitive).",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_full_text_not_contains",
            display_name="Full Text Not Contains",
            info="Excludes files whose content contains this text (case-insensitive).",
            show=False,
        ),
        BoolInput(
            name="GOOGLEDRIVE_FIND_FILE_include_items_from_all_drives",
            display_name="Include Items From All Drives",
            info="Set to true to search all drives, including shared drives. If true, 'supports_all_drives' must also be true.",
            show=False,
            value=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_mime_type",
            display_name="Mime Type",
            info="Filters files by a specific MIME type (e.g., 'application/vnd.google-apps.document' for Google Docs, 'application/pdf' for PDF files).",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_modified_after",
            display_name="Modified After",
            info="Filters for files modified after this UTC RFC3339 timestamp (e.g., '2023-01-01T00:00:00Z').",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_name_contains",
            display_name="Name Contains",
            info="Searches for files whose names contain this string (case-insensitive).",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_name_exact",
            display_name="Name Exact",
            info="Searches for files with an exact, case-sensitive name match.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_name_not_contains",
            display_name="Name Not Contains",
            info="Excludes files whose names contain this string (case-insensitive).",
            show=False,
        ),
        IntInput(
            name="GOOGLEDRIVE_FIND_FILE_page_size",
            display_name="Page Size",
            info="The maximum number of files to return per page. Must be at least 1.",
            show=False,
            value=5,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FILE_page_token",
            display_name="Page Token",
            info="Token for fetching a specific page of results. Obtained from 'next_page_token' in a previous response. If omitted or empty, the first page is returned.",
            show=False,
            value="",
        ),
        BoolInput(
            name="GOOGLEDRIVE_FIND_FILE_starred",
            display_name="Starred",
            info="Filters for files that are starred (True) or not starred (False). If unspecified, starred status is not used as a filter.",
            show=False,
        ),
        BoolInput(
            name="GOOGLEDRIVE_FIND_FILE_supports_all_drives",
            display_name="Supports All Drives",
            info="Indicates if the application supports searching 'My Drive' and shared drives. Must be true if 'include_items_from_all_drives' is true.",
            show=False,
            value=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FOLDER_full_text_contains",
            display_name="Full Text Contains",
            info="A string to search for within the full text content of files within folders (if applicable and supported by Drive for the folder type or its contents). This search is case-insensitive.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FOLDER_full_text_not_contains",
            display_name="Full Text Not Contains",
            info="A string to exclude from the full text content of files within folders. This search is case-insensitive.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FOLDER_modified_after",
            display_name="Modified After",
            info="Search for folders modified after a specific date and time. The timestamp must be in RFC 3339 format (e.g., '2023-01-15T10:00:00Z' or '2023-01-15T10:00:00.000Z').",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FOLDER_name_contains",
            display_name="Name Contains",
            info="A substring to search for within folder names. This search is case-insensitive.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FOLDER_name_exact",
            display_name="Name Exact",
            info="The exact name of the folder to search for. This search is case-sensitive.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_FIND_FOLDER_name_not_contains",
            display_name="Name Not Contains",
            info="A substring to exclude from folder names. Folders with names containing this substring will not be returned. This search is case-insensitive.",
            show=False,
        ),
        BoolInput(
            name="GOOGLEDRIVE_FIND_FOLDER_starred",
            display_name="Starred",
            info="Set to true to search for folders that are starred, or false for those that are not.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_PARSE_FILE_file_id",
            display_name="File Id",
            info="The unique ID of the file stored in Google Drive that you want to export or download.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLEDRIVE_PARSE_FILE_mime_type",
            display_name="Mime Type",
            info="Target MIME type for exporting Google Workspace documents (e.g., Docs, Sheets) to a different format (e.g., PDF, DOCX). Omit for direct download of non-Workspace files or if no conversion is needed for Workspace files.",
            show=False,
        ),
        
    ]
    
    def _find_key_recursively(self, data, key):
        """Recursively search for a key in nested dicts/lists and return its value if found."""
        if isinstance(data, dict):
            if key in data:
                return data[key]
            for v in data.values():
                found = self._find_key_recursively(v, key)
                if found is not None:
                    return found
        elif isinstance(data, list):
            for item in data:
                found = self._find_key_recursively(item, key)
                if found is not None:
                    return found
        return None
    
    def execute_action(self):
        """Execute action and return response as Message."""
        toolset = self._build_wrapper()

        try:
            self._build_action_maps()
            display_name = self.action[0]["name"] if isinstance(self.action, list) and self.action else self.action
            action_key = self._display_to_key_map.get(display_name)
            if not action_key:
                msg = f"Invalid action: {display_name}"
                raise ValueError(msg)

            enum_name = getattr(Action, action_key)
            params = {}
            if action_key in self._actions_data:
                for field in self._actions_data[action_key]["action_fields"]:
                    value = getattr(self, field)

                    if value is None or value == "":
                        continue

                    if field in self._bool_variables:
                        value = bool(value)

                    param_name = field.replace(action_key + "_", "")

                    params[param_name] = value

            result = toolset.execute_action(
                action=enum_name,
                params=params,
            )
            if not result.get("successful"):
                message = result.get("data", {}).get("message", {})

                error_info = {"error": result.get("error", "No response")}
                if isinstance(message, str):
                    try:
                        parsed_message = json.loads(message)
                        if isinstance(parsed_message, dict) and "error" in parsed_message:
                            error_data = parsed_message["error"]
                            error_info = {
                                "error": {
                                    "code": error_data.get("code", "Unknown"),
                                    "message": error_data.get("message", "No error message"),
                                }
                            }
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Failed to parse error message as JSON: {e}")
                        error_info = {"error": str(message)}
                elif isinstance(message, dict) and "error" in message:
                    error_data = message["error"]
                    error_info = {
                        "error": {
                            "code": error_data.get("code", "Unknown"),
                            "message": error_data.get("message", "No error message"),
                        }
                    }

                return error_info

            result_data = result.get("data", [])
            action_data = self._actions_data.get(action_key, {})
            if action_data.get("get_result_field"):
                result_field = action_data.get("result_field")
                if result_field:
                    found = self._find_key_recursively(result_data, result_field)
                    if found is not None and found != [] and found != {}:
                        return found
                # Fall back to default method if result field extraction returns empty
            if result_data and isinstance(result_data, dict):
                return [result_data[next(iter(result_data))]]
            return result_data  # noqa: TRY300
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            display_name = self.action[0]["name"] if isinstance(self.action, list) and self.action else str(self.action)
            msg = f"Failed to execute {display_name}: {e!s}"
            raise ValueError(msg) from e

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        return super().update_build_config(build_config, field_value, field_name)

    def set_default_tools(self):
        self._default_tools = {
            self.sanitize_action_name("GOOGLEDRIVE_FIND_FILE").replace(" ", "-"),
            self.sanitize_action_name("GOOGLEDRIVE_FIND_FOLDER").replace(" ", "-"),
        }