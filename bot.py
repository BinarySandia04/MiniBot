import random
import time
import asyncio
import discord
from discord.ext import commands

# Crea una instancia del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='%%', intents=intents)

token = ""
# Obrim el token del server del fitxer .token
with open(".token") as f:
    token = f.read()


guilds = []

lines = [
    {"name": "R1", "image": "R1.jpg", "server_name": "R1 - Rodalies de Catalunya"},
    {"name": "R2", "image": "R2.png", "server_name": "R2 - Rodalies de Catalunya"},
    {"name": "R2 Nord", "image": "R2_Nord.png", "server_name": "R2 Nord - Rodalies de Catalunya"},
    {"name": "R2 Sud", "image": "R2_Sud.png", "server_name": "R2 Sud - Rodalies de Catalunya"},
    {"name": "R3", "image": "R3.png", "server_name": "R3 - Rodalies de Catalunya"},
    {"name": "R4", "image": "R4.png", "server_name": "R4 - Rodalies de Catalunya"},
    {"name": "R7", "image": "R7.png", "server_name": "R7 - Rodalies de Catalunya"},
    {"name": "R8", "image": "R8.png", "server_name": "R8 - Rodalies de Catalunya"},
    {"name": "R11", "image": "R12.png", "server_name": "R12 - Rodalies de Catalunya"},
    {"name": "R13", "image": "R13.png", "server_name": "R13 - Rodalies de Catalunya"},
    {"name": "R14", "image": "R14.png", "server_name": "R14 - Rodalies de Catalunya"},
    {"name": "R15", "image": "R15.png", "server_name": "R15 - Rodalies de Catalunya"},
    {"name": "R16", "image": "R16.png", "server_name": "R16 - Rodalies de Catalunya"},
    {"name": "R17", "image": "R17.png", "server_name": "R17 - Rodalies de Catalunya"},
    {"name": "RG1", "image": "RG1.png", "server_name": "RG1 - Rodalies de Catalunya"},
    {"name": "RT1", "image": "RT1.png", "server_name": "RT1 - Rodalies de Catalunya"},
    {"name": "RT2", "image": "RT2.png", "server_name": "RT2 - Rodalies de Catalunya"},
]

# Comando para cambiar la imagen del servidor
@bot.command(name='set_server')
async def _set_server(ctx):

    global guilds
    # Verifica si el bot tiene permisos para cambiar la configuración del servidor
    if ctx.guild and ctx.guild.me.guild_permissions.manage_guild:

        guilds = list(filter(lambda x : x["guild"] != ctx.guild, guilds))
        guilds.append({ "guild": ctx.guild, "channel": ctx.channel })

        print(guilds)

        await ctx.send('¡Servidor registrado correctamente en este canal!')
        # await change_image(ctx.guild, ctx.channel)

    else:
        await ctx.send('El bot no tiene permisos para cambiar la configuración del servidor.')

async def change_image(guild, log_channel):
    if guild and guild.me.guild_permissions.manage_guild:

        line = lines[random.randint(0,len(lines) - 1)]

        # Construye la ruta de la imagen
        imagen_path = f'./data/lines/{line["image"]}'  # Ajusta según la ubicación y el formato de tus imágenes

        # Abre y carga la imagen
        with open(imagen_path, 'rb') as file:
            imagen_bytes = file.read()

        # Cambia la imagen del servidor
        await guild.edit(icon=imagen_bytes, name=line["server_name"])
        await log_channel.send("Servidor cambiado a " + line["name"] + "!")

    else:
        print('El bot no tiene permisos para cambiar la configuración del servidor ' + guild.name)

@bot.event
async def on_ready():
    asyncio.ensure_future(main())
    

async def main():
    print("EHHHH macarena")
    while True:
        if len(guilds) > 0:
            for guild in guilds:
                await change_image(guild["guild"], guild["channel"])
            await asyncio.sleep(3600)
        else:
            print("Esperant servers...")
            await asyncio.sleep(1)

# Conecta el bot al servidor de Discord
bot.run(token)
