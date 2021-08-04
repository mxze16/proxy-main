import asyncio
import asyncpraw
from asyncpraw import Reddit
import discord
import disputils
import json
import random
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import typing
import datetime
from disputils import BotEmbedPaginator
import os
import traceback
import sys
import discordmongo
from .classes import MXRoleConverter
from .classes import MXDurationConverter
import motor.motor_asyncio
import bson

if __name__ == '__main__':
    os.system('python main.py')

class Events(commands.Cog, description='Events. These are all the events that happen on discord. An example is on_message_delete.'):
    def __init__(self, bot):
        self.bot = bot
        print('Events Active')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        data = await self.bot.log_channels.find(message.guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'Message Deleted',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{message.author}', icon_url=f'{message.author.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{channel.guild.icon_url}')
        embed.add_field(name=f'User', value=f'{message.author.mention}', inline=True)
        embed.add_field(name=f'Message', value=f'{message.content}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print('------')
        current_guilds = len(self.bot.guilds)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'p.help | Serving {current_guilds} guilds.'))
        print(f'Logged in as: {self.bot.user.name}')
        print('Succesful connection to MongoDB.')
        self.bot.reddit_task = asyncpraw.Reddit(
            client_id="A0vipUqVfot8NA",
            client_secret="k1bklpQYMcZtHgFqBfnB_LwBHYE",
            user_agent="paradex"
        )
        print('Successful connection to Reddit.')
        print('------')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(
            title = 'Error Found',
            description = f'This task has come accross an error.',
            colour = self.bot.error_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f'Error Log.')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name=f'Error', value=f'{error}', inline=False)
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        data = await self.bot.log_channels.find(before.guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'Message Edited',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{before.author}', icon_url=f'{before.author.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{channel.guild.icon_url}')
        embed.add_field(name=f'Before', value=f'{before.content}', inline=True)
        embed.add_field(name=f'After', value=f'{after.content}', inline=True)
        embed.add_field(name=f'ID', value=f'{after.id}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        data = await self.bot.log_channels.find(role.guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'Role Created',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{role}', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{channel.guild.icon_url}')
        embed.add_field(name=f'Role', value=f'{role.mention}', inline=True)
        embed.add_field(name=f'ID', value=f'{role.id}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        data = await self.bot.log_channels.find(role.guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'Role Deleted',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{role.name}', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{channel.guild.icon_url}')
        embed.add_field(name=f'Role', value=f'{role.mention}', inline=True)
        embed.add_field(name=f'ID', value=f'{role.id}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        data = await self.bot.log_channels.find(before.guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'Role Updated',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{after}', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{channel.guild.icon_url}')
        embed.add_field(name=f'Before', value=f'{before.mention}', inline=True)
        embed.add_field(name=f'After', value=f'{after.mention}', inline=True)
        embed.add_field(name=f'ID', value=f'{after.id}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        data = await self.bot.log_channels.find(guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'User Banned',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{user}', icon_url=f'{user.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{guild.icon_url}')
        embed.add_field(name=f'User', value=f'{user.mention}', inline=True)
        embed.add_field(name=f'ID', value=f'{user.id}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        data = await self.bot.log_channels.find(guild.id)

        if not data or "channel" not in data:
            return

        channel_id = data["channel"]
        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            title = 'User Unbanned',
            description = f'This task was completed without any errors.',
            colour = self.bot.logging_color
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=f'{user}', icon_url=f'{user.avatar_url}')
        embed.set_footer(text=f'Event logging.')
        embed.set_thumbnail(url=f'{guild.icon_url}')
        embed.add_field(name=f'User', value=f'{user.mention}', inline=True)
        embed.add_field(name=f'ID', value=f'{user.id}', inline=True)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        current_guilds = len(self.bot.guilds)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'p.help | Serving {current_guilds} guilds.'))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        current_guilds = len(self.bot.guilds)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'p.help | Serving {current_guilds} guilds.'))

def setup(bot):
    bot.add_cog(Events(bot))
