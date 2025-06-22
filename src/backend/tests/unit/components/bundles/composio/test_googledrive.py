from unittest.mock import patch

import pytest
from composio import Action
from langflow.components.composio.googledrive_composio import ComposioGoogleDriveAPIComponent
from langflow.schema.dataframe import DataFrame

from tests.base import DID_NOT_EXIST, ComponentTestBaseWithoutClient

from .test_base import MockComposioToolSet


class MockAction:
    GOOGLEDRIVE_FIND_FILE = "GOOGLEDRIVE_FIND_FILE"
    GOOGLEDRIVE_FIND_FOLDER = "GOOGLEDRIVE_FIND_FOLDER"


class TestGoogleDriveComponent(ComponentTestBaseWithoutClient):
    @pytest.fixture(autouse=True)
    def mock_composio_toolset(self):
        with patch("langflow.base.composio.composio_base.ComposioToolSet", MockComposioToolSet):
            yield

    @pytest.fixture
    def component_class(self):
        return ComposioGoogleDriveAPIComponent

    @pytest.fixture
    def default_kwargs(self):
        return {
            "api_key": "",
            "entity_id": "default",
            "action": None,
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
        assert component.display_name == "GoogleDrive"
        assert component.app_name == "googledrive"
        assert "GOOGLEDRIVE_FIND_FILE" in component._actions_data
        assert "GOOGLEDRIVE_FIND_FOLDER" in component._actions_data

    def test_execute_action_find_file(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum
        monkeypatch.setattr(
            Action,
            "GOOGLEDRIVE_FIND_FILE",
            MockAction.GOOGLEDRIVE_FIND_FILE,
        )

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Find File"}]
        component.GOOGLEDRIVE_FIND_FILE_folder_id = "langflow-ai"
        component.GOOGLEDRIVE_FIND_FILE_full_text_contains = "langflow"

        # For this specific test, customize the _actions_data to not use get_result_field
        component._actions_data = {
            "GOOGLEDRIVE_FIND_FILE": {
                "display_name": "Find File",
                "action_fields": [
                    "GOOGLEDRIVE_FIND_FILE_folder_id",
                    "GOOGLEDRIVE_FIND_FILE_full_text_contains",
                ],
            },
        }

        # Execute action
        result = component.execute_action()
        assert result == ["mocked response"]

    def test_execute_action_find_folder(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum
        monkeypatch.setattr(Action, "GOOGLEDRIVE_FIND_FOLDER", MockAction.GOOGLEDRIVE_FIND_FOLDER)

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Find Folder"}]
        component.GOOGLEDRIVE_FIND_FOLDER_full_text_contains = "langflow"

        # For this specific test, customize the _actions_data to not use get_result_field
        component._actions_data = {
            "GOOGLEDRIVE_FIND_FOLDER": {
                "display_name": "Find Folder",
                "action_fields": [
                    "GOOGLEDRIVE_FIND_FOLDER_full_text_contains",
                    "GOOGLEDRIVE_FIND_FOLDER_full_text_not_contains",
                    "GOOGLEDRIVE_FIND_FOLDER_modified_after",
                    "GOOGLEDRIVE_FIND_FOLDER_name_contains",
                    "GOOGLEDRIVE_FIND_FOLDER_name_exact",
                    "GOOGLEDRIVE_FIND_FOLDER_name_not_contains",
                    "GOOGLEDRIVE_FIND_FOLDER_starred",
                ],
            },
        }

        # Execute action
        result = component.execute_action()
        assert result == ["mocked response"]

   

    def test_execute_action_invalid_action(self, component_class, default_kwargs):
        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Invalid Action"}]

        # Execute action should raise ValueError
        with pytest.raises(ValueError, match="Invalid action: Invalid Action"):
            component.execute_action()

    def test_as_dataframe(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum
        monkeypatch.setattr(Action, "GOOGLEDRIVE_FIND_FILE", MockAction.GOOGLEDRIVE_FIND_FILE)

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Find File"}]
        component.GOOGLEDRIVE_FIND_FILE_folder_id = "langflow-ai"
        component.GOOGLEDRIVE_FIND_FILE_full_text_contains = "langflow"

        # Create mock email data that would be returned by execute_action
        mock_files = [
            {
                "id": "id1",
                "name": "test file",
                "mime_type": "text/plain",
                "created_at": "2023-01-01",
                "updated_at": "2023-01-01",
            },
            {
                "id": "id2",
                "name": "test file 2",
                "mime_type": "text/plain",
                "created_at": "2023-01-01",
                "updated_at": "2023-01-01",
            },
        ]

        # Mock the execute_action method to return our mock data
        with patch.object(component, "execute_action", return_value=mock_files):
            # Test as_dataframe method
            result = component.as_dataframe()

            # Verify the result is a DataFrame
            assert isinstance(result, DataFrame)

            # Verify the DataFrame is not empty
            assert not result.empty

            # Check for expected content in the DataFrame string representation
            data_str = str(result)
            assert "test file" in data_str
            assert "test file 2" in data_str

    def test_update_build_config(self, component_class, default_kwargs):
        # Test that the GitHub component properly inherits and uses the base component's
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
        assert len(result["action"]["options"]) > 0  # Should have GitHub actions
