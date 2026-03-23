from .config import Config


class NotificationConfig(Config):
    """Stores event notification bot settings per server (e.g. notification channels)."""

    def __init__(self, server, path=None):
        super().__init__(server, path, module_name="NotificationConfig")

    def create_module(self):
        return self.write({"upcoming_events_channel_id": None, "new_pdga_approved_discs_channel_id": None}, self.module_name)

    def get_upcoming_events_channel_id(self) -> int | None:
        """Get the channel ID for upcoming events notifications."""
        data = self.read_module()
        return data.get("upcoming_events_channel_id") if data else None

    def set_upcoming_events_channel_id(self, channel_id: int) -> bool:
        """Set the channel ID for upcoming events notifications."""
        data = self.read_module() or {}
        data["upcoming_events_channel_id"] = channel_id
        return self.write(data, self.module_name)

    def get_new_pdga_approved_discs_channel_id(self) -> int | None:
        """Get the channel ID for new PDGA approved discs notifications."""
        data = self.read_module()
        return data.get("new_pdga_approved_discs_channel_id") if data else None

    def set_new_pdga_approved_discs_channel_id(self, channel_id: int) -> bool:
        """Set the channel ID for new PDGA approved discs notifications."""
        data = self.read_module() or {}
        data["new_pdga_approved_discs_channel_id"] = channel_id
        return self.write(data, self.module_name)
