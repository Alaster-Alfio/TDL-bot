import os
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Helper function to add ordinal suffixes to day numbers.
def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

# Load environment variables from the .env file.
load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")

# Set up intents. Ensure the Message Content Intent is enabled in the Discord Developer Portal.
intents = discord.Intents.default()
intents.message_content = True

# Create the bot with the specified prefix.
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Simple command: !ping
@bot.command()
async def ping(ctx):
    """Responds with pong."""
    await ctx.send("pong")

# Simple command: !echo <message>
@bot.command()
async def echo(ctx, *, message: str):
    """Repeats the message provided by the user."""
    await ctx.send(message)

# Command group for to-do list operations.
@bot.group()
async def tdl(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Please specify a subcommand. For example: `!tdl today`")

@tdl.command(name="today")
async def tdl_today(ctx):
    # Get today's date.
    now = datetime.now()
    day = now.day
    month_abbr = now.strftime("%b")
    title = f"{ordinal(day)} {month_abbr}"  # e.g. "10th Feb"

    # Get the forum channel using the provided channel ID.
    channel = bot.get_channel(1330571681592377493)
    if channel is None:
        await ctx.send("Could not find the to-do-list forum channel.")
        return

    try:
        # Create a thread (forum post) directly on the forum channel.
        thread = await channel.create_thread(
            name=title,
            content="Starting today's to-do list."
        )
        # Instead of using thread.mention, create a mention using the thread's ID.
        await ctx.send(f"Thread created: <#{thread.id}>")
    except Exception as e:
        await ctx.send(f"An error occurred while creating the thread: {e}")

# Subcommand: !tdl add <task>
@tdl.command(name="add")
async def tdl_add(ctx, *, task: str):
    """Adds a new task to today's to-do list thread."""
    # This is where you'd add code to post the task to the appropriate thread.
    await ctx.send(f"Task added: {task}")

# Run the bot.
bot.run(TOKEN)
