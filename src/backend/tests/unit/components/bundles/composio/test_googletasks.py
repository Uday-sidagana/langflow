from unittest.mock import MagicMock, patch

import pytest
from composio import Action
from langflow.components.composio.googletasks_composio import ComposioGoogleTasksAPIComponent
from langflow.schema.dataframe import DataFrame

from tests.base import DID_NOT_EXIST, ComponentTestBaseWithoutClient

from .test_base import MockComposioToolSet


class MockAction:
    GOOGLETASKS_CREATE_TASK_LIST = "GOOGLETASKS_CREATE_TASK_LIST"
    GOOGLETASKS_DELETE_TASK = "GOOGLETASKS_DELETE_TASK"


class TestGoogleTasksComponent(ComponentTestBaseWithoutClient):
    @pytest.fixture(autouse=True)
    def mock_composio_toolset(self):
        with patch("langflow.base.composio.composio_base.ComposioToolSet", MockComposioToolSet):
            yield

    @pytest.fixture
    def component_class(self):
        return ComposioGoogleTasksAPIComponent

    @pytest.fixture
    def default_kwargs(self):
        return {
            "api_key": "",
            "entity_id": "default",
            "action": None,
            "task_list_id": "",
            "task_id": "",
            "task_list_name": "",
            "task_name": "",
            "task_description": "",
            "task_due_date": "",
            "task_completed": False,
        }

    @pytest.fixture
    def file_names_mapping(self):
        # Component not yet released, mark all versions as non-existent
        return [
            {"version": "1.0.17", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.0.18", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.0.19", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.1.0", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.1.1", "module": "composio", "file_name": DID_NOT_EXIST},
        ]

    def test_init(self, component_class, default_kwargs):
        component = component_class(**default_kwargs)
        assert component.display_name == "Google Tasks"
        assert component.app_name == "googletasks"
        assert "GOOGLETASKS_CREATE_TASK_LIST" in component._actions_data
        assert "GOOGLETASKS_DELETE_TASK" in component._actions_data

    def test_execute_action_create_task_list(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum
        monkeypatch.setattr(Action, "GOOGLETASKS_CREATE_TASK_LIST", MockAction.GOOGLETASKS_CREATE_TASK_LIST)

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Create A Task List"}]
        component.GOOGLETASKS_CREATE_TASK_LIST_tasklist_title = "Test Task List"

        # Execute action
        result = component.execute_action()
        assert result == {"result": "mocked response"}

    def test_execute_action_delete_task(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum
        monkeypatch.setattr(Action, "GOOGLETASKS_DELETE_TASK", MockAction.GOOGLETASKS_DELETE_TASK)

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Delete Task"}]
        component.GOOGLETASKS_DELETE_TASK_task_id = "test_task_id"
        component.GOOGLETASKS_DELETE_TASK_tasklist_id = "test_tasklist_id"

        # Execute action (should return normal result since action doesn't have get_result_field)
        result = component.execute_action()
        assert result == {"result": "mocked response"}

    def test_execute_action_with_result_field(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum for an action that has result_field configured
        monkeypatch.setattr(Action, "GOOGLETASKS_GET_TASK", "GOOGLETASKS_GET_TASK")

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Get Task"}]
        component.GOOGLETASKS_GET_TASK_task_id = "test_task_id"
        component.GOOGLETASKS_GET_TASK_tasklist_id = "test_tasklist_id"

        # Create a mock for the toolset with specific structure for this test
        mock_toolset = MagicMock()
        mock_toolset.execute_action.return_value = {
            "successful": True,
            "data": {"task": {"id": "123", "title": "Test Task", "status": "needsAction"}},
        }

        # Patch the _build_wrapper method
        with patch.object(component, "_build_wrapper", return_value=mock_toolset):
            result = component.execute_action()
            # Should return the task data from the result_field
            assert result == {"id": "123", "title": "Test Task", "status": "needsAction"}

    def test_execute_action_invalid_action(self, component_class, default_kwargs):
        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Invalid Action"}]

        # Execute action should raise ValueError
        with pytest.raises(ValueError, match="Invalid action: Invalid Action"):
            component.execute_action()

    def test_as_dataframe(self, component_class, default_kwargs):
        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"

        # Create mock task data that would be returned by execute_action
        mock_tasks = [
            {
                "id": "1",
                "title": "Test Task 1",
                "due": "2023-01-01",
                "status": "needsAction",
                "notes": "This is a test task",
            },
            {
                "id": "2",
                "title": "Test Task 2",
                "due": "2023-01-02",
                "status": "completed",
                "notes": "This is another test task",
            },
        ]

        # Mock the execute_action method to return our mock data
        with patch.object(component, "execute_action", return_value=mock_tasks):
            # Test as_dataframe method
            result = component.as_dataframe()

            # Verify the result is a DataFrame
            assert isinstance(result, DataFrame)

            # Verify the DataFrame is not empty
            assert not result.empty

            # Check for expected content in the DataFrame string representation
            data_str = str(result)
            assert "test task" in data_str.lower()

    def test_update_build_config(self, component_class, default_kwargs):
        # Test that the GoogleTasks component properly inherits and uses the base component's
        # update_build_config method
        component = component_class(**default_kwargs)
        build_config = {
            "auth_link": {"value": "", "auth_tooltip": ""},
            "action": {
                "options": [],
                "helper_text": "",
                "helper_text_metadata": {},
            },
        }

        # Test with empty API key
        result = component.update_build_config(build_config, "", "api_key")
        assert result["auth_link"]["value"] == ""
        assert "Please provide a valid Composio API Key" in result["auth_link"]["auth_tooltip"]
        assert result["action"]["options"] == []

        # Test with valid API key
        component.api_key = "test_key"
        result = component.update_build_config(build_config, "test_key", "api_key")
        assert len(result["action"]["options"]) > 0  # Should have GoogleTasks actions
