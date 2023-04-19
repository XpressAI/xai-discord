from xai_components.base import InArg, OutArg, InCompArg, BaseComponent, Component, xai_component
from discord import File
import discord

import asyncio
import os

@xai_component
class DiscordClientInit(Component):
    """
    Initializes a Discord client with the default intents and enables message content.

    ##### ctx:
    - discord_client: A Discord client instance with the default intents and message content enabled.
    """

    def execute(self, ctx) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'We have logged in as {client.user}')

        ctx['discord_client'] = client


@xai_component
class DiscordMessageResponder(Component):
    """
    Adds a message responder that listens for a specified trigger message and responds with the specified response.

    ##### inPorts:
    - msg_trigger: The message trigger that the bot listens for.
    - msg_response: The response the bot sends when the trigger is detected.

    ##### ctx:
    - message_responders: A list of tuples containing message triggers and their corresponding responses.
    - on_message_handlers: A list of message handling functions that are called when a message is received.
    """

    msg_trigger: InCompArg[str]
    msg_response: InCompArg[str]

    def execute(self, ctx) -> None:
        client = ctx['discord_client']

        if 'message_responders' not in ctx:
            ctx['message_responders'] = []

        trigger_response = (self.msg_trigger.value, self.msg_response.value)
        ctx['message_responders'].append(trigger_response)

        if 'on_message_handlers' not in ctx:
            ctx['on_message_handlers'] = []

        if 'message_responder' not in ctx:
            async def message_responder(message):
                for trigger, response in ctx['message_responders']:
                    if message.content.startswith(trigger):
                        await message.channel.send(response, reference=message)
                        break

            ctx['message_responder'] = message_responder

            if message_responder not in ctx['on_message_handlers']:
                ctx['on_message_handlers'].append(message_responder)



@xai_component
class DiscordShutdownBot(Component):
    """
    Adds a shutdown command for the Discord bot that can be executed by an administrator.

    ##### inPorts:
    - shutdown_cmd: The command that, when received from an administrator, will shut down the bot.

    ##### ctx:
    - on_message_handlers: A list of message handling functions that are called when a message is received.
    """
    shutdown_cmd: InCompArg[str]

    def execute(self, ctx) -> None:
        client = ctx['discord_client']

        async def shutdown_bot(message):
            if message.content.startswith(self.shutdown_cmd.value) and message.author.guild_permissions.administrator:
                await message.channel.send("Shutting down...", reference=message)

                await client.close()

        if 'on_message_handlers' not in ctx:
            ctx['on_message_handlers'] = []

        ctx['on_message_handlers'].append(shutdown_bot)


@xai_component
class DiscordDeployBot(Component):
    """
    Deploys the Discord bot using the provided token, running either in Xircuits or as a standalone script.

    ##### inPorts:
    - token: The bot token to be used for authentication. 
        If not provided, will search for 'DISCORD_BOT_TOKEN' from env.

    ##### ctx:
    - on_message_handlers: A list of message handling functions that are called when a message is received.
    """

    token: InArg[str]

    def execute(self, ctx) -> None:
        client = ctx['discord_client']
        token = os.getenv("DISCORD_BOT_TOKEN") if self.token.value is None else self.token.value

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            if 'on_message_handlers' in ctx:
                for handler in ctx['on_message_handlers']:
                    await handler(message)

        if "JPY_PARENT_PID" in os.environ or "jupyter" in os.environ.get("PATH", ""):
            # If running in Jupyter, get the current event loop and run the Discord bot within it
            loop = asyncio.get_event_loop()
            loop.create_task(client.start(token))
        else:
            # If running as a standalone script, use client.run()
            client.run(token)

