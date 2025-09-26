from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioApiFlashAPIComponent(ComposioBaseComponent):
    display_name: str = "ApiFlash"
    icon = "ApiFlash"
    documentation: str = "https://docs.composio.dev"
    app_name = "apiflash"

    def set_default_tools(self):
        """Set the default tools for ApiFlash component."""
