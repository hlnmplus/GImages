import asyncio
import aiohttp
import next
import log
import creds
from time import sleep
from random import choice
from creds import gimgsettings
from next.ext import commands
from api import get_img

version = "1.0.4"

logger = log.createLogger(fileName = "gimg.log")
logger.log('Starting GImages')

class Client(commands.CommandsClient):
    async def get_prefix(self, message: next.Message):
        return "!"

    @commands.command()
    async def gimg(self, ctx: commands.Context, *args):
        """[count of images, 1 by default] - get image from Google Images"""
 
        query = ""

        banned = False

        try:
            count = int(args[0])
            for word in range(1, len(args)):
                query += f"{args[word]} "
        except:
            count = 1
            for word in args:
                query += f"{word} "
        
        if gimgsettings['usestoplist'] == True:
            for banword in gimgsettings['stoplist']:
                if banword in query:
                    banned = True
                else:
                    pass

        if count > 10:
            toomanyimages = True
        else:
            toomanyimages = False

        logger.log(f'{ctx.author.id} ({ctx.author.original_name}#{ctx.author.discriminator}) requested count={count}, query="{query}"')

        if toomanyimages == False and banned == False:
            try:
                url = get_img(query, count) # requesting image
                await ctx.send(f"Search query: {query}\n{url}") # sending image via embed
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
        logger.info(f"GImages started, v{version}")
        await client.start()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.info(f"GImages exited manually")
