from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component

import discord
from discord.ext import commands

import asyncio
import os

@xai_component
class DiscordClient(Component):
    token: InArg[str]
    client: OutArg[discord.Client]

    def __init__(self):
        super().__init__()
        self.token.value = os.getenv("DISCORD_TOKEN", "")

    def execute(self, ctx) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        self.client.value = discord.Client(intents=intents)

        @self.client.value.event
        async def on_ready():
            print(f'We have logged in as {self.client.value.user}')
        
        # Get the current event loop and run the Discord bot within it
        loop = asyncio.get_event_loop()
        loop.create_task(self.client.value.start(self.token.value))


@xai_component
class DiscordHelloXircuits(Component):
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