@xai_component
class DiscordTriggerBranch(Component):
    """
    This component listens for a specified message trigger and, when detected, 
    executes the provided on_message component, passing the received message as input.

    ##### inPorts:
    - on_message: A BaseComponent to be executed when the message trigger is detected.
    - msg_trigger (str): The message trigger that the bot listens for.

    ##### outPorts:
    - discord_msg: The received message that triggered the on_message component.

    ##### ctx:
    - on_message_handlers: A list of message handling functions that are called when a message is received.
    """
    on_message: BaseComponent
    msg_trigger: InCompArg[str]
    discord_msg: OutArg[discord.message.Message]

    def execute(self, ctx) -> None:

        if 'on_message_handlers' not in ctx:
            ctx['on_message_handlers'] = []

        async def trigger_branch_handler(message):
            if message.content.startswith(self.msg_trigger.value):
                
                self.discord_msg.value = message
                self.on_message.do(ctx)

        ctx['on_message_handlers'].append(trigger_branch_handler)


@xai_component
class DiscordEchoMessage(Component):
    """
    This component takes a Discord message as input and creates an echo response by 
    concatenating "You said: " with the message content.

    ##### inPorts:
    - discord_msg: The received Discord message.

    ##### outPorts:
    - msg (str): The constructed echo response.
    """
    discord_msg: InCompArg[discord.message.Message]
    msg: OutArg[str]

    def execute(self, ctx) -> None:

        message = self.discord_msg.value
        self.msg.value = "You said: " + str(message.content)


@xai_component
class DiscordMessage2Str(Component):
    """Util that removes the leading trigger string from a Discord message input.
    
    EG: 
    Trigger: @Xaibot
    User Input: @Xaibot Predict this image!
    msg: Predict this image!

    ##### inPorts:
    - discord_msg: Input Discord message.
    - msg_trigger(str): Trigger string to remove.

    ##### outPorts:
    - msg(str): Modified message.
    """
    discord_msg: InCompArg[discord.message.Message]
    msg_trigger: InCompArg[str]
    msg: OutArg[str]

    def execute(self, ctx) -> None:
        discord_msg = str(self.discord_msg.value.content)
        self.msg.value  = discord_msg.replace(self.msg_trigger.value, "", 1).strip()

@xai_component
class DiscordPostMessage(Component):
    """
    Sends a message with an optional attachment to the same channel as the received Discord message.
    It uses the provided message as the response and references the original message in the reply.

    ##### inPorts:
    - msg_response: The response message to be sent.
    - discord_msg (str): The original Discord message that the bot is replying to.
    - attachment_path (str): The local path to the file to be sent as an attachment. Defaults to None.
    """

    msg_response: InCompArg[str]
    discord_msg: InCompArg[discord.message.Message]
    attachment_path: InArg[str]

    def execute(self, ctx) -> None:

        message = self.discord_msg.value
        response = self.msg_response.value

        if self.attachment_path.value:
            file = File(self.attachment_path.value)
            asyncio.ensure_future(message.channel.send(response, reference=message, files=[file]))
        else:
            asyncio.ensure_future(message.channel.send(response, reference=message))

@xai_component
class DiscordProcessImage(Component):
    """Processes an image attachment from a Discord message and triggers the 'on_message' component.

    ##### inPorts:
    - msg_trigger: String representing the message trigger.

    ##### outPorts:
    - discord_msg: The processed Discord message.
    - image_data: Image data in bytes.

    """

    on_message: BaseComponent
    msg_trigger: InCompArg[str]
    discord_msg: OutArg[discord.message.Message]
    image_data: OutArg[bytes]

    def execute(self, ctx) -> None:

        import aiohttp

        if 'on_message_handlers' not in ctx:
            ctx['on_message_handlers'] = []

        async def process_image_handler(message):
            if message.content.startswith(self.msg_trigger.value):
                if message.attachments:
                    attachment = message.attachments[0]
                    if attachment.content_type.startswith("image/"):
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                self.image_data.value = await resp.read()

                self.discord_msg.value = message
                self.on_message.do(ctx)

        ctx['on_message_handlers'].append(process_image_handler)