import discord
import config
import records
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
bot = commands.Bot(command_prefix='!')


def get_name(s):
    return s.encode('ascii', 'namereplace')

@bot.command()
async def emojiname(ctx, arg):
    await ctx.send(get_name(arg))

yesnorc = ["♥", "🚫"]

# main command
@bot.command()
async def hug(ctx, musr: discord.User=None):
    if(ctx.author == musr):
        await ctx.send('_{} hugged themself, somehow_'.format(ctx.author.mention))
        return
    if(records.getblockst(ctx.author, musr)):
        return

    msg = await ctx.send('_Sent a virtual hug to {} from {}._'.format(musr.mention, ctx.author.mention))
    print('Recieved hug request from {} to {}. Waiting for acceptance...'.format(ctx.author, musr))
    for emoji in yesnorc:
        await msg.add_reaction(emoji)
    def check(reaction, user):
        return user == musr
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
        await msg.delete()
        records.RecordNRG(ctx.author, musr)
        await ctx.send('_{} did not react in time_'.format(musr.mention))
    else:
        if(str(reaction.emoji) == "♥"):
            await msg.clear_reactions()
            await msg.delete()
            await ctx.send("_{} accepted virtual hug from {}_".format(musr.mention, ctx.author.mention))
            records.RecordHug(ctx.author, musr, True)
            print('Hug request from {} to {} was accepted.'.format(ctx.author, musr))
        elif(str(reaction.emoji) == "🚫"):
            await msg.clear_reactions()
            await msg.delete()
            await ctx.send("_{} rejected virtual hug from {}_".format(musr.mention, ctx.author.mention))
            records.RecordHug(ctx.author, musr, False)
            print('Hug request from {} to {} was rejected.'.format(ctx.author, musr))


@bot.command()
async def senthugs(ctx, musr: discord.User=None):
    if(ctx.author == musr):
        return

    res = records.getinfo(ctx.author, musr)
    re = res[0]
    await ctx.send('{} has sended {} hugs to {}. {} were accepted, {} were denied, {} got no reply in time'.format(ctx.author, re[0], musr, re[1], re[2], re[3]))
@bot.command()
async def recievedhugs(ctx, musr: discord.User=None):
    if(ctx.author == musr):
        return

    res = records.getinfo(musr, ctx.author)
    if(len(res) < 1):
        await ctx.send('{} hasn\'t recieved any hugs yet from {}'.format(ctx.author, musr))
    re = res[0]
    await ctx.send('{} has recieved {} hugs from {}. {} were accepted, {} were denied, {} got no reply in time'.format(ctx.author, re[0], musr, re[1], re[2], re[3]))


@bot.command()
async def block(ctx, musr: discord.User=None):
    if(ctx.author == musr):
        return
    records.blockUsr(ctx.author, musr)
    print('{} blocked {}.'.format(ctx.author, musr))

@bot.command()
async def unblock(ctx, musr: discord.User=None):
    if(ctx.author == musr):
        return
    records.unblockUsr(ctx.author, musr)
    print('{} unblocked {}.'.format(ctx.author, musr))



bot.run(config.token)
