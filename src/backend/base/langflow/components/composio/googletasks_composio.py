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


class ComposioGoogleTasksAPIComponent(ComposioBaseComponent):
    display_name: str = "Google Tasks"
    description: str = "GoogleTasks API"
    icon = "GoogleTasks"
    documentation: str = "https://docs.composio.dev"
    app_name = "googletasks"

    _actions_data: dict = {
        "GOOGLETASKS_CLEAR_TASKS": {
            "display_name": "Clear Tasks",
            "action_fields": ["GOOGLETASKS_CLEAR_TASKS_tasklist"],
            "get_result_field": True,
            "result_field": "response_data",
        },
        "GOOGLETASKS_CREATE_TASK_LIST": {
            "display_name": "Create A Task List",
            "action_fields": ["GOOGLETASKS_CREATE_TASK_LIST_tasklist_title"],
        },
        "GOOGLETASKS_DELETE_TASK": {
            "display_name": "Delete Task",
            "action_fields": ["GOOGLETASKS_DELETE_TASK_task_id", "GOOGLETASKS_DELETE_TASK_tasklist_id"],
        },
        "GOOGLETASKS_DELETE_TASK_LIST": {
            "display_name": "Delete Task List",
            "action_fields": ["GOOGLETASKS_DELETE_TASK_LIST_tasklist_id"],
        },
        "GOOGLETASKS_GET_TASK": {
            "display_name": "Get Task",
            "action_fields": ["GOOGLETASKS_GET_TASK_task_id", "GOOGLETASKS_GET_TASK_tasklist_id"],
            "get_result_field": True,
            "result_field": "task",
        },
        "GOOGLETASKS_GET_TASK_LIST": {
            "display_name": "Get Task List",
            "action_fields": ["GOOGLETASKS_GET_TASK_LIST_tasklist_id"],
            "get_result_field": True,
            "result_field": "task_list",
        },
        "GOOGLETASKS_INSERT_TASK": {
            "display_name": "Insert Task",
            "action_fields": [
                "GOOGLETASKS_INSERT_TASK_completed",
                "GOOGLETASKS_INSERT_TASK_deleted",
                "GOOGLETASKS_INSERT_TASK_due",
                "GOOGLETASKS_INSERT_TASK_etag",
                "GOOGLETASKS_INSERT_TASK_hidden",
                "GOOGLETASKS_INSERT_TASK_id",
                "GOOGLETASKS_INSERT_TASK_notes",
                "GOOGLETASKS_INSERT_TASK_status",
                "GOOGLETASKS_INSERT_TASK_task_parent",
                "GOOGLETASKS_INSERT_TASK_task_previous",
                "GOOGLETASKS_INSERT_TASK_tasklist_id",
                "GOOGLETASKS_INSERT_TASK_title",
            ],
            "get_result_field": True,
            "result_field": "task",
        },
        "GOOGLETASKS_LIST_TASKS": {
            "display_name": "List Tasks",
            "action_fields": [
                "GOOGLETASKS_LIST_TASKS_completedMax",
                "GOOGLETASKS_LIST_TASKS_completedMin",
                "GOOGLETASKS_LIST_TASKS_dueMax",
                "GOOGLETASKS_LIST_TASKS_dueMin",
                "GOOGLETASKS_LIST_TASKS_maxResults",
                "GOOGLETASKS_LIST_TASKS_pageToken",
                "GOOGLETASKS_LIST_TASKS_showCompleted",
                "GOOGLETASKS_LIST_TASKS_showDeleted",
                "GOOGLETASKS_LIST_TASKS_showHidden",
                "GOOGLETASKS_LIST_TASKS_tasklist_id",
                "GOOGLETASKS_LIST_TASKS_updatedMin",
            ],
            "get_result_field": True,
            "result_field": "tasks",
        },
        "GOOGLETASKS_LIST_TASK_LISTS": {
            "display_name": "List Task Lists",
            "action_fields": ["GOOGLETASKS_LIST_TASK_LISTS_maxResults", "GOOGLETASKS_LIST_TASK_LISTS_pageToken"],
            "get_result_field": True,
            "result_field": "items",
        },
        "GOOGLETASKS_MOVE_TASK": {
            "display_name": "Move Task",
            "action_fields": [
                "GOOGLETASKS_MOVE_TASK_destinationTasklist",
                "GOOGLETASKS_MOVE_TASK_parent",
                "GOOGLETASKS_MOVE_TASK_previous",
                "GOOGLETASKS_MOVE_TASK_task",
                "GOOGLETASKS_MOVE_TASK_tasklist",
            ],
        },
        "GOOGLETASKS_PATCH_TASK": {
            "display_name": "Patch Task",
            "action_fields": [
                "GOOGLETASKS_PATCH_TASK_completed",
                "GOOGLETASKS_PATCH_TASK_deleted",
                "GOOGLETASKS_PATCH_TASK_due",
                "GOOGLETASKS_PATCH_TASK_etag",
                "GOOGLETASKS_PATCH_TASK_hidden",
                "GOOGLETASKS_PATCH_TASK_id",
                "GOOGLETASKS_PATCH_TASK_notes",
                "GOOGLETASKS_PATCH_TASK_status",
                "GOOGLETASKS_PATCH_TASK_task_id",
                "GOOGLETASKS_PATCH_TASK_tasklist_id",
                "GOOGLETASKS_PATCH_TASK_title",
            ],
            "get_result_field": True,
            "result_field": "task",
        },
        "GOOGLETASKS_PATCH_TASK_LIST": {
            "display_name": "Patch Task List",
            "action_fields": ["GOOGLETASKS_PATCH_TASK_LIST_tasklist_id", "GOOGLETASKS_PATCH_TASK_LIST_updated_title"],
            "get_result_field": True,
            "result_field": "response_data",
        },
        "GOOGLETASKS_UPDATE_TASK": {
            "display_name": "Update Task",
            "action_fields": [
                "GOOGLETASKS_UPDATE_TASK_due",
                "GOOGLETASKS_UPDATE_TASK_notes",
                "GOOGLETASKS_UPDATE_TASK_status",
                "GOOGLETASKS_UPDATE_TASK_task",
                "GOOGLETASKS_UPDATE_TASK_tasklist",
                "GOOGLETASKS_UPDATE_TASK_title",
            ],
        },
        "GOOGLETASKS_UPDATE_TASK_LIST": {
            "display_name": "Update Task List",
            "action_fields": ["GOOGLETASKS_UPDATE_TASK_LIST_tasklist_id", "GOOGLETASKS_UPDATE_TASK_LIST_title"],
        },
    }

    _all_fields = {field for action_data in _actions_data.values() for field in action_data["action_fields"]}

    _bool_variables = {
        "GOOGLETASKS_INSERT_TASK_deleted",
        "GOOGLETASKS_INSERT_TASK_hidden",
        "GOOGLETASKS_LIST_TASKS_showCompleted",
        "GOOGLETASKS_LIST_TASKS_showDeleted",
        "GOOGLETASKS_LIST_TASKS_showHidden",
        "GOOGLETASKS_PATCH_TASK_deleted",
        "GOOGLETASKS_PATCH_TASK_hidden",
    }

    inputs = [
        *ComposioBaseComponent._base_inputs,
        MessageTextInput(
            name="GOOGLETASKS_CLEAR_TASKS_tasklist",
            display_name="Tasklist",
            info="The identifier of the task list from which to clear completed tasks. Use '@default' for the default task list.",  # noqa: E501
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_CREATE_TASK_LIST_tasklist_title",
            display_name="Tasklist Title",
            info="Title for the new task list. The maximum allowed length is 1024 characters.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_DELETE_TASK_task_id",
            display_name="Task Id",
            info="The unique identifier of the Google Task to be deleted.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_DELETE_TASK_tasklist_id",
            display_name="Tasklist Id",
            info="The unique identifier of the Google Task list from which the task will be deleted.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_DELETE_TASK_LIST_tasklist_id",
            display_name="Tasklist Id",
            info="Unique identifier of the Google Task list to be deleted.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_GET_TASK_task_id",
            display_name="Task Id",
            info="Unique identifier of the Google Task to retrieve.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_GET_TASK_tasklist_id",
            display_name="Tasklist Id",
            info="Unique identifier of the Google Tasks list containing the task.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_GET_TASK_LIST_tasklist_id",
            display_name="Tasklist Id",
            info="The unique identifier of the task list to retrieve, assigned by Google Tasks when the list is created.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_completed",
            display_name="Completed",
            info="Completion date of the task. , Some examples of expected datetime format:,        UTC-5:30, 6:50 PM       ->If date is not mentioned, and seeming that the start date is in next 24 hours.,   UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_INSERT_TASK_deleted",
            display_name="Deleted",
            info="Flag indicating whether the task has been deleted.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_due",
            display_name="Due",
            info="Due date of the task. , Some examples of expected datetime format:,       UTC-5:30, 6:50 PM       ->If date is not mentioned, and seeming that the start date is in next 24 hours.,   UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_etag",
            display_name="Etag",
            info="ETag of the resource.",
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_INSERT_TASK_hidden",
            display_name="Hidden",
            info="Flag indicating whether the task is hidden.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_id",
            display_name="Id",
            info="Task identifier.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_notes",
            display_name="Notes",
            info="Notes describing the task. Optional. Maximum length allowed: 8192 characters.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_status",
            display_name="Status",
            info="Status of the task. This is either 'needsAction' or 'completed'.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_task_parent",
            display_name="Task Parent",
            info="Identifier of an existing task to serve as parent; if provided, creates a subtask, otherwise a top-level task in the specified list.",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_task_previous",
            display_name="Task Previous",
            info="Identifier of an existing task after which the new task will be placed, at the same hierarchical level (as a sibling).",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_tasklist_id",
            display_name="Tasklist Id",
            info="Identifier for the Google Task list where the new task will be created.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_INSERT_TASK_title",
            display_name="Title",
            info="Title of the task. Maximum length allowed: 1024 characters.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_completedMax",
            display_name="Completed Max",
            info="Exclude tasks completed after this date. , Some examples of expected datetime format:,    UTC-5:30, 6:50 PM  ->If date is not mentioned, and seeming that the start date is in next 24 hours.,        UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_completedMin",
            display_name="Completed Min",
            info="Exclude tasks completed before this date. , Some examples of expected datetime format:,   UTC-5:30, 6:50 PM  ->If date is not mentioned, and seeming that the start date is in next 24 hours.,        UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_dueMax",
            display_name="Due Max",
            info="Exclude tasks due after this date. , Some examples of expected datetime format:,  UTC-5:30, 6:50 PM       ->If date is not mentioned, and seeming that the start date is in next 24 hours.,   UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_dueMin",
            display_name="Due Min",
            info="Exclude tasks due before this date. , Some examples of expected datetime format:,         UTC-5:30, 6:50 PM  ->If date is not mentioned, and seeming that the start date is in next 24 hours.,        UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        IntInput(
            name="GOOGLETASKS_LIST_TASKS_maxResults",
            display_name="Max Results",
            info="Maximum number of tasks to return. API default: 20, maximum: 100.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_pageToken",
            display_name="Page Token",
            info="Token from a previous list operation for fetching a specific page; if omitted, retrieves the first page.",
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_LIST_TASKS_showCompleted",
            display_name="Show Completed",
            info="Include completed tasks. Defaults to true. (See action docstring for interaction with `completedMin`/`Max`).",  # noqa: E501
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_LIST_TASKS_showDeleted",
            display_name="Show Deleted",
            info="Include deleted tasks. Defaults to false.",
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_LIST_TASKS_showHidden",
            display_name="Show Hidden",
            info="Include hidden tasks. Defaults to false.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_tasklist_id",
            display_name="Tasklist Id",
            info="Identifier of the task list. Use '@default' for the user's primary task list.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASKS_updatedMin",
            display_name="Updated Min",
            info="Lower bound for task's last modification time (for syncing). , Some examples of expected datetime format:,   UTC-5:30, 6:50 PM        ->If date is not mentioned, and seeming that the start date is in next 24 hours.,       UTC+1, 11:59 PM, 31 Dec     ->If the meeting start date is in next 1 year (this is most possible case),     UTC-3:45, 7:15 AM, 22 Aug 2020      ->If the meeting is to be set after at a spefic date, mentioned with year.,     11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        IntInput(
            name="GOOGLETASKS_LIST_TASK_LISTS_maxResults",
            display_name="Max Results",
            info="Maximum number of task lists to return per page.",
            show=False,
            value=20,
        ),
        MessageTextInput(
            name="GOOGLETASKS_LIST_TASK_LISTS_pageToken",
            display_name="Page Token",
            info="Token for the page of results to return; omit for the first page, use `nextPageToken` from a previous response for subsequent pages.",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_MOVE_TASK_destinationTasklist",
            display_name="Destination Tasklist",
            info="Destination task list identifier. If set, the task is moved to this list; otherwise, it remains in its current list.",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_MOVE_TASK_parent",
            display_name="Parent",
            info="New parent task identifier. If not provided, the task is moved to the top level.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_MOVE_TASK_previous",
            display_name="Previous",
            info="New previous sibling task identifier. If not provided, the task is moved to the first position among its siblings.",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_MOVE_TASK_task",
            display_name="Task",
            info="Task identifier.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_MOVE_TASK_tasklist",
            display_name="Tasklist",
            info="Task list identifier.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_completed",
            display_name="Completed",
            info="Completion date of the task. , Some examples of expected datetime format:,        UTC-5:30, 6:50 PM       ->If date is not mentioned, and seeming that the start date is in next 24 hours.,   UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_PATCH_TASK_deleted",
            display_name="Deleted",
            info="Flag indicating whether the task has been deleted.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_due",
            display_name="Due",
            info="Due date of the task. , Some examples of expected datetime format:,       UTC-5:30, 6:50 PM       ->If date is not mentioned, and seeming that the start date is in next 24 hours.,   UTC+1, 11:59 PM, 31 Dec ->If the meeting start date is in next 1 year (this is most possible case),         UTC-3:45, 7:15 AM, 22 Aug 2020  ->If the meeting is to be set after at a spefic date, mentioned with year.,         11:15 PM, 12 May 2019   ->In case no UTC offset to be mentioned, skip the UTC part altogether.,     2023-03-01T00:00:00Z    ->Standard ISO-8601 format",  # noqa: E501
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_etag",
            display_name="Etag",
            info="ETag of the resource.",
            show=False,
        ),
        BoolInput(
            name="GOOGLETASKS_PATCH_TASK_hidden",
            display_name="Hidden",
            info="Flag indicating whether the task is hidden.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_id",
            display_name="Id",
            info="Task identifier.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_notes",
            display_name="Notes",
            info="Notes describing the task. Optional. Maximum length allowed: 8192 characters.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_status",
            display_name="Status",
            info="Status of the task. This is either 'needsAction' or 'completed'.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_task_id",
            display_name="Task Id",
            info="Identifier of the Google Task to be updated within the specified task list.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_tasklist_id",
            display_name="Tasklist Id",
            info="Identifier of the Google Task list that contains the task to be updated.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_title",
            display_name="Title",
            info="Title of the task. Maximum length allowed: 1024 characters.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_LIST_tasklist_id",
            display_name="Tasklist Id",
            info="The unique identifier of the task list to be updated.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_PATCH_TASK_LIST_updated_title",
            display_name="Updated Title",
            info="The new title for the task list.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_due",
            display_name="Due",
            info="Due date of the task (RFC 3339 timestamp).",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_notes",
            display_name="Notes",
            info="Notes describing the task.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_status",
            display_name="Status",
            info="Status of the task (needsAction or completed).",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_task",
            display_name="Task",
            info="Task identifier.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_tasklist",
            display_name="Tasklist",
            info="Task list identifier.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_title",
            display_name="Title",
            info="Title of the task.",
            show=False,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_LIST_tasklist_id",
            display_name="Tasklist Id",
            info="Task list identifier.",
            show=False,
            required=True,
        ),
        MessageTextInput(
            name="GOOGLETASKS_UPDATE_TASK_LIST_title",
            display_name="Title",
            info="Title of the task list. Maximum length allowed: 1024 characters.",
            show=False,
            required=True,
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

            # If get_result_field is True and result_field is specified, use recursive search
            if action_data.get("get_result_field") and action_data.get("result_field"):
                result_field = action_data.get("result_field")
                found = self._find_key_recursively(result_data, result_field)
                if found is not None and found != [] and found != {}:  # noqa: PLR1714
                    return found
                # Fall back to original approach if result field extraction returns empty

            # Original approach: if result_field is not specified or recursive search failed
            if len(result_data) != 1 and not action_data.get("result_field") and action_data.get("get_result_field"):
                msg = f"Expected a dict with a single key, got {len(result_data)} keys: {result_data.keys()}"
                raise ValueError(msg)
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
            "GOOGLETASKS_CREATE_TASK_LIST",
            "GOOGLETASKS_DELETE_TASK",
        }
