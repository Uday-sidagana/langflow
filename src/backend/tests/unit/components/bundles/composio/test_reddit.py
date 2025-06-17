from unittest.mock import MagicMock, patch

import pytest
from composio import Action
from langflow.components.composio.reddit_composio import ComposioRedditAPIComponent
from langflow.schema.dataframe import DataFrame

from tests.base import DID_NOT_EXIST, ComponentTestBaseWithoutClient

from .test_base import MockComposioToolSet


class MockAction:
    REDDIT_RETRIEVE_REDDIT_POST = "REDDIT_RETRIEVE_REDDIT_POST"
    REDDIT_CREATE_REDDIT_POST = "REDDIT_CREATE_REDDIT_POST"

class TestRedditComponent(ComponentTestBaseWithoutClient):
    @pytest.fixture(autouse=True)
    def mock_composio_toolset(self):
        with patch("langflow.base.composio.composio_base.ComposioToolSet", MockComposioToolSet):
            yield

    @pytest.fixture
    def component_class(self):
        return ComposioRedditAPIComponent

    @pytest.fixture
    def default_kwargs(self):
        return {
            "api_key": "",
            "entity_id": "default",
            "action": None,
        }

    @pytest.fixture
    def file_names_mapping(self):
        return [
            {"version": "1.0.17", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.0.18", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.0.19", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.1.0", "module": "composio", "file_name": DID_NOT_EXIST},
            {"version": "1.1.1", "module": "composio", "file_name": DID_NOT_EXIST},
        ]

    def test_init(self, component_class, default_kwargs):
        component = component_class(**default_kwargs)
        assert component.display_name == "Reddit"
        assert component.name == "RedditAPI"
        assert component.app_name == "reddit"
        assert "REDDIT_RETRIEVE_REDDIT_POST" in component._actions_data
        assert "REDDIT_CREATE_REDDIT_POST" in component._actions_data

    def test_execute_action_retrieve_reddit_post(self, component_class, default_kwargs, monkeypatch):
        # Mock Action enum
        monkeypatch.setattr(Action, "REDDIT_RETRIEVE_REDDIT_POST", MockAction.REDDIT_RETRIEVE_REDDIT_POST)

        # Setup component
        component = component_class(**default_kwargs)
        component.api_key = "test_key"
        component.action = [{"name": "Retrieve Reddit Post"}]
        component.REDDIT_RETRIEVE_REDDIT_POST_size = 10
        component.REDDIT_RETRIEVE_REDDIT_POST_subreddit = "test"

        # For this specific test, customize the _actions_data to not use get_result_field
        component._actions_data = {
            "REDDIT_RETRIEVE_REDDIT_POST": {
                "display_name": "Retrieve Reddit Post",
                "action_fields": ["REDDIT_RETRIEVE_REDDIT_POST_size", "REDDIT_RETRIEVE_REDDIT_POST_subreddit"],
            "get_result_field": True,
            "result_field": "posts_list",
        },
        }

        # Execute action
        result = component.execute_action()
        assert result == {"result": "mocked response"}

    # def test_execute_action_fetch_emails(self, component_class, default_kwargs, monkeypatch):
    #     # Mock Action enum
    #     monkeypatch.setattr(Action, "GMAIL_FETCH_EMAILS", MockAction.GMAIL_FETCH_EMAILS)

    #     # Setup component
    #     component = component_class(**default_kwargs)
    #     component.api_key = "test_key"
    #     component.action = [{"name": "Fetch Emails"}]
    #     component.max_results = 10
    #     component.query = "from:test@example.com"

    #     # For this specific test, we need to customize the action_data to handle results field
    #     component._actions_data = {
    #         "GMAIL_FETCH_EMAILS": {
    #             "display_name": "Fetch Emails",
    #             "action_fields": ["max_results", "query"],
    #             "result_field": "messages",
    #             "get_result_field": True,
    #         }
    #     }

    #     # Create a mock for the toolset with specific structure for this test
    #     mock_toolset = MagicMock()
    #     mock_toolset.execute_action.return_value = {"successful": True, "data": {"messages": "mocked response"}}

    #     # Patch the _build_wrapper method
    #     with patch.object(component, "_build_wrapper", return_value=mock_toolset):
    #         result = component.execute_action()
    #         # Based on the component's actual behavior, it returns the result_field directly
    #         assert result == "mocked response"

    # def test_execute_action_get_profile(self, component_class, default_kwargs, monkeypatch):
    #     # Mock Action enum
    #     monkeypatch.setattr(Action, "GMAIL_GET_PROFILE", MockAction.GMAIL_GET_PROFILE)

    #     # Setup component
    #     component = component_class(**default_kwargs)
    #     component.api_key = "test_key"
    #     component.action = [{"name": "Get User Profile"}]

    #     # For this specific test, customize the _actions_data to not use get_result_field
    #     component._actions_data = {
    #         "GMAIL_GET_PROFILE": {
    #             "display_name": "Get User Profile",
    #             "action_fields": ["gmail_user_id"],
    #             "get_result_field": False,
    #         }
    #     }

    #     # Execute action
    #     result = component.execute_action()
    #     assert result == {"result": "mocked response"}

    # def test_execute_action_invalid_action(self, component_class, default_kwargs):
    #     # Setup component
    #     component = component_class(**default_kwargs)
    #     component.api_key = "test_key"
    #     component.action = [{"name": "Invalid Action"}]

    #     # Execute action should raise ValueError
    #     with pytest.raises(ValueError, match="Invalid action: Invalid Action"):
    #         component.execute_action()

    # def test_as_dataframe(self, component_class, default_kwargs, monkeypatch):
    #     # Mock Action enum
    #     monkeypatch.setattr(Action, "GMAIL_FETCH_EMAILS", MockAction.GMAIL_FETCH_EMAILS)

    #     # Setup component
    #     component = component_class(**default_kwargs)
    #     component.api_key = "test_key"
    #     component.action = [{"name": "Fetch Emails"}]
    #     component.max_results = 10

    #     # Create mock email data that would be returned by execute_action
    #     mock_emails = [
    #         {
    #             "id": "1",
    #             "threadId": "thread1",
    #             "subject": "Test Email 1",
    #             "from": "sender1@example.com",
    #             "date": "2023-01-01",
    #             "snippet": "This is a test email",
    #         },
    #         {
    #             "id": "2",
    #             "threadId": "thread2",
    #             "subject": "Test Email 2",
    #             "from": "sender2@example.com",
    #             "date": "2023-01-02",
    #             "snippet": "This is another test email",
    #         },
    #     ]

    #     # Mock the execute_action method to return our mock data
    #     with patch.object(component, "execute_action", return_value=mock_emails):
    #         # Test as_dataframe method
    #         result = component.as_dataframe()

    #         # Verify the result is a DataFrame
    #         assert isinstance(result, DataFrame)

    #         # Verify the DataFrame is not empty
    #         assert not result.empty

    #         # Check for expected content in the DataFrame string representation
    #         data_str = str(result)
    #         assert "test email" in data_str

    # def test_update_build_config(self, component_class, default_kwargs):
    #     # Test that the Gmail component properly inherits and uses the base component's
    #     # update_build_config method
    #     component = component_class(**default_kwargs)
    #     build_config = {
    #         "auth_link": {"value": "", "auth_tooltip": ""},
    #         "action": {
    #             "options": [],
    #             "helper_text": "",
    #             "helper_text_metadata": {},
    #         },
    #     }

    #     # Test with empty API key
    #     result = component.update_build_config(build_config, "", "api_key")
    #     assert result["auth_link"]["value"] == ""
    #     assert "Please provide a valid Composio API Key" in result["auth_link"]["auth_tooltip"]
    #     assert result["action"]["options"] == []

    #     # Test with valid API key
    #     component.api_key = "test_key"
    #     result = component.update_build_config(build_config, "test_key", "api_key")
    #     assert len(result["action"]["options"]) > 0  # Should have Gmail actions
