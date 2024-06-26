import gi

gi.require_version("Notify", "0.7")
from gi.repository import GdkPixbuf, Notify  # type: ignore[attr-defined]

from eduvpn.variants import ApplicationVariant


def initialize(app_variant: ApplicationVariant) -> None:
    Notify.init(app_variant.name)


class Notification:
    def __init__(self, app_variant: ApplicationVariant) -> None:
        self.app_variant = app_variant
        self.notification = None

    def _build(self):
        icon = GdkPixbuf.Pixbuf.new_from_file(self.app_variant.icon)  # type: ignore
        notification = Notify.Notification.new(self.app_variant.name)
        notification.set_icon_from_pixbuf(icon)
        notification.set_app_name(self.app_variant.name)
        return notification

    def show(self, title: str, message: str):
        if self.notification is None:
            self.notification = self._build()
        self.notification.update(title, message)  # type: ignore
        self.notification.show()  # type: ignore

    def hide(self) -> None:
        if self.notification is not None:
            self.notification.close()  # type: ignore
            self.notification = None
