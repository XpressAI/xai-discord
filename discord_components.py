from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component

import discord
from discord.ext import commands

import asyncio
import os

@xai_component
class DiscordClient(Component):
    client: OutArg[discord.Client]

    def execute(self, ctx) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.client.value = discord.Client(intents=intents)

        @self.client.value.event
        async def on_ready():
            print(f'We have logged in as {self.client.value.user}')

        ctx['discord_client'] = self.client.value


@xai_component
class DiscordMessageResponder(Component):
    client: InArg[discord.Client]
    msg_trigger: InArg[str]
    msg_response: InArg[str]
    
    def __init__(self):
        super().__init__()
        self.msg_trigger.value = '$Hello'  
        self.msg_response.value = "Hello, I'm Xircuits Discord Bot!"
    
    def execute(self, ctx) -> None:

        @self.client.value.event
        async def on_message(message):
            if message.author == self.client.value.user:
                return

            if message.content.startswith(self.msg_trigger.value):
                await message.channel.send(self.msg_response.value)

@xai_component
class DiscordDeployBot(Component):
    token: InArg[str]
    client: InArg[discord.Client]

    def execute(self, ctx) -> None:
        token = os.getenv("DISCORD_BOT_TOKEN") if self.token.value is None else self.token.value

        if "JPY_PARENT_PID" in os.environ or "jupyter" in os.environ.get("PATH", ""):
            # If running in Jupyter, get the current event loop and run the Discord bot within it
            loop = asyncio.get_event_loop()
            loop.create_task(self.client.value.start(token))
        else:
            # If running as a standalone script, use client.run()
            self.client.value.run(token)