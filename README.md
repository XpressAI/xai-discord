# Xircuits Discord Component Library

Xircuits component library to interface with Discord! Uses [discord.py](https://github.com/Rapptz/discord.py) as backend.


![helloXircuitsDiscord](https://user-images.githubusercontent.com/68586800/232559150-593258f0-dfd7-43d5-9afa-069210bd6787.gif)

### Computer Vision Example
![DiscordCVBot](https://user-images.githubusercontent.com/68586800/232880388-0a999fa2-f9cf-40df-be51-73601afc8963.gif)


## Installation

```
pip install -r requirements.txt
```

To use this component library, simply copy the directory / clone or submodule the repository to your working Xircuits project directory.


## Discord Related Setup

### Obtaining the Bot Token

1. Log in to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on the "New Application" button in the top-right corner.
3. Enter a name for your application and click "Create".
4. In the application's settings, navigate to the "Bot" tab.
5. You will need to enable some `Privileged Gateway Intents` to enable bot interation. For this component library, `MESSAGE CONTENT INTENT` should be enough.
6. Under the "Token" section, click "Copy" to copy the bot token to your clipboard. You may need to Reset the token if it is a new bot.

### Obtaining the Channel ID

1. Open the Discord client and navigate to the server where your bot is a member.
2. Right-click on the desired text channel and click "Copy ID".
   - If you don't see the "Copy ID" option, enable Developer Mode in Discord:
     1. Click the gear icon in the bottom-left corner to open "User Settings".
     2. In the "App Settings" tab, scroll down to the "Advanced" section.
     3. Toggle the "Developer Mode" switch.

### Inviting the Bot to a Server

1. In the [Discord Developer Portal](https://discord.com/developers/applications), navigate to your application's settings.
2. Click on the "OAuth2" tab.
3. Update the "Scopes" section and then the "Bot Permissions" section. Below is the config we have used:

    #### Scopes:

    - bot: For OAuth2 bots, this puts the bot in the user's selected guild by default.
    - applications.commands: Allows your app to use commands in a guild.

    #### Bot Permissions:

    - View Channels: Allows the bot to view the channels in the server.
    - Send Messages: Allows the bot to send messages in text channels.
    - Read Message History: Allows the bot to read the message history of text channels.

4. Copy the generated URL from the "Scopes" section and paste it into your browser.
5. Follow the prompts to authorize your bot and add it to your desired server.