import logging
from raven import Client
from raven.handlers.logging import SentryHandler

from redbot.core import __version__

__all__ = ("SentryManager",)


class SentryManager:
    """Simple class to manage sentry logging for Red."""

    def __init__(self, logger: logging.Logger):
        client = Client(
            dsn=("https://62402161d4cd4ef18f83b16f3e22a020:9310ef55a502442598203205a84da2bb@"
                 "sentry.io/253983"),
            release=__version__,
            include_paths=['redbot'],
            enable_breadcrumbs=False
        )
        self.handler = SentryHandler(client)
        self.logger = logger

    def enable(self):
        """Enable error reporting for Sentry."""
        self.logger.addHandler(self.handler)

    def disable(self):
        """Disable error reporting for Sentry."""
        self.logger.removeHandler(self.handler)
