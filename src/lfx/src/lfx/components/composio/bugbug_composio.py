from lfx.base.composio.composio_base import ComposioBaseComponent


class ComposioBugBugAPIComponent(ComposioBaseComponent):
    display_name: str = "BugBug"
    icon = "BugBug"
    documentation: str = "https://docs.composio.dev"
    app_name = "bugbug"

    def set_default_tools(self):
        """Set the default tools for BugBug component."""
