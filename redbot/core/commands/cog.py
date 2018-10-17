import inspect
from typing import Callable, TYPE_CHECKING, Dict, List, Union, Awaitable, Optional

import discord
import discord.ext.commands

from .commands import CogCommandMixin, CogGroupMixin, Command
from .errors import OverrideNotAllowed
from ..i18n import Translator

if TYPE_CHECKING:
    from .context import Context


__all__ = ["CogMeta", "Cog"]

_ = Translator(__file__)


class CogMeta(CogCommandMixin, CogGroupMixin, type):
    """Metaclass for cog base class."""

    __checks: List[Callable[["Context"], Union[bool, Awaitable[bool]]]]
    __translator: Optional[Callable[[str], str]]

    def __init__(cls, *args, **kwargs) -> None:
        try:
            cls.__checks = getattr(cls, "__commands_checks__")
        except AttributeError:
            cls.__checks = []
        else:
            delattr(cls, "__commands_checks__")
        try:
            # Assign translator object if Cog.__init_subclass__ wasn't called.
            # Not using hasattr() because it's a mangled name
            cls.__translator
        except AttributeError:
            cls.__translator = None
        super().__init__(*args, **kwargs)

    @property
    def all_commands(cls) -> Dict[str, Command]:
        return {cmd.name: cmd for _, cmd in inspect.getmembers(cls) if isinstance(cmd, Command)}

    @property
    def qualified_name(cls) -> str:
        return cls.__name__

    @property
    def checks(cls) -> List[Callable[["Context"], Union[bool, Awaitable[bool]]]]:
        return cls.__checks

    async def can_run(cls, ctx: "Context") -> bool:
        """Check if the given context passes this cog class's requirements.

        Raises
        ------
        CommandError
            Any exception which are raised from underlying checks.

        """
        ret = await discord.utils.async_all((pred(ctx) for pred in cls.checks))
        if ret is False:
            return ret
        return await cls.requires.verify(ctx)

    @classmethod
    async def convert(mcs, ctx: "Context", argument: str) -> "Cog":
        cog_instance = ctx.bot.get_cog(argument)
        if cog_instance is None:
            raise discord.ext.commands.BadArgument(_('Cog "argument" not found.'))
        return type(cog_instance)

    def translate(cls, untranslated: str) -> str:
        if cls.__translator is not None:
            return cls.__translator(untranslated)


class Cog(metaclass=CogMeta):
    """Base class for a cog."""

    def __init_subclass__(cls, **kwargs) -> None:
        setattr(cls, f"_{CogMeta.__name__}__translator", kwargs.pop("translator", None))
        super().__init_subclass__(**kwargs)

    @classmethod
    async def convert(cls, ctx: "Context", argument: str) -> "Cog":
        cog_instance = ctx.bot.get_cog(argument)
        if cog_instance is None:
            raise discord.ext.commands.BadArgument(_('Cog "argument" not found.'))
        return cog_instance
