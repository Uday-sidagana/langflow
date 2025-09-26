from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioBrandFetchAPIComponent(ComposioBaseComponent):
    display_name: str = "BrandFetch"
    icon = "BrandFetch"
    documentation: str = "https://docs.composio.dev"
    app_name = "brandfetch"

    def set_default_tools(self):
        """Set the default tools for BrandFetch component."""
