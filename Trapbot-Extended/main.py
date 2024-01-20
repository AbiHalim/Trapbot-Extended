import discord
from discord.ext import commands
import os
import random
import json
import requests
import inspirobot
import asyncio
from hosting import keep_alive

#get prefix for each server
def prefix(bot, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        
        return prefixes[str(message.guild.id)]
        
    #in case default settings
    except:

        #set default prefix when bot joins server
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        
        prefixes[str(message.guild.id)] = '%'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        #make a pool when bot joins server
        with open('pool.json', 'r') as f:
            pool = json.load(f)
        
        pool[str(message.guild.id)] = []

        with open('pool.json', 'w') as f:
            json.dump(pool, f, indent=4)

        #set spam limit when bot joins server
        with open('spam_limit.json', 'r') as f:
            spam_limit = json.load(f)
        
        spam_limit[str(message.guild.id)] = 10

        with open('spam_limit.json', 'w') as f:
            json.dump(spam_limit, f, indent=4)

token = os.environ['token']
bot = commands.Bot(command_prefix = prefix, case_insensitive = True, help_command = None)

def color():
    return random.randint(0, 0xFFFFFF)

#when bot leaves server
@bot.event
async def on_guild_remove(guild):

    #remove prefix when bot leaves server
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    #remove pool when bot leaves server
    with open('pool.json', 'r') as f:
        pool = json.load(f)
    
    pool.pop(str(guild.id))

    with open('pool.json', 'w') as f:
        json.dump(pool, f, indent=4)

    #remove spam limit when bot leaves server
    with open('spam_limit.json', 'r') as f:
        spam_limit = json.load(f)
    
    spam_limit.pop(str(guild.id))

    with open('spam_limit.json', 'w') as f:
        json.dump(spam_limit, f, indent=4)

#pool finite mode
finite = False

#bot is on
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(
        name=" Scheming", url='https://www.youtube.com/watch?v=1KaecOQKNaM'))
    print('{0.user} is on'.format(bot))

#on message
@bot.event
async def on_message(msg):

    #respond to mentions
    if msg.author.id != bot.user.id:
        if '<@!860410812857057290>' in msg.content:
            try:
                with open('prefixes.json', 'r') as f:
                    prefix = json.load(f)[str(msg.guild.id)]
                await msg.channel.send(embed=discord.Embed(title='Hello!', description=f'Type {prefix}help to see a list of my commands', color=color()))
            except:
                await msg.channel.send(embed=discord.Embed(title='Hello!', description='Type %help to see a list of my commands', color=color()))

        #randomly react to messages
        reactions = [
        '<:walter:860899565895942154>','<:trollface:860899568669425664>','<:terror:860899568879140874>','<:spiggle:860899568560373771>','<:ripbozo:860899568089956423>','<:pepecry:860899568422354944>','<:pain:860899568455385109>','<:oohaah:860899568907714561>','<:megamalice:860899568706387999>','<:manic:860899568664707072>','<:malice:860899568925409301>','<:horh:860899568723820575>','<:haha:860899567990341682>','<:gigachad:860899567821520916>','<:delight:860899568501391360>','<:crazy:860899568765239316>','<:cope:860899566948712468>','<:dismay:860899567754674227>','<:agony:860899568773365761>','<:allleft:860899568475308062>','<:alms:860899568472031272>','<:anguish:860899568944939018>','<:based:860899564630704128>','<:bruh:860899569691525120>','<:cerealguy:860899568941006858>','<:clearly:860899569087938570>'
        ]
        
        chance = random.random()
        if chance <= 0.05:
            await msg.add_reaction(random.choice(reactions))

    await bot.process_commands(msg)

