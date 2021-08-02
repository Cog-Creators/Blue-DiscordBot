import discord as _discord

from .. import __version__, version_info, VersionInfo
from .config import Config
from .audio import Audio
from .utils.safety import warn_unsafe as _warn_unsafe

__all__ = ["Audio", "Config", "__version__", "version_info", "VersionInfo"]

# Prevent discord PyNaCl missing warning
_discord.voice_client.VoiceClient.warn_nacl = False
