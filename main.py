# $source ./venv/bin/activate
# $python main.py

from os import getenv
import discord
import random
from modules import info, crawler

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="監視器 | -help"))
    print(f'已登入 {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_fixed = message.content.strip().lower()

    if message_fixed.startswith('-dice '):
        if message_fixed.replace('-dice ', '').isnumeric():
            max_number = int(message_fixed.replace('-dice ', ''))
            result = random.randint(1, max_number)
            return await message.channel.send(f'使用了 {max_number} 面骰，擲出的點數是：**{result}**')

    if message_fixed.startswith('-fun'):
        new_message = await message.channel.send('讀取中……')
        random_fun_image = crawler.get_random_fun_image()
        new_embed = discord.Embed()
        new_embed.set_author(
            name=f'出自〈{random_fun_image["source"]}〉', url=random_fun_image["source_url"])
        new_embed.set_image(url=random_fun_image['image'])
        new_embed.set_footer(text=random_fun_image["source_url"])
        return await new_message.edit(content='', embed=new_embed)

    if message_fixed.startswith('-idiom'):
        new_message = await message.channel.send('讀取中……')

        if message_fixed.startswith('-idiom '):
            keyword = message_fixed.split(' ')[1]
            idiom = crawler.get_search_idiom(keyword)
            if idiom == None:
                return await new_message.edit(content=f'在教育部《成語典》中搜尋不到有關「{keyword}」的結果。')
        else:
            idiom = crawler.get_random_idiom()

        new_embed = discord.Embed(
            title=idiom['title'], description=idiom['phonet'], url=idiom['url'], color=0xa6bfe8)
        new_embed.add_field(name='釋義', value=idiom['desc'], inline=False)
        if idiom['story'] != None:
            new_embed.add_field(name='典故', value=idiom['story'], inline=False)
        new_embed.set_footer(text='以上內容出自教育部《成語典》，點擊標題查看更多詳細內容')
        return await new_message.edit(content='', embed=new_embed)

    if message_fixed.startswith('-wiki'):
        new_message = await message.channel.send('讀取中……')
        article = crawler.get_random_wikipedia_article()
        new_embed = discord.Embed(
            title=article['title'], url=article['url'], color=0xf6f6f6)
        for paragraph in article['paragraphs']:
            new_embed.add_field(name='', value=paragraph, inline=False)
        new_embed.set_footer(text='以上內容摘錄自《維基百科》，點擊標題查看更多詳細內容')
        return await new_message.edit(content='', embed=new_embed)

    if message_fixed.startswith('-help'):
        new_embed = discord.Embed(title='指令說明', color=0xa6bfe8)
        for item in info.getHelp():
            new_embed.add_field(
                name='', value=f'`{item["command"]}`：{item["desc"]}', inline=False)
        return await message.channel.send(embed=new_embed)

# BOT token
client.run(getenv("DISCORD_TOKEN"))