#help
@bot.command(aliases=['commands'])
async def help(ctx):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)[str(ctx.guild.id)]
    with open('spam_limit.json', 'r') as f:
        maximum_count = json.load(f)[str(ctx.guild.id)]
    embed=discord.Embed(title="Command List", description=f"**{prefix}help** : Shows list of commands \n**{prefix}prefix** : Changes my prefix \n**{prefix}say (message)** : Says (message) \n**{prefix}quote** : Says a random quote \n**{prefix}joke** : Says a random joke \n**{prefix}fact** : Says a random fact \n**{prefix}activity** : Sends a random activity to do if you're bored \n**{prefix}roast** : Sends a random insult \n**{prefix}inspirobot** : Sends a randomly generated inspirational quote \n**{prefix}waifu** : Sends a random waifu image\n**{prefix}comic** : Sends the current xkcd comic\n**{prefix}8ball** : Predicts the future \n**{prefix}sheeshrate** : Rates how SHEESH something is \n\n**Pool**\nA list of random messages which the bot will store \n\n**{prefix}pool** : Says a random message from the pool \n**{prefix}pool list** : Sends the full list of messages in the pool \n**{prefix}pool add (message)** : Adds (message) to the pool \n**{prefix}pool remove (message)** : Removes (message) from the pool\n**{prefix}pool clear** : Clears the pool (admins only)\n**{prefix}pool help** : Shows list of commands for pool \n\n**Zomnia Player**\nPlays Zomnia songs\n\n**{prefix}zomnia** : Plays a random Zomnia song \n**{prefix}zomnia (song)** : Plays specified song \n**{prefix}zomnia pause** : Pauses the song \n**{prefix}zomnia resume** : Resumes the song \n**{prefix}zomnia stop** : Stops the song and disconnects from channel \n**{prefix}zomnia playing** : Says what song is currently playing\n**{prefix}zomnia help** : Shows list of songs and commands for Zomnia Player \n\n**Speed**\nA game where you must send a message every second \n\n**{prefix}speed** : Starts a game of speed \n**{prefix}speed help** : Shows information for Speed\n\n**Spam**\nSpams a message\n\n**{prefix}spam (content), (amount)** : Spams (content) for (amount) of times.\n**{prefix}spam stop** : Stops spamming\n**{prefix}spam set (amount)** : Sets the maximum amount for spam. Current limit is {maximum_count}.", color=color())
    embed.set_author(name="Trapbot")
    await ctx.send(embed=embed)

#change prefix
@bot.command()
async def prefix(ctx, *, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix
    await ctx.send(f'My prefix has been set to {prefix}')

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title=f'My current prefix is {prefix}', description = f'You can change my prefix by doing {prefix}prefix (new prefix)')
        await ctx.send(embed=embed)

#say
@bot.command()
async def say(ctx, *, say):
    await ctx.message.delete()
    await ctx.send(say)

#ghostping
@bot.command()
async def ghostping(ctx):
    await ctx.message.delete()

#random quote
@bot.command()
async def quote(ctx):
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = discord.Embed(title='\"' + json_data[0]['q'] + '\"', description='- ' + json_data[0]['a'], color=color())
    await ctx.send(embed=quote)

#random joke
@bot.command()
async def joke(ctx):
    response = requests.get(
        'https://official-joke-api.appspot.com/random_joke')
    json_data = json.loads(response.text)
    joke = discord.Embed(title=json_data['setup'], description='||' + json_data['punchline'] + '||', color=color())
    await ctx.send(embed=joke)

#random fact
@bot.command()
async def fact(ctx):
    response = requests.get(
        'https://uselessfacts.jsph.pl/random.json?language=en')
    json_data = json.loads(response.text)
    fact = discord.Embed(title="Did you know?", description=json_data['text'], color=color())
    await ctx.send(embed=fact)

#random activity
@bot.command()
async def activity(ctx):
    response = requests.get('https://www.boredapi.com/api/activity/')
    json_data = json.loads(response.text)
    activity = discord.Embed(title=json_data['activity'], description='Category: ' + json_data['type'], color=color())
    await ctx.send(embed=activity)

#random roast
@bot.command(aliases=['insult'])
async def roast(ctx):
    response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
    json_data = json.loads(response.text)
    await ctx.send(json_data['insult'])

#inspirobot
@bot.command(aliases=['inspirobot', 'inspire'])
async def inspiro(ctx):
    quote = inspirobot.generate()
    embed = discord.Embed(title='Inspirobot', url='https://inspirobot.me', color = color())
    embed.set_image(url=quote)
    embed.set_footer(text='AI generated inspirational quote')
    await ctx.send(embed=embed)

#waifu
@bot.command(aliases=['gf', 'anime'])
async def waifu(ctx, category='random'):
    if category == 'waifu':
        response = requests.get('https://api.waifu.pics/sfw/waifu')
    elif category == 'neko':
        response = requests.get('https://api.waifu.pics/sfw/neko')
    elif category == 'random':
        categories = ['waifu', 'neko']
        response = requests.get('https://api.waifu.pics/sfw/' + random.choice(categories))
    json_data = json.loads(response.text)
    waifu = discord.Embed(title='Random Waifu', url='https://waifu.pics', color=color())
    waifu.set_image(url=json_data["url"])
    await ctx.send(embed=waifu)

#comic
@bot.command(aliases=['xkcd'])
async def comic(ctx):
    response = requests.get('https://xkcd.com/info.0.json')
    json_data = json.loads(response.text)
    embed = discord.Embed(title='xkcd Comic', url="https://xkcd.com", color = color())
    embed.set_image(url=json_data['img'])
    embed.set_footer(text="Comic from https://xkcd.com")
    await ctx.send(embed=embed)

