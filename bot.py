import discord
import responses
import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def send_message(message: discord.Message, user_message: str):
    if not user_message:
        print("Message was empty because intents were not enabled probably")
        return

    message_split = [i for i in user_message.split(" ") if i != ""]
    if is_private := message_split[0] == '?Makoto':
        user_message = " ".join(message_split[1:])

    # When the generation is empty,
    # I want to keep sure the CONSOLE ISN'T SPAMMING
    # "400 Bad Request (error code: 50006): Cannot send an empty message"
    try:
        response = await responses.handle_response(message, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as ex:
        if str(ex) != "400 Bad Request (error code: 50006): Cannot send an empty message":
            print(ex)


@client.event
async def on_ready():
    print(f"{client.user} is running!")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f"[{channel}] {username}: '{user_message}'")
    await send_message(message, user_message)


def run_discord_bot():
    client.run(TOKEN)
