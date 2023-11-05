import discord
import os
import urllib.parse
import time
import re
import asyncio
from discord.ext import commands
from datetime import datetime, timezone, timedelta
import tkinter as tk
from tkinter import ttk
import threading
import tqdm


# Function to read the bot token from "token.txt" file
def read_token(filename="token.txt"):
    with open(filename, "r") as file:
        return file.read().strip()



spoilers = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| ||"


def apply_minecraft_colors(text):
    color_codes = {
        "§0": "\x1b[30m",  # Black
        "§1": "\x1b[34m",  # Dark Blue
        "§2": "\x1b[32m",  # Dark Green
        "§3": "\x1b[36m",  # Dark Aqua
        "§4": "\x1b[31m",  # Dark Red
        "§5": "\x1b[35m",  # Dark Purple
        "§6": "\x1b[33m",  # Gold
        "§7": "\x1b[37m",  # Gray
        "§8": "\x1b[30;1m",  # Dark Gray (Bold)
        "§9": "\x1b[34;1m",  # Blue (Bold)
        "§a": "\x1b[32;1m",  # Green (Bold)
        "§b": "\x1b[36;1m",  # Aqua (Bold)
        "§c": "\x1b[31;1m",  # Red (Bold)
        "§d": "\x1b[35;1m",  # Light Purple (Bold)
        "§e": "\x1b[33;1m",  # Yellow (Bold)
        "§f": "\x1b[37;1m",  # White (Bold)
        "§n": "\x1b[4m",  # Underline
        "§l": "\x1b[1m",  # Bold
        "§r": "\x1b[0m",  # Reset
    }

    for code, ansi_code in color_codes.items():
        text = text.replace(code, ansi_code)

    # Reset color and formatting at the end of the text
    text += "\x1b[0m"

    return text
  




def blue_hyperlinks(text):
    # Split the text into words
    words = text.split()

    blue_words = []
    for word in words:
        # Check if the word is an emoji (already enclosed in colons)
        if re.match(r':[^:]+:', word):
            blue_words.append(word)
        else:
            # Escape colons in the word and add a blue hyperlink
            escaped_word = word.replace(":", r"\:")
            blue_words.append(f"[{escaped_word}](http://blue)")

    # Join the blue words to form the modified text
    modified_text = " ".join(blue_words)

    return modified_text


def custom_quote(s):
    """Custom quoting function that doesn't encode Latin letters and numbers."""
    return urllib.parse.quote(
        s,
        safe="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")


# Retrieve the token from the Replit secret
TOKEN = read_token()
PREFIX = "/"
long = "﷽"

# Define the list of words to search for in messages
# Add your violation words here

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, self_bot=True, intents=discord.Intents.all())

@bot.command()
async def findviolations(ctx):
    await ctx.message.delete()
    violation_words = violation_words = [
        "nigg", "kys", "cracka", "white cracker", "child porn", "gore", "porn",
        "kill all", "kam", "no right", "heil hitler", "hail hitler",
        "sieg heil", "sieg hail", "sea kyle", "gas the jews", "pussy", "dick"
    ]  # Add your violation words here
    violations = []

    async for message in ctx.channel.history(limit=5000):
        content = message.content.lower(
        )  # Convert message content to lowercase for case-insensitive search

        # Check if any of the violation words are present in the message content
        if any(word in content for word in violation_words):
            violations.append(message.author.name + ": " + message.content)

    if violations:
        violation_msg = "Messages containing violations:\n"
        violation_msg += "\n".join(map(str, violations))
        await print(violation_msg)
    else:
        await ctx.send("No violations found in the chat.")

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is 🔁 and the user is not a bot
    if str(reaction.emoji) == '🔁' and not user.bot:
        # Check if the reacted message is a ping
        if user.mentioned_in(reaction.message):
            # Send a ping to the same user and delete it after a brief delay
            ping_message = await reaction.message.channel.send(user.mention)
            await asyncio.sleep(2)  # Adjust the delay duration as needed
            await ping_message.delete()

            # Remove the reaction
            await reaction.remove(user)
            await reaction.message.remove_reaction('🔁', bot.user)

# Rest of your code...




@bot.event
async def on_ready():
    print(f'{bot.user.name}')


@bot.command()
async def embed(ctx, *, args):
    await ctx.message.delete()
    arg_list = args.split('\n')
    params = {'color': '#ffffff'}

    for arg in arg_list:
        key, value = arg.split(':', 1)
        params[key.strip().lower()] = value.strip()

    url = (f"https://appembed.netlify.app/e?"
           f"title={custom_quote(params.get('title', ''))}&"
           f"description={custom_quote(params.get('description', ''))}&"
           f"color={custom_quote(params['color'])}")

    optional_params = [
        'redirect', 'provider', 'author', 'image', 'author_url', 'icon'
    ]
    for param in optional_params:
        if param in params:
            url += f"&{custom_quote(param)}={custom_quote(params[param])}"

    await ctx.send(spoilers + url)




