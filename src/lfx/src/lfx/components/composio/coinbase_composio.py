from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioCoinbaseAPIComponent(ComposioBaseComponent):
    display_name: str = "Coinbase"
    icon = "Coinbase"
    documentation: str = "https://docs.composio.dev"
    app_name = "coinbase"

    def set_default_tools(self):
        """Set the default tools for Coinbase component."""
