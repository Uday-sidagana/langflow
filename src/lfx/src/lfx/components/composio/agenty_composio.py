from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioAgentyAPIComponent(ComposioBaseComponent):
    display_name: str = "Agenty"
    icon = "Agenty"
    documentation: str = "https://docs.composio.dev"
    app_name = "agenty"

    def set_default_tools(self):
        """Set the default tools for Agenty component."""