@bot.command()
async def status(ctx, *, args):
    args = args.split(' ')
    if args[0].lower() in ['online', 'idle', 'dnd', 'invisible']:
        status = args[0].lower()
        await bot.change_presence(status=discord.Status[status])
        await ctx.message.delete()
        message = None

        if status == 'online':
            message = spoilers + "https://appembed.netlify.app/e?title=&description=Successfully%20set%20status%20to%3A%20Online%20%F0%9F%9F%A9&color=%2323a55a&author=Online%20Status"
        elif status == 'idle':
            message = spoilers + "https://appembed.netlify.app/e?title=&description=Successfully%20set%20status%20to%3A%20Idle%20%F0%9F%9F%A8&color=%23f0b232&author=Idle%20Status"
        elif status == 'dnd':
            message = spoilers + "https://appembed.netlify.app/e?title=&description=Successfully%20set%20status%20to%3A%20Do%20not%20Disturb%20%F0%9F%9F%A5&color=%23f23f43&author=Do%20Not%20Disturb%20Status"
        elif status == 'invisible':
            message = spoilers + "https://appembed.netlify.app/e?title=&description=Successfully%20set%20status%20to%3A%20Invisible%20%E2%AC%9C&color=%23949ba4&author=Invisible%20Status"

        if message:
            await ctx.send(message)
    elif args[0].lower() == 'streaming':
        if len(args) >= 3:
            stream_activity = discord.Streaming(name=args[1], url=args[2])
            await bot.change_presence(activity=stream_activity)
            await ctx.message.delete()
            message = spoilers + "https://appembed.netlify.app/e?title=&description=Successfully%20set%20status%20to%3A%20Streaming%20%F0%9F%9F%AA&color=%23593695&author=Streaming%20Status"
            await ctx.send(message)
        else:
            await ctx.send(
                "Usage: `/status streaming <streamname> <streamurl>`")
    else:
        await ctx.send(
            "Invalid status. Please use one of the following: online, idle, dnd, invisible, or streaming."
        )


@bot.command()
async def block(ctx, member: discord.Member):
    await member.block(member.name)
    await ctx.send(f"Blocked user: {member.name}")


@bot.command()
async def unblock(ctx, member: discord.User):
    await bot.http.unblock_user(member.id)
    await ctx.send(f"Unblocked user: {member.name}")


@bot.command()
async def about(ctx):
    # Get your own user data
    user = ctx.author

    # Map Nitro type integers to human-readable names
    nitro_type_mapping = {
        0: "None",
        1: "Nitro Classic",
        2: "Nitro",
        3: "Nitro Basic"
    }

    # Create a message to display the data
    message = f"**## About Me**\n"
    message += f"• **Account Creation Date:** {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"• **Username:** {user.name}\n"
    message += f"• **Discriminator:** {user.discriminator}\n"

    nitro_type = nitro_type_mapping.get(user.premium_type, 'None')
    message += f"• **Nitro Type:** {nitro_type}"

    # Send the message
    await ctx.send(message)


@bot.command()
async def purge(ctx, amount: int):
    if 1 <= amount <= 500:
        await ctx.message.delete()

        def is_bot_message(message):
            return message.author == bot.user

        if isinstance(ctx.channel, discord.TextChannel):
            deleted_messages = await ctx.channel.purge(limit=amount,
                                                       check=is_bot_message)
        elif isinstance(ctx.channel, discord.DMChannel):
            async for message in ctx.channel.history(
                    limit=amount).filter(is_bot_message):
                await message.delete()

        deleted_count = len(
            deleted_messages) if 'deleted_messages' in locals() else 0

        confirmation_msg = await ctx.send(
            f"Deleted {deleted_count} message(s).")
        await asyncio.sleep(5)
        await confirmation_msg.delete()
    else:
        await ctx.send(
            "Please provide a number between 1 and 500 for the purge command.")


def get_status_emoji(status):
    emoji_map = {
        'online': '🟢',
        'idle': '🟡',
        'dnd': '🔴',
        'streaming': '🟣',
        'invisible': '⚪',
    }
    return emoji_map.get(status, '')


#@bot.event
#async def on_command_completion(ctx):
#    command_name = ctx.command.name if ctx.command else "Unknown Command"
#    author = ctx.message.author
#    server = ctx.guild
#    channel = ctx.message.channel
#
#    log_msg = f"{PREFIX}{command_name}\n"
#    log_msg += f"<@{author.id}>\n"
#    log_msg += f"{server}\n"
#    log_msg += f"<#{channel.id}>\n"
#
#    print(log_msg)


