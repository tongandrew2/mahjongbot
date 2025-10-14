# bot.py
import os
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
import discord
from dotenv import load_dotenv
from discord.ext import commands
from game import *
from tiles import *

#Use the API entirely and just focus on making a fully functional game
#or
#Write the game from scratch and start with tile array and yaku


intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} is connected to the following guild:\n'f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members: \n- {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$emoji'):
        await message.channel.send("<a:whirlpool:798611947569676299>")


    if message.content.startswith('$testhand'):

        def check(hand):
            return hand.author == message.author


        alltiles = []
        for x in range(136):
            alltiles.append(x)
        await message.author.send('Before shuffle: ')
        await message.author.send(alltiles)
        shuffle_tiles(alltiles)
        await message.author.send('After shuffle: ')
        await message.author.send(alltiles)
        tiles = draw_hand(alltiles)
        await message.author.send('Your hand: ' + TilesConverter.to_one_line_string(tiles))

        #discard test
        while True:
            tiledrawn = draw_tile(tiles, alltiles)
            await message.author.send('You drew the ' + TilesConverter.to_one_line_string(tiledrawn))
            await message.author.send('Your hand: ' + TilesConverter.to_one_line_string(tiles))
            await message.author.send('What would you like to discard?')
            discard = await client.wait_for('message', check=check)
            if discard.content  == 'exit':
                break


            discard_tile(tiles,(TilesConverter.one_line_string_to_136_array(discard.content))[0])


            await message.author.send('Your hand: ' + TilesConverter.to_one_line_string(tiles))


    if message.content.startswith('$calculatehand'):
        await message.author.send('Hi! Please input a winning hand in string form.')

        def check(hand):
            return hand.author == message.author

        # Mahjong preset calculator
        calculator = HandCalculator()
        msg = await client.wait_for('message', check=check)
        givenhand = TilesConverter.one_line_string_to_136_array(msg.content)
        print(givenhand)


        await message.author.send('What tile did the hand win with?')
        msgtwo = await client.wait_for('message', check=check)
        win_tile = TilesConverter.one_line_string_to_136_array(msgtwo.content)[0]
        print(win_tile)

        await message.author.send('Please input any melds (e.g. Pon, Chi, Kan) that the hand used.')
        msgthree = await client.wait_for('message', check=check)
        melds = []
        meld_tiles = TilesConverter.one_line_string_to_136_array(msgthree.content)
        meld = Meld("chi", meld_tiles)
        print(meld)
        melds.append(meld)


        result = calculator.estimate_hand_value(givenhand, win_tile,melds)

        await message.author.send("Han: " + str(result.han))
        await message.author.send("Fu: " + str(result.fu))
        await message.author.send("Points:" + str(result.cost['main']))
        await message.author.send("Yaku:")
        for yaku in result.yaku:
            await message.author.send(yaku)
        for fu_item in result.fu_details:
            await message.author.send(fu_item)


    if message.content.startswith('$testcalculation'):
        calculator = HandCalculator()

        # we had to use all 14 tiles in that array
        tiles = TilesConverter.string_to_136_array(man='22444', pin='333567', sou='444')
        win_tile = TilesConverter.string_to_136_array(sou='4')[0]

        result = calculator.estimate_hand_value(tiles, win_tile)


        await message.channel.send(str(result.han) + " " + str(result.fu))
        await message.channel.send(str(result.cost['main']))
        await message.channel.send(result.yaku)
        for fu_item in result.fu_details:
            await message.channel.send(fu_item)

client.run(TOKEN)
