# bot.py
import os
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
import discord
from dotenv import load_dotenv
from discord.ext import commands
import game
from tiles import * #change this later to import tiles after refactoring code
import scoring
import melds

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
        
        while True:
            msg = await client.wait_for('message', check=check)
            givenhand = parse_tiles(msg.content)
            if givenhand is None:
                await message.author.send("Invalid tile format.")
                continue

            if len(givenhand) != 14:
                await message.author.send("A hand must contain 14 tiles.")
                continue

            if is_valid_tile_set(givenhand) == False:
                await message.author.send("A hand must only contain 4 of each tile at most.")
                continue

            #If none of the failure conditions are met, exit the loop
            break


        await message.author.send('What tile did the hand win with?')
        while True:
            msgtwo = await client.wait_for('message', check=check)
            win_tile = parse_tiles(msgtwo.content)
            print(givenhand)
            print(win_tile)
            if win_tile is None:
                await message.author.send("Invalid tile format.")
                continue
            if win_tile[0] not in givenhand:
                await message.author.send("This tile is not in your specified hand.")
                continue
            break

        
        #add a failsafe for incorrect inputs


        await message.author.send('Please input any melds (e.g. Pon, Chi, Kan) that the hand used. Enter Done when finished.')
        hand_melds = []
        hand_melds_textform = []

        while True:
            msgthree = await client.wait_for('message', check=check)
            if msgthree.content == "Done":
                break

            meld_tiles = TilesConverter.one_line_string_to_136_array(msgthree.content)
            meld_type = melds.is_valid_meld(meld_tiles)
            if(meld_type == None):
                 await message.author.send('This is not a valid meld. Try again!')

            else:
                hand_melds_textform.append(msgthree.content)
                #the meld needs to return type!
                #await message.author.send(meld_tiles)
                hand_melds.append(melds.create_meld(meld_tiles, meld_type))
                await message.author.send('Melds:')
                for meld_textform in hand_melds_textform:
                    await message.author.send(meld_textform)

        is_tsumo = False
        await message.author.send('Was this hand won by Tsumo or Ron?')
        msgfour = await client.wait_for('message', check=check)
        if(msgfour.content.lower() == 'tsumo'):
            is_tsumo = True
        else:
            pass


        result = scoring.calculate_hand_score(givenhand, win_tile, hand_melds, is_tsumo)


        #temporary error check for erroneous hand calculation
        if result.error is not None:
            await message.author.send(result.error)
            
        elif result.han == 0:
            await message.author.send("This hand does not have a yaku.")
        else:
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
        result = calculator.estimate_hand_value(tiles,win_tile)


        await message.channel.send(str(result.han) + " " + str(result.fu))
        await message.channel.send(str(result.cost['main']))
        await message.channel.send(result.yaku)
        for fu_item in result.fu_details:
            await message.channel.send(fu_item)

client.run(TOKEN)
