import lightbulb
import hikari
import config
from datetime import datetime
from datetime import date
import threading
import pytz
import time

bot = lightbulb.BotApp(
    token=config.discord_token, 
    default_enabled_guilds=(int(config.server_code))
)

scouts = []
finishes = [] 

def check_time():
    # Define the timezone
    pst = pytz.timezone('America/Los_Angeles')
    
    while True:
        # Get the current time in PST timezone
        current_time = datetime.now(pst)
        
        # Check if the current time is 3 AM
        if current_time.hour == 3 and current_time.minute == 0:
            scouts.clear()
            finishes.clear()
        else:
            print("It is not reset yet...")
        
        # Wait for some time before checking again
        time.sleep(60)  # Wait for 60 seconds (1 minute)

# @bot.listen(hikari.GuildMessageCreateEvent)
# async def print_message(event):
#     print(event.content)
    
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print("Bot has started")
    
@bot.command
@lightbulb.command('resources', 'provides a list of E7 resources')
@lightbulb.implements(lightbulb.SlashCommand)
async def resources(ctx):
    embed = (
        hikari.Embed(
            title = 'Useful E7 Resources',
            colour = 0xFBBBBD
        )
        .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
        .add_field("Deity's New Player Guide", "https://www.youtube.com/playlist?list=PLUKW1vS-gUSTREJGkUFCPNE6OhWSji9Yp")
        .add_field("Stove Page", "Official E7 News and Updates. https://page.onstove.com/epicseven/global/list/985?page=1&direction=LATEST")
        .add_field("Cecilia Bot", "Database for hero stats, banner timeline, camping simulator, tierlist maker, and more! https://ceciliabot.github.io/#/ ")
        .add_field("Epic 7 Damage Calculator", "https://e7calc.xyz/")
        .add_field("Fribbels GW Meta Tracker", "https://fribbels.github.io/e7/gw-meta.html")
        .add_field("Fribbels Hero Library", "https://fribbels.github.io/e7/hero-library.html")
        .add_field("Fribbels Gear Optimizer", "https://github.com/fribbels/Fribbels-Epic-7-Optimizer")
        .add_field("E7 Vault", "Datamined resources and assets. https://www.e7vau.lt/index.html")
        .add_field("RTA Match History", "https://epic7.gg.onstove.com/en")
    )
    await ctx.respond(embed)

# Guild War Commands 

# Starts a thread to reset the lists
time_thread = threading.Thread(target=check_time)
time_thread.start()

@bot.command
@lightbulb.command('gw', 'This is a group!')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx):
    pass

# scouts 
@my_group.child
@lightbulb.option('ign', 'IGN', type = str)
@lightbulb.command('scout', 'scouting!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    
    # loops through 2d array to find already scouted tower names and who hit them
    for i in range(len(scouts)):
        for j in range(len(scouts[i])):
            if scouts[i][j] == ctx.options.ign.lower():
                
                user = scouts[i][j+1]
                embed = (
                    hikari.Embed(
                        title = 'Shinrai Callouts',
                        colour = 0xFF0000
                    )
                    .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
                    .add_field('Finishing Callout', f"{ctx.options.ign.lower()} is already being scouted by {user.mention}!")

                )
                await ctx.respond(embed)
                return
    
    
    scouts.append([ctx.options.ign.lower(), ctx.author])
    user = ctx.author
    
    embed = (
        hikari.Embed(
            title = 'Shinrai Callouts',
            colour = 0x00FF00
        )
        .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
        .add_field('Scouting Callout', f"{ctx.options.ign.lower()} is being scouted by {user.mention}!")

    )
    await ctx.respond(embed)

# finishes
@my_group.child
@lightbulb.option('ign', 'IGN', type = str)
@lightbulb.command('finish', 'finshing!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    
    # loops through 2d array to find already finished tower names and who hit them
    for i in range(len(finishes)):
        for j in range(len(finishes[i])):
            if finishes[i][j] == ctx.options.ign.lower():
                
                user = finishes[i][j+1]
                embed = (
                    hikari.Embed(
                        title = 'Shinrai Callouts',
                        colour = 0xFF0000
                    )
                    .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
                    .add_field('Finishing Callout', f"{ctx.options.ign.lower()} is already being finished by {user.mention}!")

                )
                await ctx.respond(embed)
                return
            
    finishes.append([ctx.options.ign.lower(), ctx.author])
    
    user = ctx.author
    
    embed = (
        hikari.Embed(
            title = 'Shinrai Callouts',
            colour = 0x00FF00
        )
        .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
        .add_field('Finishing Callout', f"{ctx.options.ign.lower()} is being finished by {user.mention}!")

    )
    await ctx.respond(embed)

# nvm 
@my_group.child
@lightbulb.option('ign', 'IGN', type = str)
@lightbulb.command('nvm', 'undo a scout/finish')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    
    for i in range(len(scouts)):
        for j in range(len(scouts[i])):
            if scouts[i][j] == ctx.options.ign.lower():
                
                user = scouts[i][j+1]
                scouts.remove(scouts[i])
                
                embed = (
                    hikari.Embed(
                        title = 'Shinrai Callouts',
                        colour = 0xFFFF00
                    )
                    .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
                    .add_field('Scouting Callout', f"{ctx.options.ign.lower()} has been unscouted by {user.mention}!")

                )
                await ctx.respond(embed)
                return
            
    for i in range(len(finishes)):
        for j in range(len(finishes[i])):
            if finishes[i][j] == ctx.options.ign.lower():
                
                
                user = finishes[i][j+1]
                finishes.remove(finishes[i])
                
                embed = (
                    hikari.Embed(
                        title = 'Shinrai Callouts',
                        colour = 0xFFFF00
                    )
                    .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
                    .add_field('Finishing Callout', f"{ctx.options.ign.lower()} still needs to be finished!")

                )
                await ctx.respond(embed)
                return
    
    # if someone typed without prior scout or finish        
    embed = (
        hikari.Embed(
            title = 'Shinrai Callouts',
            colour = 0xFF0000
        )
        .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
        .add_field('Error!', f"{ctx.options.ign.lower()}'s tower hasn't been scouted or finished")

    )
    await ctx.respond(embed)
    return

# match up of the day
@my_group.child
@lightbulb.option('matchup', 'guild name', type = str)
@lightbulb.command('matchup', 'records the matchup')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    embed = (
        hikari.Embed(
            title = 'Matchup of the day!',
            colour = 0x00FF00
        )
        .set_thumbnail("https://gamepress.gg/epicseven/sites/epicseven/files/2020-12/c1104_su.png")
        .add_field(str(date.today()), "Shinrai versus " + ctx.options.matchup)

    )
    await ctx.respond(embed)
    

bot.run()