import asyncio
import aiohttp
import next
import creds
from next.ext import commands
from api import get_img

gimgsettings = {
    "usestoplist": True,
    "stoplist": ["пенис", "хуй", "шлюха", "penis", "pride", 'lgbt', "лгбт", "прайд", "dick", "1488", "swastika", "свастика", "свастон"]
}

class Client(commands.CommandsClient):
    async def get_prefix(self, message: next.Message):
        return "!"

    @commands.command()
    async def gimg(self, ctx: commands.Context, *args):
        """Get image from Google Images"""

        arg = ""

        for word in args: # very stupid way to get args
            arg += f"{word} "

        banned = False
        if gimgsettings['usestoplist'] == True:
            for banword in gimgsettings['stoplist']:
                if banword in arg:
                    banned = True
                else:
                    pass
        
        if banned == False:
            try:
                url = get_img(arg) # requesting image
                await ctx.send(f"Search query: {arg}\n{url}") # sending image via embed
            except IndexError:
                await ctx.send("No images found")
        else:
            await ctx.send(f"Your search query contains banned words")


async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, creds.bot)
        print("Running GIMG")
        await client.start()
        
asyncio.run(main())