@bot.command()
async def hello(ctx):
    await ctx.message.delete()
    await ctx.send("Bot Online!")
    await ctx.send(
        + "https://appembed.netlify.app/e?title=&description=Successfully%20set%20status%20to%3A%20Online%20%F0%9F%9F%A9&color=%2323a55a&author=Online%20Status"
    )
    await bot.change_presence(status=discord.Status.online)


@bot.command()
async def mccolor(ctx, *, args):
    formatted_text = apply_minecraft_colors(args)
    formatted_message = f"```ansi\n{formatted_text}\n```"
    await ctx.message.delete()
    await ctx.send(formatted_message)

@bot.command()
async def anti(ctx, option):
    await ctx.message.delete()

    if option == "messagelogger":
        message = await ctx.send("#" + long * 1999)
        for i in range(2):
            await message.edit(content=long * 2000)
        await message.delete()
    elif option == "showeditmessages":

        def is_message_author(message):
            return message.author == ctx.message.author

        async def edit_message(message):
            if is_message_author(message):
                await message.edit(content=message.content)

        bot.add_listener(edit_message, "on_message")
        await ctx.send("Enabled showeditmessages to edit your messages.")
    elif option == "disable":
        listeners = bot.extra_events.get("on_message", [])
        for listener in listeners[:]:
            if listener.__name__ == "edit_message":
                bot.remove_listener(listener, "on_message")
                listeners.remove(listener)
        await ctx.send("Disabled showeditmessages.")
    elif option == "skull":
        while 1:
            time.sleep(0.3)
            async for message in ctx.channel.history(limit=1):
                # Check if the last message has a skull emoji reaction
                if "💀" in [reaction.emoji for reaction in message.reactions]:
                    await message.delete()
                    await ctx.send(message.content)
                    break
    elif option == "blue":
        message_content = ctx.message.content[len(bot.command_prefix) +
                                              len("anti blue"):].strip()
        blue_message = blue_hyperlinks(message_content)
        await ctx.send(blue_message)
    else:
        await ctx.send("Invalid option. Use `/anti showeditmessages`, `/anti messagelogger`, `/anti disable`, `/anti skull`, or `/anti blue`.")


@bot.command()
async def download(ctx):
    # Get all messages in the current channel
    messages = await ctx.channel.history(limit=None).flatten()

    # Prepare a list to store formatted messages
    formatted_messages = []

    for message in messages:
        # Get the message timestamp and format it as "MM/DD/YYYY HH:MM"
        timestamp = message.created_at.strftime("%m/%d/%Y %H:%M")

        # Get the sender's display name or username if not available
        sender_name = message.author.display_name if message.author.display_name else message.author.name

        # Format the message content, including attachments if present
        message_content = f"{timestamp} | {sender_name}: {message.content}"

        # Handle attachments
        if message.attachments:
            for attachment in message.attachments:
                message_content += f" [Attachment 📷]({attachment.url})"

        formatted_messages.append(message_content)

    # Combine the formatted messages into a single string
    chat_text = "\n".join(formatted_messages)

    # Save the chat text to a file
    with open("downloaded_chat.txt", "w", encoding="utf-8") as file:
        file.write(chat_text)

    await ctx.send("Chat messages have been downloaded and saved to `downloaded_chat.txt`.")




@bot.command()
async def killlist(ctx, action, member: discord.Member = None):
    # Define a list to store users on the kill list
    kill_list = []

    # Check if the kill_list is already saved in a file
    if os.path.exists("kill_list.txt"):
        with open("kill_list.txt", "r") as file:
            kill_list = [line.strip() for line in file]

    if action == "start":
        # Check if the user has permission to disconnect users
        if ctx.author.guild_permissions.kick_members:
            # Disconnect users on the kill list
            for user_id in kill_list:
                user = await bot.fetch_user(int(user_id))
                try:
                    await user.send("You have been disconnected from the server.")
                    await user.disconnect()
                except Exception as e:
                    pass
            await ctx.send("Disconnected users on the kill list.")
        else:
            await ctx.send("You don't have permission to disconnect users.")
    elif action == "stop":
        # Clear the kill list
        kill_list.clear()
        # Remove the kill_list file
        if os.path.exists("kill_list.txt"):
            os.remove("kill_list.txt")
        await ctx.send("Cleared the kill list.")
    elif action == "add" and member:
        # Add the user to the kill list
        if str(member.id) not in kill_list:
            kill_list.append(str(member.id))
            # Save the kill list to a file
            with open("kill_list.txt", "w") as file:
                file.write("\n".join(kill_list))
            await ctx.send(f"Added {member.name} to the kill list.")
        else:
            await ctx.send(f"{member.name} is already on the kill list.")
    else:
        await ctx.send("Invalid command usage. Use `/killlist start`, `/killlist stop`, or `/killlist add @user`.")

bot.run(TOKEN, bot=False)
