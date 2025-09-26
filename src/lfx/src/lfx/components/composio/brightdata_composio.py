from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioBrightDataAPIComponent(ComposioBaseComponent):
    display_name: str = "BrightData"
    icon = "BrightData"
    documentation: str = "https://docs.composio.dev"
    app_name = "brightdata"

    def set_default_tools(self):
        """Set the default tools for BrightData component."""
