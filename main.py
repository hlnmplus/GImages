import asyncio
import aiohttp
import next
import creds
from creds import gimgsettings
from next.ext import commands
from api import get_img

class Client(commands.CommandsClient):
    async def get_prefix(self, message: next.Message):
        return "!"

    @commands.command()
    async def gimg(self, ctx: commands.Context, *args):
        """[count of images, 1 by default] - get image from Google Images"""

        arg = ""

        banned = False
        if gimgsettings['usestoplist'] == True:
            for banword in gimgsettings['stoplist']:
                if banword in arg:
                    banned = True
                else:
                    pass
        
        try:
            count = int(args[0])
            for word in range(1, len(args)):
                arg += f"{args[word]} "
        except:
            count = 1
            for word in args:
                arg += f"{word} "
        

        if count > 10:
            toomanyimages = True
        else:
            toomanyimages = False

        if toomanyimages == False and banned == False:
            try:
                url = get_img(arg, count) # requesting image
                await ctx.send(f"Search query: {arg}\n{url}") # sending image via embed
            except IndexError:
                await ctx.send("No images found")
        elif banned == True:
            await ctx.send(f"Your search query contains banned words")
        elif toomanyimages == True:
            await ctx.send(f"You requested too many images (>10)")


async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, creds.bot)
        print("Running GImages")
        await client.start()
        
asyncio.run(main())
