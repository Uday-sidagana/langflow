from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioAbstractAPIComponent(ComposioBaseComponent):
    display_name: str = "Abstract"
    icon = "Abstract"
    documentation: str = "https://docs.composio.dev"
    app_name = "abstract"

    def set_default_tools(self):
        """Set the default tools for Abstract component."""