#spam
@bot.group(invoke_without_command = True)
async def spam(ctx, *, args):
    with open('spam_limit.json', 'r') as f:
        maximum_count = json.load(f)[str(ctx.guild.id)]
    global spam_running
    content = args.split(',')[0]
    amount = args.split(',')[1]
    count = 0
    if int(amount) <= maximum_count:
        spam_running = True
        while count < int(amount):
            if spam_running:
                count += 1
                await ctx.send(content)
                await asyncio.sleep(1.5)
            else:
                break
        spam_running = False
    else:
        await ctx.send('Limit is ' + str(maximum_count))

#stop spam
@spam.command()
async def stop(ctx):
    global spam_running
    if spam_running:
        spam_running = False
    else:
        await ctx.send('Not currently spamming!')

#change spam limit
@spam.command()
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def set(ctx, *, limit):
    try:
        limit = int(limit)
        if limit <= 100:
            with open('spam_limit.json', 'r') as f:
                spam_limit = json.load(f)

            spam_limit[str(ctx.guild.id)] = limit
            await ctx.send(f'Limit has been set to {limit}')

            with open('spam_limit.json', 'w') as f:
                json.dump(spam_limit, f, indent=4)
        elif limit >= 100:
            await ctx.send('Limit must be less than 100!')
    except:
        await ctx.send('Limit must be an integer!')

@set.error
async def set_error(ctx, error):
    await ctx.send('Something went wrong!')

@spam.error
async def spam_error(ctx, error):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)[str(ctx.guild.id)]
    await ctx.send(embed=discord.Embed(title='Something went wrong!', description=f'Format: {prefix}spam (content), (amount)', color=color()))

#8ball
@bot.command(aliases=['8ball'])
async def eightball(ctx, *, question = None):
    outcomes = ['Yes', 'No', 'Definitely', 'No way', 'Certainly', 'I\'d tell you but you wouldn\'t like the answer 😬', 'Without a doubt', 'It\'s not looking good', 'I\'m not gonna lie to you chief, it doesn\'t look good', 'I think so']
    guaranteed = ['will uggetfacts be real']
    yes = outcomes[::2]
    if question is None:
        await ctx.send(random.choice(outcomes))
    elif question.lower() in guaranteed:
        embed = discord.Embed(title=question, description=random.choice(yes), color=color())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=question, description=random.choice(outcomes), color = color())
        await ctx.send(embed=embed)

#sheeshrate
@bot.command()
async def sheeshrate(ctx):
    amount = random.randint(2, 9)
    sheeshrate = ':regional_indicator_s: :regional_indicator_h: '
    for x in range(amount):
        sheeshrate += ':regional_indicator_e: '
    sheeshrate += ':regional_indicator_s: :regional_indicator_h:'
    await ctx.send(sheeshrate)

#waifuquote
@bot.command(aliases=['gfquote', 'frl'])
async def waifuquote(ctx, category='random'):
    if category == 'waifu':
        waifuresponse = requests.get('https://api.waifu.pics/sfw/waifu')
    elif category == 'neko':
        waifuresponse = requests.get('https://api.waifu.pics/sfw/neko')
    elif category == 'random':
        categories = ['waifu', 'neko']
        waifuresponse = requests.get('https://api.waifu.pics/sfw/' + random.choice(categories))
    waifujson_data = json.loads(waifuresponse.text)

    quoteresponse = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(quoteresponse.text)
    waifuquote = discord.Embed(title='\"' + json_data[0]['q'] + '\"', description='- ' + json_data[0]['a'], color=color())
    waifuquote.set_image(url=waifujson_data["url"])
    await ctx.send(embed=waifuquote)

