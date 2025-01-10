
<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/68586800/232997216-5248081f-86a4-484d-bc87-78ee19f6d255.png" width="450"/>
</p>



<p align="center">Xircuits Component Library to interface with Discord! Create Discord Bots in seconds.</br>Uses <a href="https://github.com/Rapptz/discord.py">discord.py</a> as backend.</p>


---
## Xircuits Component Library for Discord

This library enables Xircuits to integrate with Discord, allowing seamless interaction with Discord bots and servers. It simplifies managing bot tokens, sending and receiving messages, and handling events in Discord channels and threads.

## Table of Contents

- [Preview](#preview)
- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Try the Examples](#try-the-examples)
- [Installation](#installation)

## Preview

### Discord Bot Branch Example

![DiscordBotBranchExample](https://github.com/user-attachments/assets/02002e08-7563-4459-96a6-9e7d4f05d490)

### Discord Bot Branch Result

![DiscordBotBranchExample_result](https://github.com/user-attachments/assets/403da056-f383-479a-a198-45834be61d05)

### Discord Bot Computer Vision Example

![DiscordBotCVisionExample](https://github.com/user-attachments/assets/192040bb-e7b8-41ad-ad77-f3c89cb1836e)

### Discord Bot Computer Vision Result

![DiscordBotCVisionExample_result](https://github.com/user-attachments/assets/08b78d39-1f0a-499b-8321-f3277dd44a88)

### Discord Bot Message Responder Example

![DiscordBotMessageResponder](https://github.com/user-attachments/assets/8d575682-656e-4605-b4d1-6467346bc4b5)

### Discord Bot Message Responder Result

![DiscordBotMessageResponder_result](https://github.com/user-attachments/assets/d57e44fa-cf32-4962-833f-906b3c9796f8)

## Prerequisites

Before you begin, you will need the following:

1. Python3.9+.
2. Xircuits.

## Main Xircuits Components

### DiscordMessageResponder Component:  
Adds a message responder that listens for a specific trigger message and responds with a predefined response. Multiple triggers and responses can be configured.

<img src="https://github.com/user-attachments/assets/2ca78a8d-8186-429f-97f7-ada86653ab44" alt="DiscordMessageResponder" width="200" height="100" />

### DiscordPostMessage Component:  
Sends a message, with an optional attachment, as a reply to the original Discord message. Can include files in the response.

<img src="https://github.com/user-attachments/assets/c2b6d2cf-f3ca-4412-ba28-99723b5a3974" alt="DiscordPostMessage" width="200" height="125" />

### DiscordClientInit Component:  
Initializes a Discord client with default intents, enabling message content handling. Adds the client to the context for further use.

### DiscordShutdownBot Component:  
Adds a shutdown command to the bot, allowing administrators to shut down the bot by sending a specific message.

### DiscordDeployBot Component:  
Deploys the Discord bot using the provided token. It runs the bot either in a standalone script or within Xircuits, handling events such as incoming messages.

### DiscordTriggerBranch Component:  
Listens for a specific trigger message and executes a connected component when the trigger is detected. Outputs the received message and its processed content.

### DiscordEchoMessage Component:  
Takes a Discord message as input and constructs an echo response by prepending "You said:" to the message content.

### DiscordProcessImage Component:  
Processes an image attachment from a Discord message triggered by a specified message. Outputs the image data and triggers a connected component for further processing.

## Try The Examples

We have provided an example workflow to help you get started with the Discord component library. Give it a try and see how you can create custom Discord components for your applications.

### Discord Bot Branch Example

The `DiscordBotBranchExample.xircuits` workflow creates a Discord bot that listens for messages starting with `@test` and replies with "You have said: [message]". It can also shut down using the command `$ayonara`.

### Discord Bot Computer Vision Example

The `DiscordBotCVisionExample.xircuits` workflow creates a Discord bot that listens for the command `$predict` with an image attachment. The bot processes the image using a MobileNetV2 model for predictions and responds with the predicted class. It also includes a shutdown command `$ayonara`.

Additional Example Requirement: 
```
pip install  torch==2.4.1 torchvision==0.19.1
```

### Discord Bot Message Responder Example

The `DiscordBotMessageResponder.xircuits` workflow sets up a Discord bot that listens for specific text commands and responds with predefined messages. For instance:

- `$test`: The bot replies with "it works!".
- `$Hello there!`: The bot replies with "General Kenobi!".

Additionally, the bot can be shut down using the `$ayonara` command.

## Installation

To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then pull and install this library using:

```
xircuits-submodules xai_discord
```

Otherwise you can do it manually by cloning and installing it.

```
# base Xircuits directory
git clone https://github.com/XpressAI/xai-discord xai_components/xai_discord
pip install -r xai_components/xai_discord/requirements.txt
```



## Discord Related Setup

### Obtaining the Bot Token

1. Log in to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on the "New Application" button in the top-right corner.
3. Enter a name for your application and click "Create".
4. In the application's settings, navigate to the "Bot" tab.
5. You will need to enable some `Privileged Gateway Intents` to enable bot interation. For this component library, `MESSAGE CONTENT INTENT` should be enough.
6. Under the "Token" section, click "Copy" to copy the bot token to your clipboard. You may need to Reset the token if it is a new bot.

### Inviting the Bot to a Server

1. In the [Discord Developer Portal](https://discord.com/developers/applications), navigate to your application's settings.
2. Click on the "OAuth2" tab.
3. Update the "Scopes" section and then the "Bot Permissions" section. Below is the config we have used:
    #### Scopes:
    - bot: For OAuth2 bots, this puts the bot in the user's selected guild by default.
    - applications.commands: Allows your app to use commands in a guild.
    #### Bot Permissions:
    - Read Messages / View Channels: Allows the bot to read and view the channels in the server.
    - Send Messages: Allows the bot to send messages in text channels.
    - Read Message History: Allows the bot to read the message history of text channels.
    
4. Copy the generated URL from the "Scopes" section and paste it into your browser.
5. Follow the prompts to authorize your bot and add it to your desired server.


## Developers Discord
Play with our Discord bot, Xaibo [here](https://discord.gg/dK8jgknkG6).
The devs at there too.
