################################################
#          SENSITIVE SECTION WARNING           #
################################################
# Any edits of any of the exported names       #
# may result in a breaking change.             #
# Ensure no names are removed without warning. #
################################################

from .commands import (
    Cog,
    CogMixin,
    CogCommandMixin,
    CogGroupMixin,
    Command,
    Group,
    GroupCog,
    GroupMixin,
    command,
    HybridCommand,
    HybridGroup,
    hybrid_command,
    hybrid_group,
    group,
    RedUnhandledAPI,
    RESERVED_COMMAND_NAMES,
)
from .context import Context, GuildContext, DMContext
from .converter import (
    DictConverter,
    RelativedeltaConverter,
    TimedeltaConverter,
    get_dict_converter,
    get_timedelta_converter,
    parse_relativedelta,
    parse_timedelta,
    NoParseOptional,
    UserInputOptional,
    RawUserIdConverter,
    CogConverter,
    CommandConverter,
)
from .errors import (
    BotMissingPermissions,
    UserFeedbackCheckFailure,
    ArgParserFailure,
)
from .help import (
    red_help,
    RedHelpFormatter,
    HelpSettings,
)
from .requires import (
    CheckPredicate,
    GlobalPermissionModel,
    GuildPermissionModel,
    PermissionModel,
    PrivilegeLevel,
    PermState,
    Requires,
    permissions_check,
    bot_has_permissions,
    bot_in_a_guild,
    bot_can_manage_channel,
    bot_can_react,
    has_permissions,
    can_manage_channel,
    has_guild_permissions,
    is_owner,
    guildowner,
    guildowner_or_can_manage_channel,
    guildowner_or_permissions,
    admin,
    admin_or_can_manage_channel,
    admin_or_permissions,
    mod,
    mod_or_can_manage_channel,
    mod_or_permissions,
)

# DEP-WARN: Check this *every* discord.py update
from discord.ext.commands import (
    BadArgument,
    EmojiConverter,
    GuildConverter,
    InvalidEndOfQuotedStringError,
    MemberConverter,
    BotMissingRole,
    PrivateMessageOnly,
    HelpCommand,
    MinimalHelpCommand,
    DisabledCommand,
    ExtensionFailed,
    Bot,
    NotOwner,
    CategoryChannelConverter,
    CogMeta,
    ConversionError,
    UserInputError,
    Converter,
    InviteConverter,
    ExtensionError,
    Cooldown,
    CheckFailure,
    PartialMessageConverter,
    MessageConverter,
    MissingPermissions,
    BadUnionArgument,
    DefaultHelpCommand,
    ExtensionNotFound,
    UserConverter,
    MissingRole,
    CommandOnCooldown,
    MissingAnyRole,
    ExtensionNotLoaded,
    clean_content,
    CooldownMapping,
    ArgumentParsingError,
    RoleConverter,
    CommandError,
    TextChannelConverter,
    UnexpectedQuoteError,
    Paginator,
    BucketType,
    NoEntryPointError,
    CommandInvokeError,
    TooManyArguments,
    Greedy,
    ExpectedClosingQuoteError,
    ColourConverter,
    ColorConverter,
    VoiceChannelConverter,
    StageChannelConverter,
    NSFWChannelRequired,
    IDConverter,
    MissingRequiredArgument,
    GameConverter,
    CommandNotFound,
    BotMissingAnyRole,
    NoPrivateMessage,
    AutoShardedBot,
    ExtensionAlreadyLoaded,
    PartialEmojiConverter,
    check_any,
    max_concurrency,
    CheckAnyFailure,
    MaxConcurrency,
    MaxConcurrencyReached,
    bot_has_guild_permissions,
    CommandRegistrationError,
    GuildNotFound,
    MessageNotFound,
    MemberNotFound,
    UserNotFound,
    ChannelNotFound,
    ChannelNotReadable,
    BadColourArgument,
    RoleNotFound,
    BadInviteArgument,
    EmojiNotFound,
    PartialEmojiConversionFailure,
    BadBoolArgument,
    TooManyFlags,
    MissingRequiredFlag,
    flag,
    FlagError,
    ObjectNotFound,
    GuildStickerNotFound,
    ThreadNotFound,
    GuildChannelConverter,
    run_converters,
    Flag,
    BadFlagArgument,
    BadColorArgument,
    dynamic_cooldown,
    BadLiteralArgument,
    DynamicCooldownMapping,
    ThreadConverter,
    GuildStickerConverter,
    ObjectConverter,
    FlagConverter,
    MissingFlagArgument,
    ScheduledEventConverter,
    ScheduledEventNotFound,
    check,
    guild_only,
    cooldown,
    dm_only,
    is_nsfw,
    has_role,
    has_any_role,
    bot_has_role,
    when_mentioned_or,
    when_mentioned,
    bot_has_any_role,
    before_invoke,
    after_invoke,
    CurrentChannel,
    Author,
    param,
    MissingRequiredAttachment,
    Parameter,
    ForumChannelConverter,
    CurrentGuild,
    Range,
    RangeError,
    parameter,
    HybridCommandError,
)