#change nickname
@bot.command()
async def nick(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

#pool

#get each server's specific pool
def get_pool(bot, message):
    with open('pool.json', 'r') as f:
        pool = json.load(f)
    
    return pool[str(message.guild.id)]

#get random submission from pool
@bot.group(invoke_without_command = True)
async def pool(ctx):
    with open ('pool.json', 'r+') as f:
        pool = json.load(f)[str(ctx.guild.id)]
        try:
            pool = random.choice(pool)
            await ctx.send(pool)
            if finite:
                index = pool.index(pool)
                del pool[index]
                json.load(f)[str(ctx.guild.id)] = pool
        except:
            await ctx.send('Pool is empty!')

#add submission to pool
@pool.command()
async def add(ctx, *, submission):
    with open('pool.json', 'r') as f:
        pool = json.load(f)
    
    pool[str(ctx.guild.id)].append(submission)
    await ctx.send(
        embed=discord.Embed(title='Submission to pool added:', description=submission, color=color()))
    
    with open('pool.json', 'w') as f:
        json.dump(pool, f, indent=4)

@add.error
async def pool_add_error(ctx, error):
    await ctx.send('What do you want me to add? Try again')


#remove submission from pool
@pool.command(aliases = ['delete'])
async def remove(ctx, *, submission):
    with open('pool.json', 'r') as f:
        pool = json.load(f)
    
    pool[str(ctx.guild.id)].remove(submission)
    await ctx.send(f'{submission} has been removed from the pool')
    
    with open('pool.json', 'w') as f:
        json.dump(pool, f, indent=4)

@remove.error
async def pool_remove_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('What do you want me to delete? Try again')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send('That isn\'t in the pool')


#list all submissions in pool
@pool.command()
async def list(ctx):
    with open ('pool.json', 'r+') as f:
        pool = json.load(f)[str(ctx.guild.id)]
        poollist = ''
        submissions = 0
        for submission in pool:
            submissions += 1
            poollist += str(submission + ', ')
            poollist_trimmed = [
                poollist[i:i + 1000] for i in range(0, len(poollist), 1000)]

            pages = 0
            for page in poollist_trimmed:
                pages += 1
            cur_page = 1
            
        if poollist == '':
            await ctx.send('Pool is empty!')
        else:
            message = await ctx.send(f'**Pool** \nTotal: {submissions} submissions \nPage {cur_page}/{pages}\n```{poollist_trimmed[cur_page-1]}```')

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
                # This makes sure nobody except the command sender can interact with the "menu"

            while True:
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                    # waiting for a reaction to be added - times out after 60 seconds

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        await message.edit(content=f"**Pool** \nTotal: {submissions} submissions \nPage {cur_page}/{pages}\n```{poollist_trimmed[cur_page-1]}```")
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        await message.edit(content=f"**Pool** \nTotal: {submissions} submissions \nPage {cur_page}/{pages}\n```{poollist_trimmed[cur_page-1]}```")
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)
                        # removes reactions if the user tries to go forward on the last page or
                        # backwards on the first page
                except asyncio.TimeoutError:
                    await message.delete()
                    break
                    # ending the loop if user doesn't react after 60 seconds

#clear pool
@pool.command()
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def clear(ctx):
    message = await ctx.send('`Are you sure you want to clear the pool?`')
    await message.add_reaction("🚫")
    await message.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🚫", "✅"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after 60 seconds

            if str(reaction.emoji) == "🚫":
                await message.delete()
                break

            elif str(reaction.emoji) == "✅":
                await message.delete()
                await ctx.send(content="`Pool has been cleared.`")
                with open('pool.json', 'r') as f:
                    pool = json.load(f)

                pool[str(ctx.guild.id)].clear()

                with open('pool.json', 'w') as f:
                    json.dump(pool, f, indent=4)

        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after 60 seconds

#pool help
@pool.command(aliases=['help'])
async def pool_help(ctx):
    embed=discord.Embed(title="Pool", description="A list of random messages which the bot will store\n\n**%pool** : Says a random message from the pool \n**%pool list** : Sends the full list of messages in the pool \n**%pool add (message)** : Adds (message) to the pool \n**%pool remove (message)** : Removes (message) from the pool \n**%pool clear** : Clears the pool (admins only)", color=color())
    await ctx.send(embed=embed)

#zomnia

#play a chosen song
@bot.group(invoke_without_command = True, aliases=['zom'])
async def zomnia(ctx, *, song='random'):
    global paused
    global playing
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)[str(ctx.guild.id)]
    discography = ['harden', 'jtown', 'laughin to the bank', 'like me', 'luv urz', 's3lf c0ntr0l', 'saucelikethis', 'star', 'top of the morning', 'troll', 'uknowwhatimsayinnn', 'yadig', 'arkan im prada u']
    if ctx.message.guild.id == 493773634163310592:
        discography.remove('luv urz')
    paused = False
    channel = ctx.author.voice.channel
    await channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if song.lower() in discography:
        voice.play(discord.FFmpegPCMAudio(f'zomnia/{song.lower()}.m4a'))
        await ctx.send(f'**🎵 Now playing:** {song.upper()}')
        playing = song.upper()
    elif song.lower() == 'random':
        random_song = random.choice(discography)
        voice.play(discord.FFmpegPCMAudio(f'zomnia/{random_song}.m4a'))
        await ctx.send(f'**🎵 Now playing:** {random_song.upper()}')
        playing = random_song.upper()
    else:
        random_song = random.choice(discography)
        voice.play(discord.FFmpegPCMAudio(f'zomnia/{random_song}.m4a'))
        await ctx.send(f'**🎵 Now playing:** {random_song.upper()}\n`Could not find {song}, do {prefix}zomnia help to see the list of songs.\nPlaying a random song instead.`')
        playing = random_song.upper()
    while voice.is_playing():
        await asyncio.sleep(1)
    else:
        if paused:
            await asyncio.sleep(1)
        else:
            await voice.disconnect()

