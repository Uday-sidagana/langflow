from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioActiveAPIComponent(ComposioBaseComponent):
    display_name: str = "Active"
    icon = "Active"
    documentation: str = "https://docs.composio.dev"
    app_name = "active"

    def set_default_tools(self):
        """Set the default tools for Active component."""
