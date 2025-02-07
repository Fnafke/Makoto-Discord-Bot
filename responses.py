import asyncio
from random import choice, randint
from bs4 import BeautifulSoup
import discord
# from transformers import pipeline
import requests
import time

# I initialize the chatbot here, even though it makes more sense
# to be in the bot.py but since responses is here and I want responses
# to be the deciding factor if the answer is AI or not.

# chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")


async def delete_user_message(phrase: str, channel: discord.TextChannel, user: discord.User):
    start_time = time.time()
    deleted_count = 0

    def check(msg):
        return msg.author == user and phrase.lower() in msg.content.lower()

    try:
        # Manually delete older messages one by one
        async for msg in channel.history(limit=None, oldest_first=False):
            if check(msg):
                try:
                    print("Found messsage!")
                    await msg.delete()
                    deleted_count += 1
                    await asyncio.sleep(1.5)  # Avoid rate limits
                except discord.Forbidden:
                    return "Missing permissions to delete messages."
                except discord.HTTPException as e:
                    return f"Failed to delete messages: {e}"
            else:
                print(
                    f"Did not find message, looking for next! Also date of not found message is: {msg.created_at}")

    except discord.Forbidden:
        return "Missing permissions to delete messages."
    except discord.HTTPException as e:
        return f"Failed to delete messages: {e}"

    total_time = time.time() - start_time
    return f'Deleted {deleted_count} messages in {total_time:.2f}s'


async def handle_response(message_object: discord.Message, user_message: str):
    p_message = user_message.lower()
    message_split = user_message.split(" ")
    message_first = message_split[0]
    message_rest = message_split[1:]

    list_of_commands = [
        "**?** - Used to test the discord bot",
        "**?testing makoto** - Used to test the discord bot 2",
        "**?MakotoHelp** - Used to check out all the commands available in the bot",
        "**?MakotoDelete** ***keyword*** - With this command you will be able to delete all your messages containing 'keyword'"
    ]

    # Testing the bot
    if p_message == "?testing makoto":
        return "Stfu braindead ass"

    # Testing the bot 2
    if p_message == "?":
        return "fix your shit"

    # test - Serkan
    if p_message == "test":
        return "Just one cycle bro, it wont ruin my health, just trust me bro, one cycl-"

    # Help to view all commands
    if p_message == "?makotohelp":
        commands_message = "\n".join(list_of_commands)
        return f"The list of commands for the Makoto Discord bot are:\n{commands_message}"

    # # AI conversation
    # if message_first == "?MakotoAI":
    #     prompt = "".join(message_rest)
    #     response = chatbot(prompt, num_return_sequences=1, pad_token_id=50256)
    #     response_text = response[0]['generated_text']
    #     return response_text

    # Delete your messages containing a cetain phrase
    # Use case: ?MakotoDelete [phrase]
    # Response: Deleted all messages of {user} containing [phrase] (Deleted messages: [Amount] in [Amount of time])
    if message_first == "?MakotoDelete":
        user = message_object.author
        for channel in message_object.guild.text_channels:
            response = await delete_user_message(message_rest[0], channel, user)
        return f"Deleted all messages of {user.name} containing {message_rest} ({response})"