#try to play a song while already playing

@zomnia.error
async def zomnia_error(ctx, error):

    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send('Something went wrong!')


#zomnia help / list of songs
@zomnia.command(aliases=['help', 'list', 'library', 'discography', 'songs'])
async def zom_help(ctx):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)[str(ctx.guild.id)]
    embed=discord.Embed(title="Zomnia Player", url="https://soundcloud.com/user-935029004", description=f"**Plays Zomnia songs** \n\n**Song List:** \nLaughin to the Bank \nJTOWN \nSauceLikeThis \nSTAR \nYADIG \nLIKE ME \nLUV URZ \nTOP OF THE MORNING \nHarden \nS3LF C0NTR0L \nUKNOWWHATIMSAYINNN \nARKAN IM PRADA U \n\n**Commands:** \n**{prefix}zomnia** : Plays a random Zomnia song \n**{prefix}zomnia (song)** : Plays specified song \n**{prefix}zomnia pause** : Pauses the song \n**{prefix}zomnia resume** : Resumes the song \n**{prefix}zomnia stop** : Stops the song and disconnects from channel \n**{prefix}zomnia playing** : Says what song is currently playing", color=color())
    embed.set_author(name="Zomnia", icon_url="https://i1.sndcdn.com/avatars-Mj5WGfy56NwyfQl1-6RQRWA-t500x500.jpg")
    await ctx.send(embed=embed)

#stop playing
@zomnia.command(aliases=['stop'])
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('Left the channel!')

@leave.error
async def leave_error(ctx, error):
    channel = ctx.author.voice.channel
    await channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.disconnect()

#pause the song
@zomnia.command()
async def pause(ctx):
    global paused
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        paused = True
        await ctx.send('Paused!')
    else:
        await ctx.send('Nothing is playing!')

@pause.error
async def pause_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send('Nothing is playing!')

#resume the song
@zomnia.command()
async def resume(ctx):
    global paused
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        paused = False
        await ctx.send('Resumed!')
    else:
        await ctx.send('Already playing!')

@resume.error
async def resume_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send('Nothing is playing!')

#now playing
@zomnia.command(aliases=['np', 'now'])
async def playing(ctx):
    global playing
    await ctx.send(f'**🎵 Now playing:** {playing}')

#speed
@bot.group(invoke_without_command = True)
async def speed(ctx):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)[str(ctx.guild.id)]
    message = await ctx.send(embed=discord.Embed(title='Would you like to start a game of Speed?', description=f'Do {prefix}speed help for information on Speed', color=color()))
    await message.add_reaction("🚫")
    await message.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🚫", "✅"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after 60 seconds

            if str(reaction.emoji) == "🚫":
                await message.delete()
                break

            # if they start the game
            elif str(reaction.emoji) == "✅":
                await message.delete()

                # countdown
                message = await ctx.send('Speed starting in 3...')
                await asyncio.sleep(1)
                await message.edit(content='Speed starting in 2...')
                await asyncio.sleep(1)
                await message.edit(content='Speed starting in 1...')
                await asyncio.sleep(1)
                await message.edit(content='**Go!**')
                await asyncio.sleep(1)

                alive = True
                score = 0

                # speed game
                while alive:
                    try:
                        await bot.wait_for('message', timeout=1)
                        score += 1
                    except asyncio.TimeoutError:
                        alive = False
                        break

                await ctx.send(embed=discord.Embed(title=f'**Game Over!**', description=f'Your score was {score} seconds.',color=color()))
                break
    
        except asyncio.TimeoutError:
            await message.delete()
            break
            # deleting original message if user doesn't react after 60 seconds

@speed.command(aliases=['info', 'help'])
async def speed_help(ctx):
    with open('prefixes.json', 'r') as f:
        prefix = json.load(f)[str(ctx.guild.id)]
    embed = discord.Embed(title='Speed', description=f'**A game where you must send a message every second** \n\nStart a game with {prefix}speed \n\nHow to play: \nOnce the game starts, you must type a message every second\nAnyone can send a message to keep the game going\nYou lose if a message hasn\'t been sent for more than a second', color=color())
    await ctx.send(embed=embed)

keep_alive()
bot.run(token)