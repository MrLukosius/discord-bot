import discord
from discord.ext import commands, tasks
import aiohttp

TIKTOK_USERNAMES = ["batuotaskatinasx", "bradegalt"]  # TikTok vartotojai
DISCORD_CHANNEL_ID = 1335557698959441920  # #live kanalo ID
ROLE_ID = 1341145232485646387  # Rolės ID, kurią reikia pažymėti

class TikTokNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_post_ids = {user: None for user in TIKTOK_USERNAMES}
        self.check_tiktok.start()

    async def get_tiktok_latest_post(self, username):
        """Tikrina ar yra naujas postas TikTok platformoje (naudojant trečiųjų šalių API)."""
        url = f"https://some-tiktok-api.com/user/{username}/latest-post"  # Čia reikės rasti API
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("video_id")
                return None

    @tasks.loop(minutes=5)  # Tikrinama kas 5 minutes
    async def check_tiktok(self):
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
        for username in TIKTOK_USERNAMES:
            new_post = await self.get_tiktok_latest_post(username)

            if new_post and new_post != self.last_post_ids[username]:  # Jei yra naujas postas
                role_mention = f"<@&{ROLE_ID}>"  # Tagina rolę
                embed = discord.Embed(
                    title=f"📢 {username} įkėlė naują TikTok postą!",
                    description=f"{role_mention}, peržiūrėk naujausią video!\n🔗 [Žiūrėti TikTok](https://www.tiktok.com/@{username})",
                    color=discord.Color.purple()
                )
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/0/08/TikTok_logo.png")  # TikTok logo
                await channel.send(content=role_mention, embed=embed)

            self.last_post_ids[username] = new_post  # Atnaujiname post ID

    @check_tiktok.before_loop
    async def before_check_tiktok(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TikTokNotifier(bot))
