import itertools
from discord.ext import commands
from core import checks
from string import ascii_letters, digits
from random import SystemRandom
import logging
import importlib
import sys
import discord
import aiohttp
import asyncio

from core.cog_manager import NoModuleFound

log = logging.getLogger("red")

OWNER_DISCLAIMER = ("⚠ **Only** the person who is hosting Red should be "
                    "owner. **This has SERIOUS security implications. The "
                    "owner can access any data that is present on the host "
                    "system.** ⚠")


class Core:
    """Commands related to core functions"""

    @commands.command()
    @checks.is_owner()
    async def load(self, ctx, *, cog_name: str):
        """Loads a package"""
        try:
            spec = ctx.bot.cog_mgr.find_cog(cog_name)
        except NoModuleFound:
            await ctx.send("No module by that name was found in any"
                           " cog path.")
            return

        try:
            ctx.bot.load_extension(spec)
        except Exception as e:
            log.exception("Package loading failed", exc_info=e)
            await ctx.send("Failed to load package. Check your console or "
                           "logs for details.")
        else:
            await ctx.bot.add_loaded_package(cog_name)
            await ctx.send("Done.")

    @commands.group()
    @checks.is_owner()
    async def unload(self, ctx, *, cog_name: str):
        """Unloads a package"""
        if cog_name in ctx.bot.extensions:
            ctx.bot.unload_extension(cog_name)
            await ctx.bot.remove_loaded_package(cog_name)
            await ctx.send("Done.")
        else:
            await ctx.send("That extension is not loaded.")

    @commands.command(name="reload")
    @checks.is_owner()
    async def _reload(self, ctx, *, cog_name: str):
        """Reloads a package"""
        ctx.bot.unload_extension(cog_name)
        self.cleanup_and_refresh_modules(cog_name)
        try:
            spec = ctx.bot.cog_mgr.find_cog(cog_name)
            ctx.bot.load_extension(spec)
        except Exception as e:
            log.exception("Package reloading failed", exc_info=e)
            await ctx.send("Failed to reload package. Check your console or "
                           "logs for details.")
        else:
            await ctx.bot.remove_loaded_package(cog_name)
            await ctx.send("Done.")

    def cleanup_and_refresh_modules(self, module_name: str):
        """Interally reloads modules so that changes are detected"""
        splitted = module_name.split('.')

        def maybe_reload(new_name):
            try:
                lib = sys.modules[new_name]
            except KeyError:
                pass
            else:
                importlib._bootstrap._exec(lib.__spec__, lib)

        modules = itertools.accumulate(splitted, lambda old, next: "{}.{}".format(old, next))
        for m in modules:
            maybe_reload(m)

        children = {name: lib for name, lib in sys.modules.items() if name.startswith(module_name)}
        for child_name, lib in children.items():
            importlib._bootstrap._exec(lib.__spec__, lib)

    @commands.group(name="set")
    async def _set(self, ctx):
        """Changes Red's settings"""
        if ctx.invoked_subcommand is None:
            await ctx.bot.send_cmd_help(ctx)

    @_set.command()
    @checks.guildowner()
    @commands.guild_only()
    async def adminrole(self, ctx, *, role: discord.Role):
        """Sets the admin role for this server"""
        await ctx.bot.db.guild(ctx.guild).admin_role.set(role.id)
        await ctx.send("The admin role for this server has been set.")

    @_set.command()
    @checks.guildowner()
    @commands.guild_only()
    async def modrole(self, ctx, *, role: discord.Role):
        """Sets the mod role for this server"""
        await ctx.bot.db.guild(ctx.guild).mod_role.set(role.id)
        await ctx.send("The mod role for this server has been set.")

    @_set.command()
    @checks.is_owner()
    async def avatar(self, ctx, url: str):
        """Sets Red's avatar"""
        session = aiohttp.ClientSession()
        async with session.get(url) as r:
            data = await r.read()
        await session.close()

        try:
            await ctx.bot.user.edit(avatar=data)
        except discord.HTTPException:
            await ctx.send("Failed. Remember that you can edit my avatar "
                           "up to two times a hour. The URL must be a "
                           "direct link to a JPG / PNG.")
        except discord.InvalidArgument:
            await ctx.send("JPG / PNG format only.")
        else:
            await ctx.send("Done.")

    @_set.command(name="game")
    @checks.is_owner()
    @commands.guild_only()
    async def _game(self, ctx, *, game: str):
        """Sets Red's playing status"""
        status = ctx.me.status
        game = discord.Game(name=game)
        await ctx.bot.change_presence(status=status, game=game)
        await ctx.send("Game set.")

    @_set.command()
    @checks.is_owner()
    @commands.guild_only()
    async def status(self, ctx, *, status: str):
        """Sets Red's status
        Available statuses:
            online
            idle
            dnd
            invisible"""

        statuses = {
                    "online"    : discord.Status.online,
                    "idle"      : discord.Status.idle,
                    "dnd"       : discord.Status.dnd,
                    "invisible" : discord.Status.invisible
                   }

        game = ctx.me.game

        try:
            status = statuses[status.lower()]
        except KeyError:
            await ctx.bot.send_cmd_help(ctx)
        else:
            await ctx.bot.change_presence(status=status,
                                          game=game)
            await ctx.send("Status changed to %s." % status)

    @_set.command()
    @checks.is_owner()
    @commands.guild_only()
    async def stream(self, ctx, streamer=None, *, stream_title=None):
        """Sets Red's streaming status
        Leaving both streamer and stream_title empty will clear it."""

        status = ctx.me.status

        if stream_title:
            stream_title = stream_title.strip()
            if "twitch.tv/" not in streamer:
                streamer = "https://www.twitch.tv/" + streamer
            game = discord.Game(type=1, url=streamer, name=stream_title)
            await ctx.bot.change_presence(game=game, status=status)
        elif streamer is not None:
            await ctx.bot.send_cmd_help(ctx)
            return
        else:
            await ctx.bot.change_presence(game=None, status=status)
        await ctx.send("Done.")

    @_set.command(name="username", aliases=["name"])
    @checks.is_owner()
    async def _username(self, ctx, *, username: str):
        """Sets Red's username"""
        try:
            await ctx.bot.user.edit(username=username)
        except discord.HTTPException:
            await ctx.send("Failed to change name. Remember that you can "
                           "only do it up to 2 times an hour. Use "
                           "nicknames if you need frequent changes. "
                           "`{}set nickname`".format(ctx.prefix))
        else:
            await ctx.send("Done.")

    @_set.command(name="nickname")
    @checks.admin()
    @commands.guild_only()
    async def _nickname(self, ctx, *, nickname: str):
        """Sets Red's nickname"""
        try:
            await ctx.bot.user.edit(nick=nickname)
        except discord.Forbidden:
            await ctx.send("I lack the permissions to change my own "
                           "nickname.")
        else:
            await ctx.send("Done.")

    @_set.command(aliases=["prefixes"])
    @checks.is_owner()
    async def prefix(self, ctx, *prefixes):
        """Sets Red's global prefix(es)"""
        if not prefixes:
            await ctx.bot.send_cmd_help(ctx)
            return
        prefixes = sorted(prefixes, reverse=True)
        await ctx.bot.db.prefix.set(prefixes)
        await ctx.send("Prefix set.")

    @_set.command(aliases=["serverprefixes"])
    @checks.admin()
    @commands.guild_only()
    async def serverprefix(self, ctx, *prefixes):
        """Sets Red's server prefix(es)"""
        if not prefixes:
            await ctx.bot.db.guild(ctx.guild).prefix.set([])
            await ctx.send("Server prefixes have been reset.")
            return
        prefixes = sorted(prefixes, reverse=True)
        await ctx.bot.db.guild(ctx.guild).prefix.set(prefixes)
        await ctx.send("Prefix set.")

    @_set.command()
    @commands.cooldown(1, 60 * 10, commands.BucketType.default)
    async def owner(self, ctx):
        """Sets Red's main owner"""
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # According to the Python docs this is suitable for cryptographic use
        random = SystemRandom()
        length = random.randint(25, 35)
        chars = ascii_letters + digits
        token = ""

        for i in range(length):
            token += random.choice(chars)
        log.info("{0} ({0.id}) requested to be set as owner."
                 "".format(ctx.author))
        print("\nVerification token:")
        print(token)

        await ctx.send("Remember:\n" + OWNER_DISCLAIMER)
        await asyncio.sleep(5)

        await ctx.send("I have printed a one-time token in the console. "
                       "Copy and paste it here to confirm you are the owner.")

        try:
            message = await ctx.bot.wait_for("message", check=check,
                                             timeout=60)
        except asyncio.TimeoutError:
            self.owner.reset_cooldown(ctx)
            await ctx.send("The set owner request has timed out.")
        else:
            if message.content.strip() == token:
                self.owner.reset_cooldown(ctx)
                await ctx.bot.db.owner.set(ctx.author.id)
                ctx.bot.owner_id = ctx.author.id
                await ctx.send("You have been set as owner.")
            else:
                await ctx.send("Invalid token.")
