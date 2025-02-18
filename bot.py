import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Užkrauname .env failą (jei naudojamas)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="Prižiūrių tvarką👀")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Prisijungta kaip {bot.user.name}")

    # Užregistruojamos visos komandos
    for command in bot.commands:
        print(f"🔹 Užregistruota komanda: {command.name}")

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            extension = f"commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"✅ Įkelta komanda: {filename}")
            except commands.errors.ExtensionAlreadyLoaded:
                print(f"⚠️ Modulis {extension} jau įkeltas!")
            except Exception as e:
                print(f"❌ Klaida įkeliant {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        
        # Patikriname, ar `server_info` tikrai įkeltas
        if "commands.server_info" not in bot.extensions:
            print("⚠️ Modulis `server_info` nebuvo užkrautas!")
        else:
            print("✅ Modulis `server_info` sėkmingai užkrautas!")

        await bot.start(os.getenv("DISCORD_TOKEN"))

# Startuojame bot'ą
asyncio.run(main())
