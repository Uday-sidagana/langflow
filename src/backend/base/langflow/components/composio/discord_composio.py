from typing import Any

from composio import Action

from langflow.base.composio.composio_base import ComposioBaseComponent
from langflow.inputs import (
    IntInput,
    MessageTextInput,
)
from langflow.logging import logger


class ComposioDiscordAPIComponent(ComposioBaseComponent):
    display_name: str = "Discord bot"
    description: str = "Discord API"
    icon = "Discord"
    documentation: str = "https://docs.composio.dev"
    app_name = "discordbot"
    
    _actions_data: dict = {
        "DISCORDBOT_ADD_GUILD_MEMBER_ROLE": {
      "display_name": "Assign role to guild member",
      "action_fields": [
        "DISCORDBOT_ADD_GUILD_MEMBER_ROLE_guild_id",
        "DISCORDBOT_ADD_GUILD_MEMBER_ROLE_role_id",
        "DISCORDBOT_ADD_GUILD_MEMBER_ROLE_user_id"
      ]
    },
    "DISCORDBOT_CREATE_DM": {
      "display_name": "Initiate user channel with recipient",
      "action_fields": [
        "DISCORDBOT_CREATE_DM_access_tokens",
        "DISCORDBOT_CREATE_DM_nicks",
        "DISCORDBOT_CREATE_DM_recipient_id"
      ]
    },
    "DISCORDBOT_CREATE_GUILD": {
      "display_name": "Create new guild object",
      "action_fields": [
        "DISCORDBOT_CREATE_GUILD_afk_channel_id",
        "DISCORDBOT_CREATE_GUILD_afk_timeout",
        "DISCORDBOT_CREATE_GUILD_channels",
        "DISCORDBOT_CREATE_GUILD_default_message_notifications",
        "DISCORDBOT_CREATE_GUILD_description",
        "DISCORDBOT_CREATE_GUILD_explicit_content_filter",
        "DISCORDBOT_CREATE_GUILD_icon",
        "DISCORDBOT_CREATE_GUILD_name",
        "DISCORDBOT_CREATE_GUILD_preferred_locale",
        "DISCORDBOT_CREATE_GUILD_region",
        "DISCORDBOT_CREATE_GUILD_roles",
        "DISCORDBOT_CREATE_GUILD_system_channel_flags",
        "DISCORDBOT_CREATE_GUILD_system_channel_id",
        "DISCORDBOT_CREATE_GUILD_verification_level"
      ]
    },
    "DISCORDBOT_DELETE_GUILD_MEMBER_ROLE": {
      "display_name": "Delete guild member role",
      "action_fields": [
        "DISCORDBOT_DELETE_GUILD_MEMBER_ROLE_guild_id",
        "DISCORDBOT_DELETE_GUILD_MEMBER_ROLE_role_id",
        "DISCORDBOT_DELETE_GUILD_MEMBER_ROLE_user_id"
      ]
    },
    "DISCORDBOT_GET_USER": {
      "display_name": "Retrieve user by id",
      "action_fields": [
        "DISCORDBOT_GET_USER_user_id"
      ]
    },
    "DISCORDBOT_LIST_GUILD_MEMBERS": {
      "display_name": "Get guild members",
      "action_fields": [
        "DISCORDBOT_LIST_GUILD_MEMBERS_after",
        "DISCORDBOT_LIST_GUILD_MEMBERS_guild_id",
        "DISCORDBOT_LIST_GUILD_MEMBERS_limit"
      ]
    }
    }
    
    _list_variables = {
        "DISCORDBOT_CREATE_DM_access_tokens",
        "DISCORDBOT_CREATE_GUILD_roles"
    }
    
    _all_fields = {field for action_data in _actions_data.values() for field in action_data["action_fields"]}
    
    _bool_variables = {}
    
    inputs = [
        *ComposioBaseComponent._base_inputs,
        MessageTextInput(
        name="DISCORDBOT_DELETE_GUILD_MEMBER_ROLE_guild_id",
        display_name="Guild Id",
        info="Guild Id",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_DELETE_GUILD_MEMBER_ROLE_role_id",
        display_name="Role Id",
        info="Role Id",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_DELETE_GUILD_MEMBER_ROLE_user_id",
        display_name="User Id",
        info="User Id",
        show=False,
        required=True,
    ),
    IntInput(
        name="DISCORDBOT_LIST_GUILD_MEMBERS_after",
        display_name="After",
        info="After",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_LIST_GUILD_MEMBERS_guild_id",
        display_name="Guild Id",
        info="Guild Id",
        show=False,
        required=True,
    ),
    IntInput(
        name="DISCORDBOT_LIST_GUILD_MEMBERS_limit",
        display_name="Limit",
        info="Limit",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_GET_USER_user_id",
        display_name="User Id",
        info="User Id",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_DM_access_tokens",
        display_name="Access Tokens",
        info="Access Tokens",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_DM_nicks",
        display_name="Nicks",
        info="Nicks",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_DM_recipient_id",
        display_name="Recipient Id",
        info="Recipient Id",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_ADD_GUILD_MEMBER_ROLE_guild_id",
        display_name="Guild Id",
        info="Guild Id",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_ADD_GUILD_MEMBER_ROLE_role_id",
        display_name="Role Id",
        info="Role Id",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_ADD_GUILD_MEMBER_ROLE_user_id",
        display_name="User Id",
        info="User Id",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_afk_channel_id",
        display_name="Afk Channel Id",
        info="Afk Channel Id",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_afk_timeout",
        display_name="Afk Timeout",
        info="Afk Timeout",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_channels",
        display_name="Channels",
        info="Channels",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_default_message_notifications",
        display_name="Default Message Notifications",
        info="Default Message Notifications",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_description",
        display_name="Description",
        info="Description",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_explicit_content_filter",
        display_name="Explicit Content Filter",
        info="Explicit Content Filter",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_icon",
        display_name="Icon",
        info="Icon",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_name",
        display_name="Name",
        info="Name",
        show=False,
        required=True,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_preferred_locale",
        display_name="Preferred Locale",
        info="Preferred Locale",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_region",
        display_name="Region",
        info="Region",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_roles",
        display_name="Roles",
        info="Roles",
        show=False,
    ),
    IntInput(
        name="DISCORDBOT_CREATE_GUILD_system_channel_flags",
        display_name="System Channel Flags",
        info="System Channel Flags",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_system_channel_id",
        display_name="System Channel Id",
        info="System Channel Id",
        show=False,
    ),
    MessageTextInput(
        name="DISCORDBOT_CREATE_GUILD_verification_level",
        display_name="Verification Level",
        info="Verification Level",
        show=False,
    ),
    ]
    
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
                    
                    if field in self._list_variables and value:
                        value = [item.strip() for item in value.split(",")]

                    if field in self._bool_variables:
                        value = bool(value)

                    param_name = field.replace(action_key + "_", "")

                    params[param_name] = value

            result = toolset.execute_action(
                action=enum_name,
                params=params,
            )
            if not result.get("successful"):
                return {"error": result.get("error", "No response")}

            return result.get("data", [])
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            display_name = self.action[0]["name"] if isinstance(self.action, list) and self.action else str(self.action)
            msg = f"Failed to execute {display_name}: {e!s}"
            raise ValueError(msg) from e

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        return super().update_build_config(build_config, field_value, field_name)

    def set_default_tools(self):
        self._default_tools = {
            self.sanitize_action_name("<default action 1>").replace(" ", "-"),
            self.sanitize_action_name("<default action 2>").replace(" ", "-"),
        }