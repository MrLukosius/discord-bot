import a2s
import asyncio
from discord.ext import commands

class Bradega(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bradega(self, ctx):
        try:
            ip = "45.81.254.160"
            port = 27015
            server_address = (ip, port)

            # Paleidžiame a2s.info asynchroniškai, kad išvengtume event loop problemų
            loop = asyncio.get_running_loop()
            info = await loop.run_in_executor(None, lambda: a2s.info(server_address))

            await ctx.send(f"🎮 **Bradega Serverio informacija:**\n"
                           f"🔹 Žaidėjų skaičius: {info.player_count}/{info.max_players}\n"
                           f"🌍 Žemėlapis: {info.map_name}\n"
                           f"🏷️ Serverio pavadinimas: {info.server_name}")
        except Exception as e:
            await ctx.send("⚠️ Nepavyko gauti Bradega serverio informacijos!")
            print(e)

async def setup(bot):
    await bot.add_cog(Bradega(bot))
