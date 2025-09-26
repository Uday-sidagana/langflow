from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioBitQueryAPIComponent(ComposioBaseComponent):
    display_name: str = "BitQuery"
    icon = "BitQuery"
    documentation: str = "https://docs.composio.dev"
    app_name = "bitquery"

    def set_default_tools(self):
        """Set the default tools for BitQuery component."""