__all__ = (
    # .commands
    "Cog",
    "CogMixin",
    "CogCommandMixin",
    "CogGroupMixin",
    "Command",
    "Group",
    "GroupCog",
    "GroupMixin",
    "command",
    "HybridCommand",
    "HybridGroup",
    "hybrid_command",
    "hybrid_group",
    "group",
    "RedUnhandledAPI",
    "RESERVED_COMMAND_NAMES",
    # .context
    "Context",
    "GuildContext",
    "DMContext",
    # .converter
    "DictConverter",
    "RelativedeltaConverter",
    "TimedeltaConverter",
    "get_dict_converter",
    "get_timedelta_converter",
    "parse_relativedelta",
    "parse_timedelta",
    "NoParseOptional",
    "UserInputOptional",
    "RawUserIdConverter",
    "CogConverter",
    "CommandConverter",
    # .errors
    "BotMissingPermissions",
    "UserFeedbackCheckFailure",
    "ArgParserFailure",
    # .help
    "red_help",
    "RedHelpFormatter",
    "HelpSettings",
    # .requires
    "CheckPredicate",
    "GlobalPermissionModel",
    "GuildPermissionModel",
    "PermissionModel",
    "PrivilegeLevel",
    "PermState",
    "Requires",
    "permissions_check",
    "bot_has_permissions",
    "bot_in_a_guild",
    "bot_can_manage_channel",
    "bot_can_react",
    "has_permissions",
    "can_manage_channel",
    "has_guild_permissions",
    "is_owner",
    "guildowner",
    "guildowner_or_can_manage_channel",
    "guildowner_or_permissions",
    "admin",
    "admin_or_can_manage_channel",
    "admin_or_permissions",
    "mod",
    "mod_or_can_manage_channel",
    "mod_or_permissions",
    # discord.ext.commands
    "BadArgument",
    "EmojiConverter",
    "GuildConverter",
    "InvalidEndOfQuotedStringError",
    "MemberConverter",
    "BotMissingRole",
    "PrivateMessageOnly",
    "HelpCommand",
    "MinimalHelpCommand",
    "DisabledCommand",
    "ExtensionFailed",
    "Bot",
    "NotOwner",
    "CategoryChannelConverter",
    "CogMeta",
    "ConversionError",
    "UserInputError",
    "Converter",
    "InviteConverter",
    "ExtensionError",
    "Cooldown",
    "CheckFailure",
    "PartialMessageConverter",
    "MessageConverter",
    "MissingPermissions",
    "BadUnionArgument",
    "DefaultHelpCommand",
    "ExtensionNotFound",
    "UserConverter",
    "MissingRole",
    "CommandOnCooldown",
    "MissingAnyRole",
    "ExtensionNotLoaded",
    "clean_content",
    "CooldownMapping",
    "ArgumentParsingError",
    "RoleConverter",
    "CommandError",
    "TextChannelConverter",
    "UnexpectedQuoteError",
    "Paginator",
    "BucketType",
    "NoEntryPointError",
    "CommandInvokeError",
    "TooManyArguments",
    "Greedy",
    "ExpectedClosingQuoteError",
    "ColourConverter",
    "ColorConverter",
    "VoiceChannelConverter",
    "StageChannelConverter",
    "NSFWChannelRequired",
    "IDConverter",
    "MissingRequiredArgument",
    "GameConverter",
    "CommandNotFound",
    "BotMissingAnyRole",
    "NoPrivateMessage",
    "AutoShardedBot",
    "ExtensionAlreadyLoaded",
    "PartialEmojiConverter",
    "check_any",
    "max_concurrency",
    "CheckAnyFailure",
    "MaxConcurrency",
    "MaxConcurrencyReached",
    "bot_has_guild_permissions",
    "CommandRegistrationError",
    "GuildNotFound",
    "MessageNotFound",
    "MemberNotFound",
    "UserNotFound",
    "ChannelNotFound",
    "ChannelNotReadable",
    "BadColourArgument",
    "RoleNotFound",
    "BadInviteArgument",
    "EmojiNotFound",
    "PartialEmojiConversionFailure",
    "BadBoolArgument",
    "TooManyFlags",
    "MissingRequiredFlag",
    "flag",
    "FlagError",
    "ObjectNotFound",
    "GuildStickerNotFound",
    "ThreadNotFound",
    "GuildChannelConverter",
    "run_converters",
    "Flag",
    "BadFlagArgument",
    "BadColorArgument",
    "dynamic_cooldown",
    "BadLiteralArgument",
    "DynamicCooldownMapping",
    "ThreadConverter",
    "GuildStickerConverter",
    "ObjectConverter",
    "FlagConverter",
    "MissingFlagArgument",
    "ScheduledEventConverter",
    "ScheduledEventNotFound",
    "check",
    "guild_only",
    "cooldown",
    "dm_only",
    "is_nsfw",
    "has_role",
    "has_any_role",
    "bot_has_role",
    "when_mentioned_or",
    "when_mentioned",
    "bot_has_any_role",
    "before_invoke",
    "after_invoke",
    "CurrentChannel",
    "Author",
    "param",
    "MissingRequiredAttachment",
    "Parameter",
    "ForumChannelConverter",
    "CurrentGuild",
    "Range",
    "RangeError",
    "parameter",
    "HybridCommandError",
)
