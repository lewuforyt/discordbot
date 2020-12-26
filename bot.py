import discord
from discord.ext import commands
import time

client = commands.Bot(command_prefix = '.')

komutlar = [{"isim":"Ban", "kod":"ban", "aciklama":"Belirttiğiniz kişiyi banlar."},
            {"isim":"Kick", "kod":"kick", "aciklama":"Belirttiğiniz kişiyi kickler"},
            {"isim":"Ping", "kod":"ping", "aciklama":"Botun ping'ini söyler"},
            {"isim":"Kaç sunucu ?", "kod":"kacsunucu", "aciklama":"Kaç sunucuda hizmet ettiğini söyler."},
            {"isim":"Yardım", "kod":"help", "aciklama":"Yardım komutudur. Komutların listesini söyler."},
            {"isim":"Kullanıcı Bilgisi", "kod":"user", "aciklama":"Kullanıcının bilgisini gösterir."},
            {"isim":"Yapımcı", "kod":"admin", "aciklama":"Kısaca admin bilgisi"},
           {"isim":"Sunucu bilgisi", "kod":"serverinfo", "aciklama":"Kısaca sunucu bilgisi"}]

client.remove_command('help')

@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def help(ctx):
    await ctx.message.add_reaction("😋")
    embed = discord.Embed(
    colour = discord.Colour.orange()
    )
    embed.set_author(name =ctx.message.author)

    for _ in komutlar:
        embed.add_field(name =_['isim'], value=f"Açıklama : {_['aciklama']}\nKod : {_['kod']}", inline=True)
    

    embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/0cDy5smIATH2PlW4_5_B_K6MYbq9rLSfX7hIz8t392Y/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/791220109704167454/3585b46450b604885178baaddfba949a.webp?width=419&height=419')
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} , {reason} Sebebiyle banlandı')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f'{member} , {reason} Sebebiyle kick\'lendi ')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount)
    mesjj = await ctx.send(f"{amount} mesaj silindi. Bu mesaj kendini imha edecek.")
    time.sleep(5)
    await mesjj.delete()


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f'Pingim: {round(client.latency * 1000)}')



@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def kacsunucu(ctx):
    count = 0
    for _ in client.guilds:
        count+=1
    print(count)
    await ctx.send(str(count)+' Sunucuda hizmet veriyorum')

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def user(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author

    embed = discord.Embed(
    colour = discord.Colour.blue()
    )
    embed.set_author(name= member.name)

    rolesa = member.roles

    roller =  []
    saeq = "'"
    for _ in rolesa:
        roller.append(_.mention)
    embed.add_field(name= "Rolleri", value=f"{str(roller[1:]).replace('[', '').replace(']', '').replace(',', '').replace(saeq, '')}", inline=True)

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Kullanıcı id: {member.id}")
    await ctx.send(embed=embed)

@client.command()
async def admin(ctx):
    await ctx.send(f"THT Discord Botu\nYapımcı: Ar-Ge <-> Xenopeltis")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Yanlış bir komut yazdınız.(.help) yazarak komut listesini alabilirsiniz.')

    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send('Bunu yapmaya yetkin yok.')
        time.sleep(3)
        await msg.delete()
    
    if isinstance(error, commands.CommandOnCooldown):
        saniye = int(str(error).split(" ")[-1].split('.')[0])
        msg = await ctx.send(f'Çok hızlısın. {saniye} saniye sonra tekrar dene.')
        time.sleep(3)
        await msg.delete()

@client.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name,
        description=f"Sunucu sahibi: {ctx.guild.owner.mention}",
        color=discord.Color.blue()
    )

    dnd = 0
    off = 0
    on = 0
    idle = 0

    for _ in ctx.guild.members:
        if str(_.status) == "dnd":
            dnd+=1

        if str(_.status) == "idle":
            idle+=1

        if str(_.status) == "offline":
            off+=1

        if str(_.status) == "online":
            on+=1

    embed.add_field(name=f"{len(ctx.guild.channels)} kanal bulunuyor.", value=f"**{len(ctx.guild.text_channels)}** Text Kanalı\n**{len(ctx.guild.voice_channels)}** Ses Kanalı\n**{len(ctx.guild.categories)}** Kategori", inline=True)
    embed.add_field(name=f"{ctx.guild.member_count} Üye blunuyor.", value=f":green_circle: {on} Aktif\n:red_circle: {dnd} Rahatsız Etmeyin\n:yellow_circle: {idle} Boşta\n:white_circle: {off} Çevrimdışı", inline=True)
    embed.add_field(name="Oluşturulma Tarihi", value=ctx.guild.created_at)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Sunucu id: {id}")


    await ctx.send(embed=embed)
                    
client.run("token")
