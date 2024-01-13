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

# Comando para cambiar la imagen del servidor
@bot.command()
async def cambiar_imagen(ctx, nombre_imagen: str):
    try:
        # Verifica si el bot tiene permisos para cambiar la configuración del servidor
        if ctx.guild and ctx.guild.me.guild_permissions.manage_guild:
            # Construye la ruta de la imagen
            imagen_path = f'./{nombre_imagen}.png'  # Ajusta según la ubicación y el formato de tus imágenes

            # Abre y carga la imagen
            with open(imagen_path, 'rb') as file:
                imagen_bytes = file.read()

            # Cambia la imagen del servidor
            await ctx.guild.edit(icon=imagen_bytes)
            await ctx.send('¡Imagen del servidor cambiada correctamente!')

        else:
            await ctx.send('El bot no tiene permisos para cambiar la configuración del servidor.')

    except FileNotFoundError:
        await ctx.send(f'La imagen {nombre_imagen} no fue encontrada.')

# Conecta el bot al servidor de Discord
bot.run(token)
