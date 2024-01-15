import random
import asyncio
import os
import json
import discord
from discord import app_commands
from discord.ext import commands


# Crea una instancia del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

token = ""
OWNER_USERID = 342287101225598987
data = None
save_data = {
    "guilds": [],
    "current_dif": 2,
    "messages": ["Juan haz el minimini"]
}

# Obrim el token del server del fitxer .token
with open(".token") as f:
    token = f.read()

with open("data.json") as f:
    data = json.loads(f.read())

if os.path.exists(".save_data.json"):
    with open(".save_data.json") as f:
        save_data = json.loads(f.read())


def save():
    global save_data
    with open(".save_data.json", "w") as f:
        f.write(json.dumps(save_data))
    print("Data saved succesfully")

async def fetch_guild(guild_id):
    return bot.get_guild(guild_id)

async def fetch_channel(channel_id):
    return bot.get_channel(channel_id)

async def change_icon(img_path):
    with open(img_path, 'rb') as file:
            imagen_bytes = file.read()
    # Cambia la imagen del servidor
    try:
        await bot.user.edit(avatar=imagen_bytes)
    except:
        print("Error muy rapido cambio de avatar")

async def global_log(msg):
    for guild_obj in save_data["guilds"]:
        channel = await fetch_channel(guild_obj["log_channel"])
        await channel.send(msg)
                
async def update_difficulty():
    if save_data["current_dif"] < 0:
        save_data["current_dif"] = 0
    if save_data["current_dif"] >= len(data["difficulties"]):
        save_data["current_dif"] = len(data["difficulties"]) - 1
    
    save()
    
    await change_icon("data/difficulty/" + data["difficulties"][save_data["current_dif"]]["icon"])
    await global_log("Dificultad cambiada a " + data["difficulties"][save_data["current_dif"]]["name"])


@tree.command(name='dif')
@app_commands.describe(command="Acción que hacer con el comando")
@app_commands.choices(command=[
    app_commands.Choice(name='Up', value=1),
    app_commands.Choice(name='Down', value=2),
    app_commands.Choice(name='Show', value=3)
    ])
async def change_difficulty(ctx, command: app_commands.Choice[int]):
    print("????")
    global save_data

    if command.name == "Up":
        save_data["current_dif"] += 1
        await update_difficulty()
    elif command.name == "Down":
        save_data["current_dif"] -= 1
        await update_difficulty()
    else:
        await ctx.send('Dificultad actual: ' + data["difficulties"][save_data["current_dif"]]["name"])

@tree.command(name="difset", description="Fija la dificultad del bot")
@app_commands.describe(num="Número de la dificultad (más alto más dificultad)")
async def set_difficulty(ctx, num: int):
    save_data["current_dif"] = int(num)
    await update_difficulty()

@tree.command(name="test", description="Crec que no va")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Test")

@tree.command(name="msg")
@app_commands.describe(cmd="Comanda a fer amb els missatges")
@app_commands.describe(msg="Missatge a posar")
async def _msg_add(ctx: discord.Interaction, cmd: str, msg: str):
    if cmd == "add":
        if msg is not None:
            save_data["messages"].append(msg)

            save()
            await ctx.send("Añadido mensaje " + msg)

# Comando para cambiar la imagen del servidor
@tree.command(name='set_server')
@app_commands.describe(first_channel="Primer canal")
@app_commands.describe(second_channel="Segon canal")
async def _set_server(ctx, first_channel: discord.VoiceChannel, second_channel: discord.VoiceChannel):

    global save_data
    # Verifica si el bot tiene permisos para cambiar la configuración del servidor
    if ctx.guild and ctx.guild.me.guild_permissions.manage_guild:

        save_data["guilds"] = list(filter(lambda x : x["id"] != ctx.guild.id, save_data["guilds"]))
        save_data["guilds"].append({
            "id": ctx.guild.id,
            "log_channel": ctx.channel.id,
            "first_channel": int(first_channel.id),
            "second_channel": int(second_channel.id)
        })

        print(save_data["guilds"])

        save()

        await ctx.send('¡Servidor registrado correctamente en este canal!')

    else:
        await ctx.send('El bot no tiene permisos para cambiar la configuración del servidor.')

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == OWNER_USERID:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

async def change_line(guild_object):

    guild = await fetch_guild(guild_object["id"])
    channel = await fetch_channel(guild_object["log_channel"])

    vc1 = await fetch_channel(guild_object["first_channel"])
    vc2 = await fetch_channel(guild_object["second_channel"])

    print(guild)

    if guild and guild.me.guild_permissions.manage_guild:

        line = data["lines"][random.randint(0,len(data["lines"]) - 1)]

        # Construye la ruta de la imagen
        imagen_path = f'./data/lines/{line["image"]}'  # Ajusta según la ubicación y el formato de tus imágenes

        # Abre y carga la imagen
        with open(imagen_path, 'rb') as file:
            imagen_bytes = file.read()

        # Cambia la imagen del servidor
        await guild.edit(icon=imagen_bytes, name=line["server_name"])

        await vc1.edit(name = line["start"])
        await vc2.edit(name = line["end"])

    else:
        print('El bot no tiene permisos para cambiar la configuración del servidor ' + guild.name)

@bot.event
async def on_ready():
    asyncio.ensure_future(main())

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    required = data["difficulties"][save_data["current_dif"]]["odd"]
    if random.uniform(0, 1) < required:
        if message.author == bot.user:
            return
        msg = save_data["messages"][random.randint(0, len(save_data["messages"]) - 1)]
        await message.channel.send(msg, reference=message)

async def random_dif_update():
    global data
    global save_data
    mod = len(data["difficulties"]) / 2 - save_data["current_dif"]
    # És més baix si la dif és més alta

    up_prob = 0.5 + ((mod / len(data["difficulties"])) * 2) / 4
    if random.uniform(0,1) < up_prob:
        save_data["current_dif"] += 1
        await update_difficulty()
    else:
        save_data["current_dif"] -= 1
        await update_difficulty()

async def main():
    global data
    global save_data

    print("Data:")
    print(data)
    print("Save data:")
    print(save_data)
    while True:
        if len(save_data["guilds"]) > 0:
            for guild_obj in save_data["guilds"]:
                # await change_line(guild_obj)

                print("???")
                await tree.sync(guild=discord.Object(id=guild_obj["id"]))
                print("QUe")
                if(save_data["current_dif"] != 0):
                    await random_dif_update()
            await asyncio.sleep(3600 * 24)
        else:
            await asyncio.sleep(1)

# Conecta el bot al servidor de Discord
bot.run(token)
